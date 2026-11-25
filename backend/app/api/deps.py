"""FastAPI dependency for getting current authenticated user."""
from typing import Optional
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User


def get_current_user(
    access_token: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise creds_exception
    payload = decode_token(access_token)
    if not payload or payload.get("type") != "access":
        raise creds_exception
    user_id = payload.get("sub")
    if not user_id:
        raise creds_exception
    user = db.scalar(select(User).where(User.id == int(user_id), User.is_active.is_(True)))
    if not user:
        raise creds_exception
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def get_user_timezone(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> str:
    from sqlalchemy import select
    from app.models.user import UserProfile
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == current_user.id))
    return profile.timezone if profile else "UTC"
