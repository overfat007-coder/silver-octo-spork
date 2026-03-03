"""Team collaboration endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.notification import Notification
from app.models.task import Task
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.schemas.common import TaskRead, TeamCreate, TeamMemberAdd, TeamRoleUpdate
from app.tasks.notifications import send_notification

router = APIRouter(prefix="/teams", tags=["teams"])


def _is_admin(db: Session, team_id: int, user_id: int) -> bool:
    member = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id).first()
    return bool(member and member.role == "admin")


@router.post("/", status_code=201)
def create_team(payload: TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    team = Team(name=payload.name, owner_id=current_user.id)
    db.add(team)
    db.commit()
    db.refresh(team)
    db.add(TeamMember(team_id=team.id, user_id=current_user.id, role="admin"))
    db.commit()
    return {"id": team.id, "name": team.name}


@router.post("/{team_id}/members", status_code=201)
def add_member(team_id: int, payload: TeamMemberAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    if not _is_admin(db, team_id, current_user.id):
        raise HTTPException(status_code=403, detail="Admin role required")

    user = None
    if payload.user_id:
        user = db.query(User).filter(User.id == payload.user_id).first()
    elif payload.email:
        user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    exists = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == user.id).first()
    if exists:
        raise HTTPException(status_code=422, detail="Already member")

    db.add(TeamMember(team_id=team_id, user_id=user.id, role="member"))
    db.add(Notification(user_id=user.id, message=f"Вас добавили в команду #{team_id}"))
    db.commit()
    send_notification.delay(user.id, f"Вас добавили в команду #{team_id}")
    return {"status": "ok"}


@router.delete("/{team_id}/members/{user_id}", status_code=204)
def remove_member(team_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    if not _is_admin(db, team_id, current_user.id):
        raise HTTPException(status_code=403, detail="Admin role required")
    member = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()


@router.patch("/{team_id}/members/{user_id}/role")
def update_role(team_id: int, user_id: int, payload: TeamRoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    if payload.role not in {"admin", "member"}:
        raise HTTPException(status_code=422, detail="Invalid role")
    if not _is_admin(db, team_id, current_user.id):
        raise HTTPException(status_code=403, detail="Admin role required")
    member = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    member.role = payload.role
    db.commit()
    return {"status": "ok"}


@router.get("/{team_id}/tasks", response_model=list[TaskRead])
def team_tasks(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Task]:
    member = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")
    return db.query(Task).filter(Task.team_id == team_id).order_by(Task.created_at.desc()).all()
