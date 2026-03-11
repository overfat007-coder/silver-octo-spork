from app.mega.log.fleet import FleetService
from app.mega.log.route import eta


def test_log_fleet_and_eta() -> None:
    svc=FleetService()
    svc.add_vehicle("v1",1500)
    assert svc.vehicles["v1"]["capacity_kg"]==1500
    assert eta(120,60)==2.0
