from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.gamification import Notification

router = APIRouter()


@router.get("")
def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifs = db.scalars(
        select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).limit(50)
    ).all()
    return [{"id": n.id, "title": n.title, "message": n.message, "category": n.category,
              "is_read": n.is_read, "action_url": n.action_url, "created_at": n.created_at.isoformat()} for n in notifs]


@router.patch("/{notif_id}/read")
def mark_read(notif_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.scalar(select(Notification).where(Notification.id == notif_id, Notification.user_id == current_user.id))
    if notif:
        notif.is_read = True
        db.commit()
    return {"detail": "ok"}


@router.patch("/read-all")
def mark_all_read(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifs = db.scalars(
        select(Notification).where(Notification.user_id == current_user.id, Notification.is_read.is_(False))
    ).all()
    for n in notifs:
        n.is_read = True
    db.commit()
    return {"detail": "all marked read"}
