"""Routes for logistics foundation."""
from fastapi import APIRouter
from app.mega.log.fleet import FleetService

router=APIRouter(prefix="/mega/log",tags=["mega-log"])
svc=FleetService()

@router.post("/vehicles/{vehicle_id}")
def add_vehicle(vehicle_id:str,payload:dict)->dict:
    return svc.add_vehicle(vehicle_id,float(payload.get("capacity_kg",0)))
