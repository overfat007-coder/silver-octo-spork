"""Sync routes."""

from fastapi import APIRouter

from app.mobile.common.store import InMemoryStore
from app.mobile.sync.service import SyncService

router = APIRouter(prefix="/mobile/sync", tags=["mobile-sync"])
_store = InMemoryStore()
_service = SyncService(_store)


@router.post("/apply/{key}")
def apply_sync(key: str, payload: dict) -> dict:
    return _service.apply(key, payload["local"], payload["remote"])
