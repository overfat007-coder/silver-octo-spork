"""Module 21 - Quantum channel simulation APIs."""

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.models.user import User
from app.services.pq_security import pq_handshake_stub
from app.services.quantum_qkd import bb84_simulate

router = APIRouter(prefix="/quantum", tags=["quantum"])


@router.get("/status")
def status(eve: bool = Query(default=False), current_user: User = Depends(get_current_user)) -> dict:
    q = bb84_simulate(64, eve=eve)
    if q["intercept_detected"]:
        fallback = pq_handshake_stub(current_user.id)
        return {"channel": "compromised", "qber": q["qber"], "fallback": fallback["kem"]}
    return {"channel": "ok", **q}
