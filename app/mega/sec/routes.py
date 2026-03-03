"""Routes for security foundation."""
from fastapi import APIRouter
from app.mega.sec.collector import SecurityCollector

router=APIRouter(prefix="/mega/sec",tags=["mega-sec"])
svc=SecurityCollector()

@router.post("/events")
def ingest_event(payload:dict)->dict:
    return svc.ingest(payload.get("source","unknown"),payload.get("event_type","generic"),payload.get("severity","low"))
