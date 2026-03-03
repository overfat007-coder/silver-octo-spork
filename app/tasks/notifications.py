"""Background tasks for notifications, audit and chaos routines."""

import hashlib
import random
from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.models.audit_root import AuditRoot
from app.models.notification import Notification
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.tasks.celery_app import celery_app


@celery_app.task
def send_notification(user_id: int, message: str) -> None:
    db = SessionLocal()
    try:
        db.add(Notification(user_id=user_id, message=message))
        db.commit()
    finally:
        db.close()


@celery_app.task
def notify_upcoming_deadlines() -> None:
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        upper = now + timedelta(hours=1)
        tasks = db.query(Task).filter(Task.due_date >= now, Task.due_date <= upper, Task.is_completed.is_(False)).all()
        for task in tasks:
            if task.assignee_id:
                db.add(Notification(user_id=task.assignee_id, message=f"Скоро дедлайн задачи: {task.title}"))
        db.commit()
    finally:
        db.close()


@celery_app.task
def build_hourly_merkle_root() -> str:
    db = SessionLocal()
    try:
        end = datetime.now(timezone.utc).replace(tzinfo=None)
        start = end - timedelta(hours=1)
        rows = db.query(TaskHistory).filter(TaskHistory.timestamp >= start, TaskHistory.timestamp <= end).order_by(TaskHistory.id.asc()).all()
        hashes = [r.hash_value for r in rows] or ["EMPTY"]
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            hashes = [hashlib.sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest() for i in range(0, len(hashes), 2)]
        root = hashes[0]
        db.add(AuditRoot(root_hash=root, period_start=start, period_end=end))
        db.commit()
        return root
    finally:
        db.close()


@celery_app.task
def chaos_monkey() -> dict:
    targets = ["db", "redis", "ai_api"]
    victim = random.choice(targets)
    return {"event": "chaos_simulated", "target": victim, "mode": "degraded"}
