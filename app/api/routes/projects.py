"""Project endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.common import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Project:
    project = Project(name=payload.name, user_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Project]:
    return db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.id.desc()).all()
