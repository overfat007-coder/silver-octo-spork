"""Composed routes for mega vertical foundations."""
from fastapi import APIRouter
from app.mega.dms.routes import router as dms_router
from app.mega.med.routes import router as med_router
from app.mega.prop.routes import router as prop_router
from app.mega.log.routes import router as log_router
from app.mega.sec.routes import router as sec_router

router=APIRouter(tags=["mega"])
router.include_router(dms_router)
router.include_router(med_router)
router.include_router(prop_router)
router.include_router(log_router)
router.include_router(sec_router)
