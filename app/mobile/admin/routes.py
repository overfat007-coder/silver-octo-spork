"""Admin routes."""

from fastapi import APIRouter

from app.mobile.admin.service import AdminService

router = APIRouter(prefix="/mobile/admin", tags=["mobile-admin"])
_service = AdminService()


@router.post("/report")
def report(payload: dict) -> dict:
    return _service.reports.add(payload["reporter"], payload["target"], payload["reason"])
