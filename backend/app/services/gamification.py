from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.gamification import (
    Achievement,
    DailyActivity,
    LeaderboardEntry,
    Notification,
    Quest,
    Streak,
    UserAchievement,
    UserLearningAnalytics,
    UserLevel,
    UserQuest,
    XPTransaction,
)
from app.models.learning import CodeSubmission, Lesson, LessonProgress, Module, QuizAttempt
from app.models.project import ProjectSubmission
from app.models.user import UserProfile

LEVEL_THRESHOLDS = [
    (1, 0, "AI Explorer"),
    (2, 150, "Python Apprentice"),
    (3, 400, "Data Enthusiast"),
    (4, 800, "ML Practitioner"),
    (5, 1400, "Neural Architect"),
    (6, 2200, "AI Innovator"),
    (7, 3200, "Generative AI Engineer"),
    (8, 4600, "AI Specialist"),
    (9, 6500, "AI Architect"),
    (10, 9000, "AI Mastermind"),
]

STREAK_MILESTONES = {3: 40, 7: 100, 14: 200, 30: 400, 60: 750, 100: 1500}


def get_zoneinfo(tz_name: str | None) -> ZoneInfo:
    if not tz_name:
        return ZoneInfo("UTC")
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def local_today(tz_name: str | None) -> date:
    return datetime.now(get_zoneinfo(tz_name)).date()


def local_hour(tz_name: str | None) -> int:
    return datetime.now(get_zoneinfo(tz_name)).hour


def get_period_keys(ref_date: date) -> tuple[str, str, str]:
    iso_year, iso_week, _ = ref_date.isocalendar()
    daily_key = ref_date.isoformat()
    weekly_key = f"{iso_year}-W{iso_week:02d}"
    monthly_key = f"{ref_date.year}-{ref_date.month:02d}"
    return daily_key, weekly_key, monthly_key


def compute_level_info(total_xp: int) -> dict[str, Any]:
    current = LEVEL_THRESHOLDS[0]
    next_threshold = LEVEL_THRESHOLDS[1][1]
    for idx, (lvl, threshold, title) in enumerate(LEVEL_THRESHOLDS):
        if total_xp >= threshold:
            current = (lvl, threshold, title)
            next_threshold = LEVEL_THRESHOLDS[idx + 1][1] if idx + 1 < len(LEVEL_THRESHOLDS) else threshold
    lvl, cur_floor, title = current
    is_max = lvl == LEVEL_THRESHOLDS[-1][0]
    span = max(1, next_threshold - cur_floor)
    progress_pct = 100.0 if is_max else min(100.0, round(((total_xp - cur_floor) / span) * 100, 1))
    return {
        "level": lvl,
        "title": title,
        "total_xp": total_xp,
        "current_level_xp": cur_floor,
        "next_level_xp": next_threshold,
        "xp_to_next_level": 0 if is_max else max(0, next_threshold - total_xp),
        "progress_percentage": progress_pct,
        "is_max_level": is_max,
    }


def create_notification(
    db: Session, user_id: int, title: str, message: str, category: str = "system", action_url: str = ""
) -> Notification:
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        category=category,
        action_url=action_url,
    )
    db.add(notif)
    return notif


def _upsert_leaderboard_score(db: Session, user_id: int, period_type: str, period_key: str, delta_xp: int) -> None:
    entry = db.scalar(
        select(LeaderboardEntry).where(
            LeaderboardEntry.user_id == user_id,
            LeaderboardEntry.period_type == period_type,
            LeaderboardEntry.period_key == period_key,
        )
    )
    if entry:
        entry.xp_score += delta_xp
    else:
        db.add(
            LeaderboardEntry(
                user_id=user_id,
                period_type=period_type,
                period_key=period_key,
                xp_score=delta_xp,
            )
        )


