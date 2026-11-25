from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.models.gamification import UserLevel, XPTransaction
from app.models.learning import LessonProgress, CodeSubmission, QuizAttempt

router = APIRouter()


@router.get("/users")
def admin_list_users(
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    users = db.scalars(select(User).offset(offset).limit(limit)).all()
    total = db.scalar(select(func.count(User.id)))
    return {
        "total": total,
        "users": [{"id": u.id, "email": u.email, "username": u.username, "role": u.role,
                    "is_active": u.is_active, "created_at": u.created_at.isoformat()} for u in users],
    }


@router.get("/stats")
def admin_platform_stats(db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    total_users = db.scalar(select(func.count(User.id))) or 0
    total_lessons = db.scalar(select(func.count(LessonProgress.id)).where(LessonProgress.status == "completed")) or 0
    total_submissions = db.scalar(select(func.count(CodeSubmission.id))) or 0
    total_xp = db.scalar(select(func.sum(XPTransaction.amount))) or 0
    quiz_attempts = db.scalar(select(func.count(QuizAttempt.id))) or 0
    return {
        "total_users": total_users,
        "lessons_completed_total": total_lessons,
        "code_submissions_total": total_submissions,
        "xp_awarded_total": total_xp,
        "quiz_attempts_total": quiz_attempts,
    }


@router.patch("/users/{user_id}/toggle-active")
def toggle_user_active(user_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"user_id": user.id, "is_active": user.is_active}
