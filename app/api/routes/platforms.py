"""Composed routes for CMS, e-commerce, and LMS platform foundations."""
from fastapi import APIRouter
from app.platforms.cms.routes import router as cms_router
from app.platforms.ecommerce.routes import router as ecom_router
from app.platforms.lms.routes import router as lms_router

router=APIRouter(tags=['platforms'])
router.include_router(cms_router)
router.include_router(ecom_router)
router.include_router(lms_router)