def award_xp(
    db: Session,
    user_id: int,
    amount: int,
    source_type: str,
    source_id: str,
    description: str,
    idempotency_key: str,
    timezone_str: str = "UTC",
) -> dict[str, Any]:
    if amount <= 0:
        return {"awarded": False, "xp_added": 0, "leveled_up": False}

    existing = db.scalar(select(XPTransaction).where(XPTransaction.idempotency_key == idempotency_key))
    if existing:
        level_state = db.scalar(select(UserLevel).where(UserLevel.user_id == user_id))
        info = compute_level_info(level_state.total_xp if level_state else 0)
        return {"awarded": False, "xp_added": 0, "leveled_up": False, "level_info": info}

    tx = XPTransaction(
        user_id=user_id,
        amount=amount,
        source_type=source_type,
        source_id=source_id,
        description=description,
        idempotency_key=idempotency_key,
    )
    db.add(tx)

    level_state = db.scalar(select(UserLevel).where(UserLevel.user_id == user_id))
    if not level_state:
        level_state = UserLevel(user_id=user_id, total_xp=0, current_level=1, level_title="AI Explorer")
        db.add(level_state)
        db.flush()

    prev_level = level_state.current_level
    level_state.total_xp += amount
    info = compute_level_info(level_state.total_xp)
    level_state.current_level = info["level"]
    level_state.level_title = info["title"]
    leveled_up = info["level"] > prev_level

    if leveled_up:
        create_notification(
            db,
            user_id,
            f"Level Up! Level {info['level']}: {info['title']}",
            f"Congratulations! You reached {info['total_xp']} XP and unlocked the {info['title']} rank.",
            category="level_up",
            action_url="/dashboard",
        )

    today = local_today(timezone_str)
    _, weekly_key, monthly_key = get_period_keys(today)
    _upsert_leaderboard_score(db, user_id, "global", "all_time", amount)
    _upsert_leaderboard_score(db, user_id, "weekly", weekly_key, amount)
    _upsert_leaderboard_score(db, user_id, "monthly", monthly_key, amount)

    daily = db.scalar(
        select(DailyActivity).where(DailyActivity.user_id == user_id, DailyActivity.activity_date == today)
    )
    if not daily:
        daily = DailyActivity(user_id=user_id, activity_date=today, xp_earned=amount)
        db.add(daily)
    else:
        daily.xp_earned += amount

    increment_quest_progress(db, user_id, "xp_earned", amount, timezone_str)

    return {
        "awarded": True,
        "xp_added": amount,
        "leveled_up": leveled_up,
        "new_level": info["level"] if leveled_up else None,
        "level_info": info,
    }


def record_qualifying_activity(
    db: Session,
    user_id: int,
    timezone_str: str = "UTC",
    lessons_delta: int = 0,
    challenges_delta: int = 0,
    quizzes_delta: int = 0,
    mentor_delta: int = 0,
    minutes_delta: int = 0,
) -> dict[str, Any]:
    today = local_today(timezone_str)
    daily = db.scalar(
        select(DailyActivity).where(DailyActivity.user_id == user_id, DailyActivity.activity_date == today)
    )
    if not daily:
        daily = DailyActivity(user_id=user_id, activity_date=today)
        db.add(daily)

    daily.lessons_completed = (daily.lessons_completed or 0) + lessons_delta
    daily.challenges_solved = (daily.challenges_solved or 0) + challenges_delta
    daily.quizzes_passed = (daily.quizzes_passed or 0) + quizzes_delta
    daily.mentor_questions = (daily.mentor_questions or 0) + mentor_delta
    daily.minutes_learned = (daily.minutes_learned or 0) + minutes_delta

    analytics = db.scalar(select(UserLearningAnalytics).where(UserLearningAnalytics.user_id == user_id))
    if not analytics:
        analytics = UserLearningAnalytics(user_id=user_id, total_learning_minutes=minutes_delta)
        db.add(analytics)
    else:
        analytics.total_learning_minutes += minutes_delta

    streak = db.scalar(select(Streak).where(Streak.user_id == user_id))
    if not streak:
        streak = Streak(user_id=user_id, current_streak=0, longest_streak=0, milestone_awarded_days=[])
        db.add(streak)
        db.flush()

    streak_updated = False
    milestone_bonus = 0
    if streak.last_active_date is None:
        streak.current_streak = 1
        streak.last_active_date = today
        streak_updated = True
    elif streak.last_active_date == today:
        pass
    elif streak.last_active_date == today - timedelta(days=1):
        streak.current_streak += 1
        streak.last_active_date = today
        streak_updated = True
    elif streak.last_active_date == today - timedelta(days=2):
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
        if profile and profile.streak_freezes > 0:
            profile.streak_freezes -= 1
            yesterday = today - timedelta(days=1)
            frozen_day = db.scalar(
                select(DailyActivity).where(DailyActivity.user_id == user_id, DailyActivity.activity_date == yesterday)
            )
            if not frozen_day:
                db.add(DailyActivity(user_id=user_id, activity_date=yesterday, freeze_used=True))
            else:
                frozen_day.freeze_used = True
            streak.current_streak += 1
            streak.last_active_date = today
            streak_updated = True
            create_notification(
                db,
                user_id,
                "Streak Freeze Activated",
                f"A Streak Freeze protected your {streak.current_streak}-day streak!",
                category="streak",
                action_url="/dashboard",
            )
        else:
            streak.current_streak = 1
            streak.last_active_date = today
            streak_updated = True
    else:
        streak.current_streak = 1
        streak.last_active_date = today
        streak_updated = True

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    awarded_milestones = list(streak.milestone_awarded_days or [])
    for days, bonus_xp in STREAK_MILESTONES.items():
        if streak.current_streak >= days and days not in awarded_milestones:
            awarded_milestones.append(days)
            streak.milestone_awarded_days = awarded_milestones
            res = award_xp(
                db,
                user_id,
                bonus_xp,
                "streak_milestone",
                str(days),
                f"{days}-day learning streak milestone bonus",
                f"streak_milestone:{user_id}:{days}",
                timezone_str,
            )
            if res.get("awarded"):
                milestone_bonus += bonus_xp
                create_notification(
                    db,
                    user_id,
                    f"{days}-Day Streak Milestone!",
                    f"You kept your streak alive for {days} days and earned +{bonus_xp} bonus XP.",
                    category="streak",
                    action_url="/dashboard",
                )

    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "streak_updated": streak_updated,
        "milestone_bonus_xp": milestone_bonus,
    }


