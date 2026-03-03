from app.enterprise.iot.devices import DeviceRegistry
from app.enterprise.iot.telemetry import ingest


def test_iot_registry_and_ingest() -> None:
    reg=DeviceRegistry()
    reg.register('d1','sensor')
    reg.shadow_update('d1',{'temp':23})
    assert reg.devices['d1']['shadow']['temp']==23
    assert ingest([1,2,3])['avg']==2.0
