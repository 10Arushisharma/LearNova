from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.project import Project, ProjectSubmission
from app.services.gamification import award_xp, evaluate_achievements

router = APIRouter()


@router.get("")
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.scalars(select(Project).where(Project.is_published.is_(True))).all()
    completed_ids = set(
        db.scalars(select(ProjectSubmission.project_id).where(
            ProjectSubmission.user_id == current_user.id, ProjectSubmission.passed.is_(True)
        )).all()
    )
    return [
        {
            "id": p.id, "slug": p.slug, "title": p.title, "summary": p.summary,
            "difficulty": p.difficulty, "technologies": p.technologies,
            "xp_reward": p.xp_reward, "completed": p.id in completed_ids,
        }
        for p in projects
    ]


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = db.get(Project, project_id)
    if not p:
        raise HTTPException(404, "Project not found")
    return {
        "id": p.id, "slug": p.slug, "title": p.title, "summary": p.summary,
        "problem_statement": p.problem_statement, "difficulty": p.difficulty,
        "technologies": p.technologies, "prerequisites": p.prerequisites,
        "learning_objectives": p.learning_objectives, "milestones": p.milestones,
        "evaluation_criteria": p.evaluation_criteria, "sample_dataset": p.sample_dataset,
        "starter_code": p.starter_code, "xp_reward": p.xp_reward,
    }


class ProjectSubmitIn(BaseModel):
    code: str
    notes: str = ""
    completed_milestones: list[int] = []


@router.post("/{project_id}/submit")
def submit_project(
    project_id: int,
    payload: ProjectSubmitIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tz: str = Depends(get_user_timezone),
):
    p = db.get(Project, project_id)
    if not p:
        raise HTTPException(404, "Project not found")
    
    # Backend keyword-based evaluation
    code_lower = payload.code.lower()
    required = p.required_keywords or []
    matched = [k for k in required if k.lower() in code_lower]
    score = round(len(matched) / max(1, len(required)) * 100, 1) if required else 80.0
    passed = score >= 60.0 or not required
    
    already_passed = db.scalar(select(ProjectSubmission).where(
        ProjectSubmission.user_id == current_user.id,
        ProjectSubmission.project_id == project_id,
        ProjectSubmission.passed.is_(True),
    ))
    xp_result = {}
    if passed and not already_passed:
        xp_result = award_xp(db, current_user.id, p.xp_reward, "project", str(p.id),
                              f"Completed project: {p.title}",
                              f"project:{current_user.id}:{p.id}", tz)
    
    sub = ProjectSubmission(
        user_id=current_user.id, project_id=p.id,
        code=payload.code[:20000], notes=payload.notes,
        completed_milestones=payload.completed_milestones,
        passed=passed, score=score,
        evaluation_report={"matched_keywords": matched, "required_keywords": required, "score": score},
        xp_awarded=xp_result.get("xp_added", 0),
    )
    db.add(sub)
    new_achievements = evaluate_achievements(db, current_user.id, tz)
    db.commit()
    return {"passed": passed, "score": score, "xp_result": xp_result, "evaluation_report": sub.evaluation_report, "new_achievements": new_achievements}
