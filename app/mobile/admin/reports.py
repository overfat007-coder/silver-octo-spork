"""Moderation reports service."""

class ReportService:
    def __init__(self) -> None:
        self._reports: list[dict] = []

    def add(self, reporter: str, target: str, reason: str) -> dict:
        item = {"reporter": reporter, "target": target, "reason": reason}
        self._reports.append(item)
        return item
