from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_user_timezone
from app.db.session import get_db
from app.models.user import User, UserProfile, UserPreference
from app.models.gamification import DailyActivity, Streak, UserLevel, UserLearningAnalytics, XPTransaction
from app.models.learning import LessonProgress, CodeSubmission
from app.services.gamification import compute_level_info
from datetime import date, timedelta

router = APIRouter()


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    timezone: str | None = None
    public_profile: bool | None = None
    show_on_leaderboard: bool | None = None
    github_url: str | None = None
    avatar_url: str | None = None


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == current_user.id))
    prefs = db.scalar(select(UserPreference).where(UserPreference.user_id == current_user.id))
    level_state = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
    streak = db.scalar(select(Streak).where(Streak.user_id == current_user.id))
    level_info = compute_level_info(level_state.total_xp if level_state else 0)
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "onboarding_completed": current_user.onboarding_completed,
        "profile": {
            "avatar_url": profile.avatar_url if profile else "",
            "bio": profile.bio if profile else "",
            "timezone": profile.timezone if profile else "UTC",
            "public_profile": profile.public_profile if profile else True,
            "show_on_leaderboard": profile.show_on_leaderboard if profile else True,
            "github_url": profile.github_url if profile else "",
            "streak_freezes": profile.streak_freezes if profile else 2,
        },
        "preferences": {
            "experience_level": prefs.experience_level if prefs else "complete_beginner",
            "interests": prefs.interests if prefs else [],
            "learning_goal": prefs.learning_goal if prefs else "",
            "daily_minutes_goal": prefs.daily_minutes_goal if prefs else 30,
            "recommended_path_slug": prefs.recommended_path_slug if prefs else "python-foundations",
        },
        "level_info": level_info,
        "streak": {
            "current_streak": streak.current_streak if streak else 0,
            "longest_streak": streak.longest_streak if streak else 0,
            "last_active_date": str(streak.last_active_date) if streak and streak.last_active_date else None,
        },
    }


@router.patch("/me")
def update_me(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.full_name:
        current_user.full_name = payload.full_name
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == current_user.id))
    if profile:
        for field in ["bio", "timezone", "public_profile", "show_on_leaderboard", "github_url", "avatar_url"]:
            val = getattr(payload, field)
            if val is not None:
                setattr(profile, field, val)
    db.commit()
    return {"detail": "Profile updated"}


@router.get("/me/stats")
def get_my_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), tz: str = Depends(get_user_timezone)):
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    lessons_done = db.scalar(
        select(func.count(LessonProgress.id)).where(
            LessonProgress.user_id == current_user.id, LessonProgress.status == "completed"
        )
    ) or 0
    challenges_done = db.scalar(
        select(func.count(func.distinct(CodeSubmission.challenge_id))).where(
            CodeSubmission.user_id == current_user.id, CodeSubmission.passed.is_(True)
        )
    ) or 0
    
    weekly = db.scalars(
        select(DailyActivity).where(
            DailyActivity.user_id == current_user.id,
            DailyActivity.activity_date >= week_ago,
        )
    ).all()
    
    analytics = db.scalar(select(UserLearningAnalytics).where(UserLearningAnalytics.user_id == current_user.id))
    level_state = db.scalar(select(UserLevel).where(UserLevel.user_id == current_user.id))
    streak = db.scalar(select(Streak).where(Streak.user_id == current_user.id))
    
    return {
        "lessons_completed": lessons_done,
        "challenges_solved": challenges_done,
        "total_learning_minutes": analytics.total_learning_minutes if analytics else 0,
        "avg_quiz_score": analytics.avg_quiz_score if analytics else 0.0,
        "total_xp": level_state.total_xp if level_state else 0,
        "current_streak": streak.current_streak if streak else 0,
        "longest_streak": streak.longest_streak if streak else 0,
        "weekly_activity": [
            {
                "date": str(a.activity_date),
                "xp_earned": a.xp_earned,
                "lessons_completed": a.lessons_completed,
                "challenges_solved": a.challenges_solved,
                "minutes_learned": a.minutes_learned,
            }
            for a in sorted(weekly, key=lambda x: x.activity_date)
        ],
    }
