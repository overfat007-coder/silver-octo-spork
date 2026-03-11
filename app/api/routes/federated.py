"""Module 17 - Federated learning APIs."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.events.bus import bus
from app.models.user import User
from app.services.federated import apply_dp, local_train_stub, secure_aggregate_stub

router = APIRouter(prefix="/federated", tags=["federated"])


@router.post("/local-train")
def local_train(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    samples = payload.get("samples", [])
    grads = local_train_stub(samples)
    private = apply_dp(grads, epsilon=float(payload.get("epsilon", 0.1)))
    bus.publish("federated.update_submitted", {"user_id": current_user.id, "grads": private})
    return {"user_id": current_user.id, "private_gradients": private}


@router.post("/aggregate")
def aggregate(payload: dict, current_user: User = Depends(get_current_user)) -> dict:
    agg = secure_aggregate_stub(payload.get("updates", []))
    return {"aggregated": agg, "requested_by": current_user.id}
