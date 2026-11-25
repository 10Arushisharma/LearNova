from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.learning import (
    LearningPath, Module, Lesson, LessonProgress, Quiz, Question, QuizAttempt
)
from app.models.gamification import DailyActivity, XPTransaction
from app.services.gamification import award_xp, record_qualifying_activity, increment_quest_progress, evaluate_achievements
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()


@router.get("/paths")
def list_paths(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    paths = db.scalars(select(LearningPath).where(LearningPath.is_published.is_(True)).order_by(LearningPath.order_index)).all()
    result = []
    for p in paths:
        total_lessons = db.scalar(
            select(func.count(Lesson.id)).join(Module).where(Module.path_id == p.id, Lesson.is_published.is_(True))
        ) or 0
        done_lessons = db.scalar(
            select(func.count(LessonProgress.id)).join(Lesson).join(Module).where(
                Module.path_id == p.id, LessonProgress.user_id == current_user.id, LessonProgress.status == "completed"
            )
        ) or 0
        result.append({
            "id": p.id, "slug": p.slug, "title": p.title, "subtitle": p.subtitle,
            "description": p.description, "difficulty": p.difficulty, "icon_name": p.icon_name,
            "accent_color": p.accent_color, "estimated_hours": p.estimated_hours,
            "total_lessons": total_lessons, "completed_lessons": done_lessons,
            "progress_percentage": round(done_lessons / total_lessons * 100, 1) if total_lessons else 0,
        })
    return result


@router.get("/paths/{slug}")
def get_path(slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    path = db.scalar(select(LearningPath).where(LearningPath.slug == slug, LearningPath.is_published.is_(True)))
    if not path:
        raise HTTPException(404, "Learning path not found")
    modules = db.scalars(select(Module).where(Module.path_id == path.id, Module.is_published.is_(True)).order_by(Module.order_index)).all()
    mods_data = []
    for m in modules:
        lessons = db.scalars(select(Lesson).where(Lesson.module_id == m.id, Lesson.is_published.is_(True)).order_by(Lesson.order_index)).all()
        lessons_data = []
        for l in lessons:
            prog = db.scalar(select(LessonProgress).where(LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == l.id))
            lessons_data.append({
                "id": l.id, "slug": l.slug, "title": l.title, "summary": l.summary,
                "xp_reward": l.xp_reward, "estimated_minutes": l.estimated_minutes,
                "order_index": l.order_index, "status": prog.status if prog else "not_started",
            })
        mods_data.append({"id": m.id, "slug": m.slug, "title": m.title, "description": m.description,
                           "order_index": m.order_index, "xp_reward": m.xp_reward, "lessons": lessons_data})
    return {"id": path.id, "slug": path.slug, "title": path.title, "subtitle": path.subtitle,
            "description": path.description, "difficulty": path.difficulty, "icon_name": path.icon_name,
            "accent_color": path.accent_color, "estimated_hours": path.estimated_hours, "modules": mods_data}


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson or not lesson.is_published:
        raise HTTPException(404, "Lesson not found")
    quiz = db.scalar(select(Quiz).where(Quiz.lesson_id == lesson.id))
    quiz_data = None
    if quiz:
        questions = db.scalars(select(Question).where(Question.quiz_id == quiz.id).order_by(Question.order_index)).all()
        quiz_data = {
            "id": quiz.id, "title": quiz.title, "pass_percentage": quiz.pass_percentage,
            "xp_reward": quiz.xp_reward, "time_limit_seconds": quiz.time_limit_seconds,
            "questions": [
                {
                    "id": q.id, "question_type": q.question_type, "prompt": q.prompt,
                    "code_snippet": q.code_snippet, "options": q.options, "topic_tag": q.topic_tag,
                    # Do NOT include correct_answer in the response (sent separately on submit)
                }
                for q in questions
            ],
        }
    prog = db.scalar(select(LessonProgress).where(LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == lesson.id))
    return {
        "id": lesson.id, "slug": lesson.slug, "title": lesson.title, "summary": lesson.summary,
        "learning_objectives": lesson.learning_objectives,
        "content_blocks": lesson.content_blocks,
        "key_terms": lesson.key_terms,
        "common_mistakes": lesson.common_mistakes,
        "interactive_lab_type": lesson.interactive_lab_type,
        "starter_code": lesson.starter_code,
        "xp_reward": lesson.xp_reward,
        "estimated_minutes": lesson.estimated_minutes,
        "status": prog.status if prog else "not_started",
        "quiz": quiz_data,
    }


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tz: str = Depends(get_user_timezone),
):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    prog = db.scalar(select(LessonProgress).where(LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == lesson.id))
    if not prog:
        prog = LessonProgress(user_id=current_user.id, lesson_id=lesson.id)
        db.add(prog)
        db.flush()
    if prog.status == "completed" and prog.xp_awarded:
        from app.services.gamification import compute_level_info
        from app.models.gamification import UserLevel
        lvl = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
        return {"already_completed": True, "xp_awarded": 0, "level_info": compute_level_info(lvl.total_xp if lvl else 0)}
    prog.status = "completed"
    prog.completed_at = datetime.now(timezone.utc)
    xp_result = {}
    if not prog.xp_awarded:
        prog.xp_awarded = True
        xp_result = award_xp(db, current_user.id, lesson.xp_reward, "lesson", str(lesson.id),
                              f"Completed lesson: {lesson.title}",
                              f"lesson:{current_user.id}:{lesson.id}", tz)
    record_qualifying_activity(db, current_user.id, tz, lessons_delta=1, minutes_delta=lesson.estimated_minutes)
    increment_quest_progress(db, current_user.id, "lessons_completed", 1, tz)
    new_achievements = evaluate_achievements(db, current_user.id, tz)
    db.commit()
    return {"lesson_id": lesson.id, "xp_result": xp_result, "new_achievements": new_achievements}


class QuizSubmit(BaseModel):
    answers: dict  # {question_id: answer_value}
    duration_seconds: int = 0


@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(
    quiz_id: int,
    payload: QuizSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tz: str = Depends(get_user_timezone),
):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    questions = db.scalars(select(Question).where(Question.quiz_id == quiz.id)).all()
    correct = 0
    topic_scores: dict[str, dict] = {}
    results = []
    for q in questions:
        correct_val = q.correct_answer.get("value")
        submitted = payload.answers.get(str(q.id))
        is_correct = str(submitted) == str(correct_val)
        if is_correct:
            correct += 1
        t = q.topic_tag
        if t not in topic_scores:
            topic_scores[t] = {"correct": 0, "total": 0}
        topic_scores[t]["total"] += 1
        if is_correct:
            topic_scores[t]["correct"] += 1
        results.append({"question_id": q.id, "correct": is_correct, "correct_answer": correct_val, "explanation": q.explanation})
    
    total = len(questions)
    score_pct = round(correct / total * 100, 1) if total else 0
    passed = score_pct >= quiz.pass_percentage
    xp_earned = quiz.xp_reward if passed else 0
    xp_result = {}
    if xp_earned:
        # Use attempt count as idempotency suffix to allow multiple attempts
        attempt_count = db.scalar(select(func.count(QuizAttempt.id)).where(QuizAttempt.user_id == current_user.id, QuizAttempt.quiz_id == quiz.id)) or 0
        xp_result = award_xp(db, current_user.id, xp_earned, "quiz", str(quiz.id),
                              f"Passed quiz: {quiz.title}",
                              f"quiz:{current_user.id}:{quiz.id}:attempt{attempt_count + 1}", tz)
    attempt = QuizAttempt(
        user_id=current_user.id, quiz_id=quiz.id,
        answers={str(k): v for k, v in payload.answers.items()},
        score_percentage=score_pct, passed=passed,
        correct_count=correct, total_count=total,
        topic_breakdown={t: {"pct": round(v["correct"] / v["total"] * 100, 1) if v["total"] else 0} for t, v in topic_scores.items()},
        xp_awarded=xp_earned, duration_seconds=payload.duration_seconds,
    )
    db.add(attempt)
    if passed:
        increment_quest_progress(db, current_user.id, "quizzes_passed", 1, tz)
    if score_pct >= 100:
        increment_quest_progress(db, current_user.id, "perfect_quiz", 1, tz)
    record_qualifying_activity(db, current_user.id, tz, quizzes_delta=1 if passed else 0)
    new_achievements = evaluate_achievements(db, current_user.id, tz)
    db.commit()
    return {
        "score_percentage": score_pct,
        "passed": passed,
        "correct_count": correct,
        "total_count": total,
        "topic_breakdown": topic_scores,
        "results": results,
        "xp_result": xp_result,
        "new_achievements": new_achievements,
    }
