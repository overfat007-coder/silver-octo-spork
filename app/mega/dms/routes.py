"""Routes for DMS foundation."""
from fastapi import APIRouter
from app.mega.dms.core import DmsService

router=APIRouter(prefix="/mega/dms",tags=["mega-dms"])
svc=DmsService()

@router.post("/documents/{doc_id}")
def create_doc(doc_id:str,payload:dict)->dict:
    return svc.create(doc_id,payload.get("title",doc_id),payload.get("type","generic"))
