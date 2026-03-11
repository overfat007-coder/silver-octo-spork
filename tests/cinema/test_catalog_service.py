import pytest


def test_catalog_pagination_and_filtering() -> None:
    fastapi_testclient = pytest.importorskip('fastapi.testclient')
    from microservices.cinema.catalog_service import main

    client = fastapi_testclient.TestClient(main.app)
    main.startup()
    r = client.get('/movies', params={'page': 1, 'page_size': 2, 'genre': 'sci-fi'})
    assert r.status_code == 200
    payload = r.json()
    assert payload['page_size'] == 2
    assert payload['total'] >= 1
    assert all(item['genre'] == 'sci-fi' for item in payload['items'])


def test_protected_movies_requires_active_subscription(monkeypatch) -> None:
    fastapi_testclient = pytest.importorskip('fastapi.testclient')
    from microservices.cinema.catalog_service import main

    client = fastapi_testclient.TestClient(main.app)

    monkeypatch.setattr(main, 'is_active_subscription', lambda user_id: False)
    r = client.get('/protected/movies', params={'user_id': 'u2'})
    assert r.status_code == 403
