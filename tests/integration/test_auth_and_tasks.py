import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.integration
def test_register_and_login_flow() -> None:
    client = TestClient(app)
    reg = client.post("/api/v1/auth/register", json={"username": "u1", "email": "u1@example.com", "password": "secret123"})
    assert reg.status_code in {201, 422}

    login = client.post("/api/v1/auth/login", json={"login": "u1", "password": "secret123"})
    assert login.status_code == 200
    assert "access_token" in login.json()


@pytest.mark.integration
def test_create_team_task() -> None:
    client = TestClient(app)
    client.post("/api/v1/auth/register", json={"username": "u2", "email": "u2@example.com", "password": "secret123"})
    login = client.post("/api/v1/auth/login", json={"login": "u2", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    team = client.post("/api/v1/teams/", json={"name": "Core"}, headers=headers)
    assert team.status_code == 201
    team_id = team.json()["id"]

    task = client.post("/api/v1/tasks/", json={"title": "Task", "description": "desc", "team_id": team_id}, headers=headers)
    assert task.status_code == 201


@pytest.mark.integration
def test_ai_fallback_with_mock(monkeypatch) -> None:
    from app.services import ai_service

    monkeypatch.setattr(ai_service.settings, "openai_api_key", "x")

    class FakeResp:
        def raise_for_status(self):
            raise RuntimeError("timeout")

    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        module = real_import(name, *args, **kwargs)
        if name == "requests":
            module.post = lambda *a, **k: FakeResp()
        return module

    monkeypatch.setattr(builtins, "__import__", fake_import)
    result = ai_service.enhance_task_with_ai("Срочно", "")
    assert result["priority"] == 5
