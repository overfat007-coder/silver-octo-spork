import pytest


def test_subscription_status_and_update(monkeypatch) -> None:
    fastapi_testclient = pytest.importorskip('fastapi.testclient')
    from microservices.cinema.subscription_service import main

    monkeypatch.setattr(main, 'publish_subscription_event', lambda user_id, active: True)
    client = fastapi_testclient.TestClient(main.app)

    r1 = client.get('/subscriptions/u1/active')
    assert r1.status_code == 200
    assert 'active' in r1.json()

    r2 = client.post('/subscriptions/u9', json={'active': True})
    assert r2.status_code == 200
    assert r2.json()['event_published'] is True
