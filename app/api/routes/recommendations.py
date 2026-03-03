"""Module 22 - GNN recommendation APIs (stub)."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.services.gnn_reco import recommend_assignee_stub, similar_tasks_stub, team_formation_stub

router = APIRouter(prefix="/recommendations", tags=["gnn-reco"])


@router.post("/assignee")
def assignee(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    rid = recommend_assignee_stub(payload.get("title", ""), payload.get("team_members", []))
    return {"requested_by": current_user.id, "recommended_assignee": rid}


@router.get("/tasks/{task_id}")
def similar(task_id: int, current_user: User = Depends(get_current_user)) -> dict:
    return {"requested_by": current_user.id, "task_id": task_id, "similar_tasks": similar_tasks_stub(task_id)}


@router.post("/team")
def team(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    return {"requested_by": current_user.id, "team": team_formation_stub(payload.get("users", []))}
