"""Productivity analytics service."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.task import Task


def build_productivity_stats(db: Session, user_id: int) -> dict:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)

    completed_week = db.query(Task).filter(Task.user_id == user_id, Task.is_completed.is_(True), Task.created_at >= week_start).count()
    completed_month = db.query(Task).filter(Task.user_id == user_id, Task.is_completed.is_(True), Task.created_at >= month_start).count()

    by_category: dict[str, int] = {}
    for category, count in db.query(Task.category, Task.id).filter(Task.user_id == user_id).all():
        key = category or "Без категории"
        by_category[key] = by_category.get(key, 0) + 1

    total_estimated = sum(
        t.estimated_minutes or 0
        for t in db.query(Task).filter(Task.user_id == user_id, Task.is_completed.is_(False)).all()
    )

    return {
        "completed_week": completed_week,
        "completed_month": completed_month,
        "by_category": by_category,
        "total_estimated_minutes_open": total_estimated,
    }
