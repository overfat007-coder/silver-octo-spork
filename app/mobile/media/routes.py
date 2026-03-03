"""Media routes."""

from fastapi import APIRouter, HTTPException

from app.mobile.common.store import InMemoryStore
from app.mobile.media.service import MediaService

router = APIRouter(prefix="/mobile/media", tags=["mobile-media"])
_store = InMemoryStore()
_service = MediaService(_store)


@router.post("/upload-meta/{media_id}")
def upload_meta(media_id: str, payload: dict) -> dict:
    try:
        return _service.upload_meta(media_id, payload["filename"], payload["size"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
