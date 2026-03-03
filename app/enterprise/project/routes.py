"""Routes for PM foundation."""
from fastapi import APIRouter
from app.enterprise.project.core import ProjectService

router=APIRouter(prefix="/enterprise/pm",tags=["enterprise-pm"])
svc=ProjectService()

@router.post("/projects/{project_id}")
def create_project(project_id:str,payload:dict)->dict:
    return svc.create(project_id,payload.get("name",project_id))

@router.post("/projects/{project_id}/tasks")
def add_task(project_id:str,payload:dict)->dict:
    return svc.add_task(project_id,payload.get("task","task"))
