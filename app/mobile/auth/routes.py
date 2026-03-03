"""FastAPI routes for mobile auth."""

from fastapi import APIRouter, HTTPException

from app.mobile.auth.service import AuthService
from app.mobile.common.store import InMemoryStore

router = APIRouter(prefix="/mobile/auth", tags=["mobile-auth"])
_store = InMemoryStore()
_service = AuthService(_store)


@router.post("/register")
def register(payload: dict) -> dict:
    user = _service.register(payload["user_id"], payload["email"], payload["password"])
    return {"user_id": user.user_id, "email": user.email}


@router.post("/login")
def login(payload: dict) -> dict:
    token = _service.login(payload["email"], payload["password"])
    if not token:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"access_token": token}
