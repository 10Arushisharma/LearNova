from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User, UserProfile
from app.models.gamification import LeaderboardEntry, UserLevel
from app.services.gamification import get_period_keys, local_today

router = APIRouter()


def _board(db: Session, period_type: str, period_key: str, limit: int, offset: int, current_user_id: int):
    entries = db.scalars(
        select(LeaderboardEntry).where(
            LeaderboardEntry.period_type == period_type,
            LeaderboardEntry.period_key == period_key,
        ).order_by(desc(LeaderboardEntry.xp_score)).limit(limit).offset(offset)
    ).all()
    result = []
    for rank, e in enumerate(entries, start=offset + 1):
        user = db.get(User, e.user_id)
        if not user:
            continue
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == e.user_id))
        if profile and not profile.show_on_leaderboard and e.user_id != current_user_id:
            continue
        lvl = db.scalar(select(UserLevel).where(UserLevel.user_id == e.user_id))
        result.append({
            "rank": rank,
            "user_id": e.user_id,
            "username": user.username,
            "full_name": user.full_name,
            "avatar_url": profile.avatar_url if profile else "",
            "xp_score": e.xp_score,
            "level": lvl.current_level if lvl else 1,
            "level_title": lvl.level_title if lvl else "AI Explorer",
            "is_me": e.user_id == current_user_id,
        })
    return result


@router.get("/global")
def global_leaderboard(
    limit: int = Query(20, le=100),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _board(db, "global", "all_time", limit, offset, current_user.id)


@router.get("/weekly")
def weekly_leaderboard(
    limit: int = Query(20, le=100),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = local_today(None)
    _, weekly_key, _ = get_period_keys(today)
    return _board(db, "weekly", weekly_key, limit, offset, current_user.id)


@router.get("/monthly")
def monthly_leaderboard(
    limit: int = Query(20, le=100),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = local_today(None)
    _, _, monthly_key = get_period_keys(today)
    return _board(db, "monthly", monthly_key, limit, offset, current_user.id)
