from app.mega.sec.collector import SecurityCollector
from app.mega.sec.correlation import correlated


def test_sec_collect_and_correlation() -> None:
    c=SecurityCollector()
    c.ingest("fw","login_fail","high")
    c.ingest("fw","login_fail","high")
    assert correlated(c.events,"event_type",2)
