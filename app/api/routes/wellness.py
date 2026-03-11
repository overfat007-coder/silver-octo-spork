"""Module 20 - Burnout prediction APIs."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.events.bus import bus
from app.models.user import User
from app.services.burnout import burnout_probability_14d, fatigue_index, recommendation

router = APIRouter(prefix="/wellness", tags=["wellness"])


@router.get("/dashboard/{user_id}")
def dashboard(user_id: int, current_user: User = Depends(get_current_user)) -> dict:
    fatigue = fatigue_index(40, 0.1, 3, 1)
    prob = burnout_probability_14d(fatigue)
    if prob > 0.7:
        bus.publish("burnout.detected", {"user_id": user_id, "probability": prob})
    return {
        "requested_by": current_user.id,
        "user_id": user_id,
        "fatigue_index": round(fatigue, 2),
        "burnout_probability_14d": round(prob, 3),
        "recommendation": recommendation(prob),
        "forecast": f"Если темп сохранится, риск выгорания за 14 дней: {round(prob*100)}%",
    }
