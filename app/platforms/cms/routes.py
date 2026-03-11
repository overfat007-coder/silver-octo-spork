"""FastAPI routes for CMS foundation."""
from fastapi import APIRouter, HTTPException
from app.platforms.cms.service import CmsService

router=APIRouter(prefix='/platform/cms',tags=['platform-cms'])
svc=CmsService()

@router.post('/types/{name}')
def create_type(name:str,payload:dict)->dict:
    ct=svc.register_type(name,payload.get('fields',{}))
    return {'name':ct.name,'fields':ct.fields}

@router.post('/entries/{entry_id}')
def create_entry(entry_id:str,payload:dict)->dict:
    try:
        e=svc.create_entry(entry_id,payload['type_name'],payload.get('data',{}))
    except (KeyError,ValueError) as exc:
        raise HTTPException(status_code=400,detail=str(exc)) from exc
    return {'entry_id':e.entry_id,'version':e.version,'status':e.status}
