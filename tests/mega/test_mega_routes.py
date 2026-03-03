import pytest


def test_mega_routes_smoke() -> None:
    fastapi=pytest.importorskip("fastapi")
    testclient=pytest.importorskip("fastapi.testclient")
    from app.api.routes.mega import router

    app=fastapi.FastAPI()
    app.include_router(router)
    c=testclient.TestClient(app)
    r=c.post("/mega/dms/documents/d1",json={"title":"A","type":"contract"})
    assert r.status_code==200