def ensure_user_quests(db: Session, user_id: int, timezone_str: str = "UTC") -> list[dict[str, Any]]:
    today = local_today(timezone_str)
    daily_key, weekly_key, _ = get_period_keys(today)
    quests = db.scalars(select(Quest).where(Quest.is_active.is_(True))).all()
    results = []
    for q in quests:
        pkey = weekly_key if q.quest_type == "weekly" else daily_key
        uq = db.scalar(
            select(UserQuest).where(
                UserQuest.user_id == user_id,
                UserQuest.quest_id == q.id,
                UserQuest.period_key == pkey,
            )
        )
        if not uq:
            uq = UserQuest(user_id=user_id, quest_id=q.id, period_key=pkey, progress_count=0)
            db.add(uq)
            db.flush()
        results.append(
            {
                "id": q.id,
                "code": q.code,
                "title": q.title,
                "description": q.description,
                "quest_type": q.quest_type,
                "metric_type": q.metric_type,
                "target_count": q.target_count,
                "progress_count": min(uq.progress_count, q.target_count),
                "xp_reward": q.xp_reward,
                "difficulty": q.difficulty,
                "completed": uq.completed,
                "claimed": uq.claimed,
                "period_key": pkey,
            }
        )
    return results


def increment_quest_progress(
    db: Session, user_id: int, metric_type: str, amount: int = 1, timezone_str: str = "UTC"
) -> list[dict[str, Any]]:
    today = local_today(timezone_str)
    daily_key, weekly_key, _ = get_period_keys(today)
    matching = db.scalars(select(Quest).where(Quest.is_active.is_(True), Quest.metric_type == metric_type)).all()
    newly_completed = []
    for q in matching:
        pkey = weekly_key if q.quest_type == "weekly" else daily_key
        uq = db.scalar(
            select(UserQuest).where(
                UserQuest.user_id == user_id,
                UserQuest.quest_id == q.id,
                UserQuest.period_key == pkey,
            )
        )
        if not uq:
            uq = UserQuest(user_id=user_id, quest_id=q.id, period_key=pkey, progress_count=0)
            db.add(uq)
            db.flush()
        if not uq.completed:
            uq.progress_count = min(q.target_count, uq.progress_count + amount)
            if uq.progress_count >= q.target_count:
                uq.completed = True
                newly_completed.append({"id": q.id, "title": q.title, "xp_reward": q.xp_reward})
                create_notification(
                    db,
                    user_id,
                    f"Quest Ready to Claim: {q.title}",
                    f"You completed '{q.title}'. Claim your +{q.xp_reward} XP reward in Quests!",
                    category="quest",
                    action_url="/quests",
                )
    return newly_completed


def claim_quest_reward(db: Session, user_id: int, quest_id: int, timezone_str: str = "UTC") -> dict[str, Any]:
    today = local_today(timezone_str)
    daily_key, weekly_key, _ = get_period_keys(today)
    quest = db.get(Quest, quest_id)
    if not quest:
        raise ValueError("Quest not found")
    pkey = weekly_key if quest.quest_type == "weekly" else daily_key
    uq = db.scalar(
        select(UserQuest).where(
            UserQuest.user_id == user_id,
            UserQuest.quest_id == quest.id,
            UserQuest.period_key == pkey,
        )
    )
    if not uq or not uq.completed:
        raise ValueError("Quest is not yet completed")
    if uq.claimed:
        raise ValueError("Quest reward has already been claimed")

    uq.claimed = True
    uq.claimed_at = datetime.now(timezone.utc)
    xp_res = award_xp(
        db,
        user_id,
        quest.xp_reward,
        "quest",
        f"{quest.id}:{pkey}",
        f"Completed quest: {quest.title}",
        f"quest:{user_id}:{quest.id}:{pkey}",
        timezone_str,
    )
    return {"quest_id": quest.id, "claimed": True, "xp_result": xp_res}


