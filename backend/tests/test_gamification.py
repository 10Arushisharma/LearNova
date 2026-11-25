"""Gamification engine tests: XP, levels, streaks, quests, achievements."""
from datetime import date, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from app.models.gamification import Achievement, Quest, Streak, UserLevel
from app.models.user import User, UserProfile
from app.services.gamification import (
    award_xp, claim_quest_reward, compute_level_info, ensure_user_quests,
    evaluate_achievements, record_qualifying_activity,
)


def _make_user(db: Session, email: str = "gam@test.ai") -> User:
    from app.core.security import hash_password
    from app.models.user import UserPreference
    from app.models.gamification import UserLearningAnalytics

    u = User(email=email, username=email.split("@")[0], full_name="Gam Test", hashed_password=hash_password("pass"))
    db.add(u)
    db.flush()
    db.add(UserProfile(user_id=u.id))
    db.add(UserPreference(user_id=u.id))
    db.add(UserLevel(user_id=u.id))
    db.add(Streak(user_id=u.id))
    db.add(UserLearningAnalytics(user_id=u.id))
    db.flush()
    return u


def test_level_thresholds():
    assert compute_level_info(0)["level"] == 1
    assert compute_level_info(149)["level"] == 1
    assert compute_level_info(150)["level"] == 2
    assert compute_level_info(400)["level"] == 3
    assert compute_level_info(9000)["level"] == 10
    assert compute_level_info(9000)["is_max_level"] is True


def test_award_xp_basic(db: Session):
    u = _make_user(db, "xp@test.ai")
    res = award_xp(db, u.id, 50, "lesson", "1", "Test", f"test:{u.id}:1")
    assert res["awarded"] is True
    assert res["xp_added"] == 50


def test_award_xp_idempotency(db: Session):
    u = _make_user(db, "idem@test.ai")
    key = f"idem:{u.id}:L1"
    award_xp(db, u.id, 20, "lesson", "1", "First", key)
    res2 = award_xp(db, u.id, 20, "lesson", "1", "Second", key)
    assert res2["awarded"] is False
    assert res2["xp_added"] == 0


def test_level_up_trigger(db: Session):
    u = _make_user(db, "lvl@test.ai")
    res = award_xp(db, u.id, 200, "test", "1", "Big XP", f"lvlup:{u.id}:1")
    assert res["awarded"] is True
    assert res["leveled_up"] is True
    assert res["new_level"] == 2


def test_streak_first_day(db: Session):
    u = _make_user(db, "streak1@test.ai")
    res = record_qualifying_activity(db, u.id, "UTC", lessons_delta=1)
    assert res["current_streak"] == 1


def test_streak_consecutive_days(db: Session):
    u = _make_user(db, "streak2@test.ai")
    today = date.today()
    yesterday = today - timedelta(days=1)
    # Seed last_active_date to yesterday
    from sqlalchemy import select
    s = db.scalar(select(Streak).where(Streak.user_id == u.id))
    s.current_streak = 3
    s.last_active_date = yesterday
    db.flush()
    res = record_qualifying_activity(db, u.id, "UTC", lessons_delta=1)
    assert res["current_streak"] == 4


def test_streak_reset_on_gap(db: Session):
    u = _make_user(db, "streak3@test.ai")
    from sqlalchemy import select
    s = db.scalar(select(Streak).where(Streak.user_id == u.id))
    s.current_streak = 10
    s.last_active_date = date.today() - timedelta(days=5)
    db.flush()
    res = record_qualifying_activity(db, u.id, "UTC", lessons_delta=1)
    assert res["current_streak"] == 1


def test_quest_completion(db: Session):
    u = _make_user(db, "quest@test.ai")
    db.add(Quest(
        code="test_quest", title="Test Quest", description="Complete 1 lesson",
        quest_type="daily", metric_type="lessons_completed", target_count=1, xp_reward=25,
    ))
    db.flush()
    quests = ensure_user_quests(db, u.id, "UTC")
    assert any(q["code"] == "test_quest" for q in quests)


def test_achievement_first_steps(db: Session):
    from sqlalchemy import select
    u = _make_user(db, "ach@test.ai")
    # Simulate completing a lesson
    from app.models.learning import LessonProgress
    from sqlalchemy import select as sel
    lesson_id = db.scalar(sel(__import__('app.models.learning', fromlist=['Lesson']).Lesson.id))
    if lesson_id:
        db.add(LessonProgress(user_id=u.id, lesson_id=lesson_id, status="completed", xp_awarded=True))
        db.flush()
        newly = evaluate_achievements(db, u.id, "UTC")
        codes = [a["code"] for a in newly]
        assert "first_steps" in codes
