"""Routes for IoT foundation."""
from fastapi import APIRouter
from app.enterprise.iot.devices import DeviceRegistry

router=APIRouter(prefix="/enterprise/iot",tags=["enterprise-iot"])
svc=DeviceRegistry()

@router.post("/devices/{device_id}")
def register(device_id:str,payload:dict)->dict:
    return svc.register(device_id,payload.get("kind","sensor"))

@router.post("/devices/{device_id}/shadow")
def update_shadow(device_id:str,payload:dict)->dict:
    return svc.shadow_update(device_id,payload)
