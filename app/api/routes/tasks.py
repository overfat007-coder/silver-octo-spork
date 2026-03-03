"""Task endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.notification import Notification
from app.models.project import Project
from app.models.task import Task
from app.models.task_features import TaskFeatures
from app.models.team_member import TeamMember
from app.models.user import User
from app.schemas.common import TaskCreate, TaskRead, TaskUpdate
from app.services.ai_service import enhance_task_with_ai
from app.services.distributed import two_phase_commit_create_task
from app.services.history import add_history
from app.services.ml import build_features, predict_task_metrics
from app.tasks.notifications import send_notification

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Task:
    if payload.project_id:
        project = db.query(Project).filter(Project.id == payload.project_id, Project.user_id == current_user.id).first()
        if not project:
            raise HTTPException(status_code=422, detail="Project is not owned by user")

    if payload.team_id:
        membership = db.query(TeamMember).filter(TeamMember.team_id == payload.team_id, TeamMember.user_id == current_user.id).first()
        if not membership:
            raise HTTPException(status_code=403, detail="Not a team member")

    ai = enhance_task_with_ai(payload.title, payload.description)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    ml_features = build_features(payload.title, payload.description, now, payload.due_date, payload.assignee_id, payload.team_id, ai["priority"])
    ml_prediction = predict_task_metrics(ml_features)

    task = Task(
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        project_id=payload.project_id,
        team_id=payload.team_id,
        assignee_id=payload.assignee_id,
        user_id=current_user.id,
        priority=ai["priority"],
        category=ai["category"],
        estimated_minutes=ai["estimated_minutes"],
        predicted_completion_time=ml_prediction["predicted_completion_time"],
        overdue_probability=ml_prediction["overdue_probability"],
        is_risky=ml_prediction["is_risky"],
    )

    created_ok = two_phase_commit_create_task(
        prepared=[lambda: None],
        committers=[lambda: (db.add(task), db.commit())],
        rollbackers=[lambda: db.rollback()],
    )
    if not created_ok:
        raise HTTPException(status_code=500, detail="Distributed transaction failed")
    db.refresh(task)

    feature_row = TaskFeatures(task_id=task.id, **ml_features, predicted_completion_time=task.predicted_completion_time, overdue_probability=task.overdue_probability)
    db.add(feature_row)
    db.commit()

    add_history(db, task.id, current_user.id, "create", "", f"Task '{task.title}' created")

    if payload.assignee_id:
        message = f"Вам назначена задача: {task.title}"
        db.add(Notification(user_id=payload.assignee_id, message=message))
        db.commit()
        send_notification.delay(payload.assignee_id, message)

    return task


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    project_id: int | None = Query(default=None),
    is_completed: bool | None = Query(default=None),
) -> list[Task]:
    team_ids = [m.team_id for m in db.query(TeamMember).filter(TeamMember.user_id == current_user.id).all()]
    query = db.query(Task).filter((Task.user_id == current_user.id) | (Task.team_id.in_(team_ids)))
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    if is_completed is not None:
        query = query.filter(Task.is_completed == is_completed)
    return query.order_by(Task.created_at.desc()).all()


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    allowed = task.user_id == current_user.id or db.query(TeamMember).filter(TeamMember.team_id == task.team_id, TeamMember.user_id == current_user.id).first()
    if not allowed:
        raise HTTPException(status_code=403, detail="Forbidden")

    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        old = str(getattr(task, k, ""))
        setattr(task, k, v)
        add_history(db, task.id, current_user.id, k, old, str(v))
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    add_history(db, task.id, current_user.id, "delete", task.title, "deleted")
    db.delete(task)
    db.commit()
