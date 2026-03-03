from app.mega.dms.core import DmsService
from app.mega.dms.signature import sign_payload, verify_signature


def test_dms_core_and_signature() -> None:
    svc=DmsService()
    doc=svc.create("d1","Doc","contract")
    assert doc["version"]==1
    sig=sign_payload("payload","alice")
    assert verify_signature("payload","alice",sig)
