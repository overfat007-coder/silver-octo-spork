from app.mega.med.appointment import AppointmentService


def test_med_appointment() -> None:
    svc=AppointmentService()
    a=svc.book("a1","p1","dr1","2027-01-01T10:00")
    assert a["status"]=="booked"
