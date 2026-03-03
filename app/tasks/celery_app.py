"""Celery app setup."""

from celery import Celery

from app.core.config import settings

celery_app = Celery("smartflow", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "deadline-notifier-hourly": {"task": "app.tasks.notifications.notify_upcoming_deadlines", "schedule": 3600.0},
        "audit-merkle-hourly": {"task": "app.tasks.notifications.build_hourly_merkle_root", "schedule": 3600.0},
        "chaos-monkey": {"task": "app.tasks.notifications.chaos_monkey", "schedule": 600.0},
    },
)
