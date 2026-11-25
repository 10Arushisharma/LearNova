"""Auth router: register, login, logout, refresh, forgot/reset password."""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, create_password_reset_token,
    decode_token, hash_token,
)
from app.db.session import get_db
from app.models.user import User, UserProfile, UserPreference, RefreshToken, PasswordResetToken
from app.models.gamification import UserLevel, Streak, UserLearningAnalytics

router = APIRouter()

COOKIE_OPTS = dict(
    httponly=True,
    secure=settings.COOKIE_SECURE,
    samesite=settings.COOKIE_SAMESITE,
    path="/",
)


# ── Schemas ──────────────────────────────────────────────────────────────────

class RegisterIn(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str
    new_password: str


class OnboardingIn(BaseModel):
    experience_level: str
    interests: list[str]
    learning_goal: str
    daily_minutes: int


# ── Helpers ───────────────────────────────────────────────────────────────────

def _set_auth_cookies(response: Response, user: User) -> None:
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    response.set_cookie("access_token", access, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, **COOKIE_OPTS)
    response.set_cookie("refresh_token", refresh, max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, **COOKIE_OPTS)


def _revoke_refresh_tokens(db: Session, user_id: int) -> None:
    tokens = db.scalars(
        select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
    ).all()
    for t in tokens:
        t.revoked = True
    db.commit()


def _guess_path(interests: list[str], experience_level: str) -> str:
    if "python" in [i.lower() for i in interests] or experience_level == "complete_beginner":
        return "python-foundations"
    if any(x in [i.lower() for i in interests] for x in ["machine learning", "ml"]):
        return "machine-learning"
    if any(x in [i.lower() for i in interests] for x in ["data science", "data"]):
        return "data-science"
    if any(x in [i.lower() for i in interests] for x in ["deep learning"]):
        return "deep-learning"
    if any(x in [i.lower() for i in interests] for x in ["generative ai", "llm"]):
        return "generative-ai"
    if any(x in [i.lower() for i in interests] for x in ["ai engineering"]):
        return "ai-engineering"
    return "python-foundations"


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, response: Response, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(400, "Email already registered")
    if db.scalar(select(User).where(User.username == payload.username)):
        raise HTTPException(400, "Username already taken")
    if len(payload.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.flush()
    db.add(UserProfile(user_id=user.id))
    db.add(UserPreference(user_id=user.id))
    db.add(UserLevel(user_id=user.id))
    db.add(Streak(user_id=user.id))
    db.add(UserLearningAnalytics(user_id=user.id))
    db.commit()
    db.refresh(user)
    _set_auth_cookies(response, user)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "onboarding_completed": user.onboarding_completed,
    }


@router.post("/login")
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email, User.is_active.is_(True)))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    _set_auth_cookies(response, user)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "onboarding_completed": user.onboarding_completed,
        "role": user.role,
    }


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    if refresh_token:
        payload = decode_token(refresh_token)
        if payload:
            _revoke_refresh_tokens(db, int(payload.get("sub", 0)))
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"detail": "Logged out"}


@router.post("/refresh")
def refresh(response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(401, "No refresh token")
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")
    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401, "User not found")
    _set_auth_cookies(response, user)
    return {"detail": "Tokens refreshed"}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    # Always return success to prevent email enumeration
    if user:
        raw_token = create_password_reset_token(payload.email)
        db.add(PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(raw_token),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES),
        ))
        db.commit()
        # In production, send this via email. Returned here for dev convenience.
        return {"detail": "Password reset email sent", "dev_token": raw_token}
    return {"detail": "Password reset email sent"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    token_data = decode_token(payload.token)
    if not token_data or token_data.get("type") != "reset":
        raise HTTPException(400, "Invalid or expired reset token")
    record = db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == hash_token(payload.token),
            PasswordResetToken.used.is_(False),
        )
    )
    if not record:
        raise HTTPException(400, "Reset token already used or not found")
    if len(payload.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    user = db.get(User, record.user_id)
    user.hashed_password = hash_password(payload.new_password)
    record.used = True
    db.commit()
    return {"detail": "Password reset successful"}


@router.post("/onboarding")
def complete_onboarding(
    payload: OnboardingIn,
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    from app.core.security import decode_token as dt
    if not access_token:
        raise HTTPException(401, "Not authenticated")
    tok = dt(access_token)
    if not tok:
        raise HTTPException(401, "Invalid token")
    user = db.get(User, int(tok["sub"]))
    pref = db.scalar(select(UserPreference).where(UserPreference.user_id == user.id))
    if not pref:
        pref = UserPreference(user_id=user.id)
        db.add(pref)
    pref.experience_level = payload.experience_level
    pref.interests = payload.interests
    pref.learning_goal = payload.learning_goal
    pref.daily_minutes_goal = payload.daily_minutes
    pref.recommended_path_slug = _guess_path(payload.interests, payload.experience_level)
    user.onboarding_completed = True
    db.commit()
    return {
        "recommended_path": pref.recommended_path_slug,
        "daily_goal_minutes": pref.daily_minutes_goal,
    }