def evaluate_achievements(db: Session, user_id: int, timezone_str: str = "UTC") -> list[dict[str, Any]]:
    achievements = db.scalars(select(Achievement)).all()
    unlocked_ids = set(
        db.scalars(select(UserAchievement.achievement_id).where(UserAchievement.user_id == user_id)).all()
    )
    lessons_done = db.scalar(
        select(func.count(LessonProgress.id)).where(
            LessonProgress.user_id == user_id, LessonProgress.status == "completed"
        )
    ) or 0
    challenges_done = db.scalar(
        select(func.count(func.distinct(CodeSubmission.challenge_id))).where(
            CodeSubmission.user_id == user_id, CodeSubmission.passed.is_(True)
        )
    ) or 0
    perfect_quizzes = db.scalar(
        select(func.count(QuizAttempt.id)).where(
            QuizAttempt.user_id == user_id, QuizAttempt.score_percentage >= 100.0
        )
    ) or 0
    projects_done = db.scalar(
        select(func.count(func.distinct(ProjectSubmission.project_id))).where(
            ProjectSubmission.user_id == user_id, ProjectSubmission.passed.is_(True)
        )
    ) or 0
    level_state = db.scalar(select(UserLevel).where(UserLevel.user_id == user_id))
    total_xp = level_state.total_xp if level_state else 0
    streak_state = db.scalar(select(Streak).where(Streak.user_id == user_id))
    cur_streak = streak_state.current_streak if streak_state else 0
    hr = local_hour(timezone_str)
    is_night = 1 if (hr >= 22 or hr < 5) else 0

    # Check path/module completion counts
    python_lessons_total = db.scalar(
        select(func.count(Lesson.id))
        .join(Module, Lesson.module_id == Module.id)
        .where(Module.path_id == 1)
    ) or 0
    python_lessons_done = db.scalar(
        select(func.count(LessonProgress.id))
        .join(Lesson, LessonProgress.lesson_id == Lesson.id)
        .join(Module, Lesson.module_id == Module.id)
        .where(LessonProgress.user_id == user_id, LessonProgress.status == "completed", Module.path_id == 1)
    ) or 0

    ml_lessons_done = db.scalar(
        select(func.count(LessonProgress.id))
        .join(Lesson, LessonProgress.lesson_id == Lesson.id)
        .join(Module, Lesson.module_id == Module.id)
        .where(LessonProgress.user_id == user_id, LessonProgress.status == "completed", Module.path_id == 3)
    ) or 0

    newly_unlocked = []
    for ach in achievements:
        if ach.id in unlocked_ids:
            continue
        earned = False
        ct = ach.criteria_type
        cv = ach.criteria_value
        if ct == "lessons_completed" and lessons_done >= cv:
            earned = True
        elif ct == "challenges_solved" and challenges_done >= cv:
            earned = True
        elif ct == "streak_days" and cur_streak >= cv:
            earned = True
        elif ct == "perfect_quiz" and perfect_quizzes >= cv:
            earned = True
        elif ct == "projects_completed" and projects_done >= cv:
            earned = True
        elif ct == "total_xp" and total_xp >= cv:
            earned = True
        elif ct == "night_owl" and is_night >= 1 and lessons_done >= 1:
            earned = True
        elif ct == "python_path" and python_lessons_total > 0 and python_lessons_done >= min(cv, python_lessons_total):
            earned = True
        elif ct == "ml_lessons" and ml_lessons_done >= cv:
            earned = True

        if earned:
            db.add(UserAchievement(user_id=user_id, achievement_id=ach.id))
            if ach.xp_reward > 0:
                award_xp(
                    db,
                    user_id,
                    ach.xp_reward,
                    "achievement",
                    ach.code,
                    f"Unlocked achievement: {ach.title}",
                    f"achievement:{user_id}:{ach.code}",
                    timezone_str,
                )
            create_notification(
                db,
                user_id,
                f"Achievement Unlocked: {ach.title}",
                f"{ach.description} (+{ach.xp_reward} XP)",
                category="achievement",
                action_url="/achievements",
            )
            newly_unlocked.append(
                {
                    "code": ach.code,
                    "title": ach.title,
                    "description": ach.description,
                    "icon_name": ach.icon_name,
                    "xp_reward": ach.xp_reward,
                }
            )
    return newly_unlocked
