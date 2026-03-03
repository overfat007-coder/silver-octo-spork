"""Audit verification endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.user import User

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/prove/{task_id}")
def prove_task_chain(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    rows = db.query(TaskHistory).filter(TaskHistory.task_id == task_id).order_by(TaskHistory.id.asc()).all()
    return {"task_id": task_id, "chain": [r.hash_value for r in rows]}


@router.get("/verify/{task_id}/{history_id}")
def verify_history(task_id: int, history_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    row = db.query(TaskHistory).filter(TaskHistory.id == history_id, TaskHistory.task_id == task_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="History not found")
    return {"history_id": row.id, "hash": row.hash_value, "previous_hash": row.previous_hash, "merkle_proof": [row.hash_value]}
