from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User
from app.models.gamification import Quest, UserQuest
from app.services.gamification import ensure_user_quests, claim_quest_reward

router = APIRouter()


@router.get("/daily")
def get_daily_quests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), tz: str = Depends(get_user_timezone)):
    quests = ensure_user_quests(db, current_user.id, tz)
    db.commit()
    return [q for q in quests if q["quest_type"] == "daily"]


@router.get("/weekly")
def get_weekly_quests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), tz: str = Depends(get_user_timezone)):
    quests = ensure_user_quests(db, current_user.id, tz)
    db.commit()
    return [q for q in quests if q["quest_type"] == "weekly"]


@router.get("/all")
def get_all_quests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), tz: str = Depends(get_user_timezone)):
    quests = ensure_user_quests(db, current_user.id, tz)
    db.commit()
    return quests


@router.post("/{quest_id}/claim")
def claim_quest(
    quest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    tz: str = Depends(get_user_timezone),
):
    try:
        result = claim_quest_reward(db, current_user.id, quest_id, tz)
        db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))
