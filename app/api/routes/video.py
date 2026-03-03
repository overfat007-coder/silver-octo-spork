"""Module 19 - Video analytics APIs."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.services.video_context import aggregate_activity, fatigue_alert, suggest_tasks_from_objects

router = APIRouter(prefix="/video", tags=["video-analytics"])


@router.post("/activity")
def activity(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    stats = aggregate_activity(payload.get("events", []))
    return {"user_id": current_user.id, "stats": stats}


@router.post("/objects")
def objects(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    suggestions = suggest_tasks_from_objects(payload.get("objects", []))
    return {"user_id": current_user.id, "suggestions": suggestions}


@router.post("/fatigue")
def fatigue(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    alert = fatigue_alert(int(payload.get("blinks_per_min", 0)), bool(payload.get("posture_bad", False)))
    return {"user_id": current_user.id, "fatigue_alert": alert}
