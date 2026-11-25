from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.gamification import Achievement, Streak, UserAchievement, UserLevel, XPTransaction
from app.services.gamification import compute_level_info, ensure_user_quests

router = APIRouter()


@router.get("/xp")
def get_xp_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txs = db.scalars(
        select(XPTransaction).where(XPTransaction.user_id == current_user.id).order_by(XPTransaction.created_at.desc()).limit(50)
    ).all()
    return [{"id": t.id, "amount": t.amount, "source_type": t.source_type, "description": t.description,
              "created_at": t.created_at.isoformat()} for t in txs]


@router.get("/level")
def get_level(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lvl = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
    return compute_level_info(lvl.total_xp if lvl else 0)


@router.get("/streak")
def get_streak(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    streak = db.scalar(select(Streak).where(Streak.user_id == current_user.id))
    if not streak:
        return {"current_streak": 0, "longest_streak": 0, "last_active_date": None, "milestone_awarded_days": []}
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_active_date": str(streak.last_active_date) if streak.last_active_date else None,
        "milestone_awarded_days": streak.milestone_awarded_days or [],
    }


@router.get("/achievements")
def get_achievements(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    all_achs = db.scalars(select(Achievement)).all()
    unlocked_ids = set(db.scalars(select(UserAchievement.achievement_id).where(UserAchievement.user_id == current_user.id)).all())
    return [
        {
            "id": a.id, "code": a.code, "title": a.title, "description": a.description,
            "icon_name": a.icon_name, "category": a.category, "xp_reward": a.xp_reward,
            "unlocked": a.id in unlocked_ids,
        }
        for a in all_achs
    ]
