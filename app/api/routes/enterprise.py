"""Composed routes for enterprise mega foundations."""
from fastapi import APIRouter
from app.enterprise.project.routes import router as pm_router
from app.enterprise.hr.routes import router as hr_router
from app.enterprise.finance.routes import router as fin_router
from app.enterprise.iot.routes import router as iot_router
from app.enterprise.marketing.routes import router as mk_router

router=APIRouter(tags=["enterprise"])
router.include_router(pm_router)
router.include_router(hr_router)
router.include_router(fin_router)
router.include_router(iot_router)
router.include_router(mk_router)
