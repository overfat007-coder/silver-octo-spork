import pytest


def test_mobile_routes_auth() -> None:
    fastapi = pytest.importorskip("fastapi")
    testclient = pytest.importorskip("fastapi.testclient")
    from app.api.routes.mobile_backend import router

    app = fastapi.FastAPI()
    app.include_router(router)
    client = testclient.TestClient(app)
    response = client.post('/mobile/auth/register', json={'user_id': 'u1', 'email': 'a@b.c', 'password': 'p'})
    assert response.status_code == 200
