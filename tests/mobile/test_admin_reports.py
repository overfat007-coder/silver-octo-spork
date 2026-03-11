from app.mobile.admin.service import AdminService


def test_admin_report_create() -> None:
    svc = AdminService()
    out = svc.reports.add("u1", "u2", "spam")
    assert out["reason"] == "spam"
