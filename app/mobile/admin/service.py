"""Admin service facade."""

from app.mobile.admin.reports import ReportService


class AdminService:
    def __init__(self) -> None:
        self.reports = ReportService()
