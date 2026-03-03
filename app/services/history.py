"""Task history and audit hashing helpers."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.task_history import TaskHistory
from app.services.audit_utils import chain_hash


def add_history(db: Session, task_id: int, user_id: int, field: str, old: str, new: str) -> TaskHistory:
    prev = db.query(TaskHistory).filter(TaskHistory.task_id == task_id).order_by(TaskHistory.id.desc()).first()
    previous_hash = prev.hash_value if prev else "GENESIS"
    ts = datetime.now(timezone.utc).replace(tzinfo=None)
    hash_value = chain_hash(previous_hash, ts, user_id, field, new)
    row = TaskHistory(
        task_id=task_id,
        user_id=user_id,
        field_changed=field,
        old_value=old,
        new_value=new,
        previous_hash=previous_hash,
        hash_value=hash_value,
        timestamp=ts,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
