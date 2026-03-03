from app.services.fungal import glow_intensity
from app.services.reincarnation import reincarnate
from app.services.singularity import consciousness_level


def test_fungal_glow_range() -> None:
    assert 0 <= glow_intensity(42) <= 255


def test_reincarnation_nirvana_at_7() -> None:
    assert reincarnate("x", 7)["nirvana"] is True


def test_consciousness_level_bounds() -> None:
    level = consciousness_level({"automation": 999, "self_reflection": 999})
    assert 0 <= level <= 100
