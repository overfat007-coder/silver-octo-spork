import pytest


def test_platforms_routes_smoke() -> None:
    fastapi = pytest.importorskip('fastapi')
    testclient = pytest.importorskip('fastapi.testclient')
    from app.api.routes.platforms import router

    app=fastapi.FastAPI()
    app.include_router(router)
    c=testclient.TestClient(app)
    r=c.post('/platform/cms/types/article',json={'fields':{'title':'text'}})
    assert r.status_code==200
