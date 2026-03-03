import pytest

from app.mobile.common.store import InMemoryStore
from app.mobile.media.service import MediaService


def test_media_upload_meta() -> None:
    svc = MediaService(InMemoryStore())
    out = svc.upload_meta("m1", "a.png", 100)
    assert out["filename"] == "a.png"


def test_media_invalid() -> None:
    svc = MediaService(InMemoryStore())
    with pytest.raises(ValueError):
        svc.upload_meta("m1", "invalid", 100)
