"""Event bus visibility and pump endpoints."""

from fastapi import APIRouter

from app.events.bus import bus

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/pump")
def pump() -> dict:
    processed = bus.consume_once()
    return {"processed": processed, "queued": len(bus.memory_queue), "dlq": len(bus.dead_letter_queue)}


@router.get("/dlq")
def dlq() -> dict:
    return {"items": bus.dead_letter_queue}
