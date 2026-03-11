"""Routes for proptech foundation."""
from fastapi import APIRouter
from app.mega.prop.property import PropertyService

router=APIRouter(prefix="/mega/prop",tags=["mega-prop"])
svc=PropertyService()

@router.post("/properties/{property_id}")
def put_property(property_id:str,payload:dict)->dict:
    return svc.put(property_id,payload.get("address","n/a"),float(payload.get("price",0)))
