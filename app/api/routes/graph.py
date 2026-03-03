"""Task knowledge graph endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.task import Task
from app.models.task_relation import TaskRelation
from app.models.user import User
from app.schemas.common import TaskRelationCreate, TaskRelationRead
from app.services.graph import critical_path, detect_cycle, graph_neighbors

router = APIRouter(prefix="/tasks", tags=["graph"])


@router.post("/{task_id}/relations", response_model=TaskRelationRead, status_code=201)
def create_relation(task_id: int, payload: TaskRelationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> TaskRelation:
    source = db.query(Task).filter(Task.id == task_id).first()
    target = db.query(Task).filter(Task.id == payload.target_task_id).first()
    if not source or not target:
        raise HTTPException(status_code=404, detail="Task not found")
    if source.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if payload.relation_type == "depends_on" and detect_cycle(db, task_id, payload.target_task_id):
        raise HTTPException(status_code=409, detail="Cycle detected")

    rel = TaskRelation(source_task_id=task_id, target_task_id=payload.target_task_id, relation_type=payload.relation_type)
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


@router.get("/{task_id}/graph")
def task_graph(task_id: int, depth: int = Query(default=3), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    edges = graph_neighbors(db, task_id, depth)
    return {"task_id": task_id, "depth": depth, "edges": edges}


@router.get("/{task_id}/critical-path")
def task_critical_path(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return critical_path(db, task_id)
