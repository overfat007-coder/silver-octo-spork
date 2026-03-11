"""A/B experiment control endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.common import ExperimentStartRequest

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/start")
def start_experiment(payload: ExperimentStartRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    bucket = "A" if current_user.id % 2 == 0 else "B"
    return {"experiment": payload.name, "bucket": bucket, "show_ml_predictions": bucket == "A"}
