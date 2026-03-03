from app.ecosystem.registry import PluginRegistry


def test_registry_create() -> None:
    reg = PluginRegistry()
    reg.register("x", lambda: {"ok": True})
    assert reg.names() == ["x"]
    assert reg.create("x") == {"ok": True}
