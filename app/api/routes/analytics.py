"""Analytics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.common import ProductivityAnalytics
from app.services.analytics import build_productivity_stats

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/productivity", response_model=ProductivityAnalytics)
def productivity(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return build_productivity_stats(db, current_user.id)
