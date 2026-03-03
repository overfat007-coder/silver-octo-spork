"""Routes for HR foundation."""
from fastapi import APIRouter
from app.enterprise.hr.recruiting import RecruitingService

router=APIRouter(prefix="/enterprise/hr",tags=["enterprise-hr"])
svc=RecruitingService()

@router.post("/candidates/{candidate_id}")
def add_candidate(candidate_id:str,payload:dict)->dict:
    return svc.add_candidate(candidate_id,payload.get("name",candidate_id))

@router.post("/candidates/{candidate_id}/stage/{stage}")
def move_stage(candidate_id:str,stage:str)->dict:
    return svc.move_stage(candidate_id,stage)
