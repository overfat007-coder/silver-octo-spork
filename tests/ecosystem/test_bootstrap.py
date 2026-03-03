from app.ecosystem.bootstrap import build_default_registry


def test_bootstrap_has_defaults() -> None:
    reg = build_default_registry()
    assert "serializer:json" in reg.names()
    assert reg.create("store:memory").__class__.__name__ == "MemoryKV"
