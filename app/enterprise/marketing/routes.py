"""Routes for marketing foundation."""
from fastapi import APIRouter
from app.enterprise.marketing.contacts import ContactService

router=APIRouter(prefix="/enterprise/marketing",tags=["enterprise-marketing"])
svc=ContactService()

@router.post("/contacts/{contact_id}")
def upsert(contact_id:str,payload:dict)->dict:
    return svc.upsert(contact_id,payload.get("email","n/a"))
