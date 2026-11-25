from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "learnova",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
)


@celery_app.task(name="learnova.recompute_leaderboard_snapshot")
def recompute_leaderboard_snapshot() -> dict:
    return {"status": "ok", "message": "Leaderboard snapshot synchronized"}


@celery_app.task(name="learnova.dispatch_streak_reminder")
def dispatch_streak_reminder(user_id: int) -> dict:
    return {"status": "ok", "user_id": user_id}
