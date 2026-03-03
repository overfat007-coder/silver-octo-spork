import pytest


def test_enterprise_routes_smoke() -> None:
    fastapi=pytest.importorskip('fastapi')
    testclient=pytest.importorskip('fastapi.testclient')
    from app.api.routes.enterprise import router

    app=fastapi.FastAPI()
    app.include_router(router)
    c=testclient.TestClient(app)
    r=c.post('/enterprise/pm/projects/p1',json={'name':'Demo'})
    assert r.status_code==200
