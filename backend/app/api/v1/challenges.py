from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.learning import CodingChallenge, CodeSubmission
from app.services.sandbox import evaluate_challenge_submission
from app.services.gamification import award_xp, record_qualifying_activity, increment_quest_progress, evaluate_achievements
from app.services.rate_limit import rate_limiter
from app.core.config import settings

router = APIRouter()


@router.get("")
def list_challenges(
    path_slug: str | None = None,
    difficulty: str | None = None,
    limit: int = Query(20, le=50),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(CodingChallenge).where(CodingChallenge.is_published.is_(True))
    if path_slug:
        q = q.where(CodingChallenge.path_slug == path_slug)
    if difficulty:
        q = q.where(CodingChallenge.difficulty == difficulty)
    challenges = db.scalars(q.offset(offset).limit(limit)).all()
    solved_ids = set(
        db.scalars(select(func.distinct(CodeSubmission.challenge_id)).where(
            CodeSubmission.user_id == current_user.id, CodeSubmission.passed.is_(True)
        )).all()
    )
    return [
        {
            "id": c.id, "slug": c.slug, "title": c.title, "description": c.description,
            "mode": c.mode, "difficulty": c.difficulty, "xp_reward": c.xp_reward,
            "path_slug": c.path_slug, "solved": c.id in solved_ids,
        }
        for c in challenges
    ]


@router.get("/{challenge_id}")
def get_challenge(challenge_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    c = db.get(CodingChallenge, challenge_id)
    if not c:
        raise HTTPException(404, "Challenge not found")
    return {
        "id": c.id, "slug": c.slug, "title": c.title, "description": c.description,
        "mode": c.mode, "difficulty": c.difficulty, "xp_reward": c.xp_reward,
        "starter_code": c.starter_code, "hints": c.hints,
        "test_cases": [{"name": t.get("name"), "assert_expr": t.get("assert_expr")} for t in (c.test_cases or []) if not t.get("hidden")],
    }


class SubmitIn(BaseModel):
    code: str
    used_hint: bool = False


@router.post("/{challenge_id}/submit")
def submit_challenge(
    challenge_id: int,
    payload: SubmitIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tz: str = Depends(get_user_timezone),
):
    if not rate_limiter.allow(f"sandbox:{current_user.id}", settings.SANDBOX_RATE_LIMIT_PER_MINUTE):
        raise HTTPException(429, "Too many submissions. Please wait a moment.")
    c = db.get(CodingChallenge, challenge_id)
    if not c:
        raise HTTPException(404, "Challenge not found")
    
    eval_result = evaluate_challenge_submission(payload.code, c.test_cases or [], c.expected_output)
    
    already_solved = db.scalar(
        select(CodeSubmission).where(
            CodeSubmission.user_id == current_user.id,
            CodeSubmission.challenge_id == challenge_id,
            CodeSubmission.passed.is_(True),
        )
    )
    xp_result = {}
    if eval_result["passed"] and not already_solved:
        xp_to_award = max(10, c.xp_reward - (10 if payload.used_hint else 0))
        xp_result = award_xp(db, current_user.id, xp_to_award, "challenge", str(c.id),
                              f"Solved challenge: {c.title}",
                              f"challenge:{current_user.id}:{c.id}", tz)
        record_qualifying_activity(db, current_user.id, tz, challenges_delta=1)
        increment_quest_progress(db, current_user.id, "challenges_solved", 1, tz)
        if not payload.used_hint:
            increment_quest_progress(db, current_user.id, "challenges_no_hint", 1, tz)
    
    submission = CodeSubmission(
        user_id=current_user.id, challenge_id=c.id, code=payload.code,
        passed=eval_result["passed"], passed_tests=eval_result.get("passed_tests", 0),
        total_tests=eval_result.get("total_tests", 0), used_hint=payload.used_hint,
        xp_awarded=xp_result.get("xp_added", 0),
        execution_time_ms=eval_result.get("execution_time_ms", 0.0),
        feedback={"details": eval_result.get("details", [])},
    )
    db.add(submission)
    new_achievements = evaluate_achievements(db, current_user.id, tz)
    db.commit()
    return {**eval_result, "xp_result": xp_result, "new_achievements": new_achievements}
