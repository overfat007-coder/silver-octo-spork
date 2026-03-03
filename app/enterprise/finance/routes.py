"""Routes for finance foundation."""
from fastapi import APIRouter, HTTPException
from app.enterprise.finance.accounts import Ledger

router=APIRouter(prefix="/enterprise/finance",tags=["enterprise-finance"])
ledger=Ledger()

@router.post("/accounts/{code}/post/{amount}")
def post(code:str,amount:float)->dict:
    if amount==0:
        raise HTTPException(status_code=400,detail="zero amount")
    return {"code":code,"balance":ledger.post(code,amount)}
