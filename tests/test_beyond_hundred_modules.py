from app.services.beyond_hundred import (
    complexity_p_vs_np,
    transfinite_continuum_hypothesis,
    transfinite_aleph,
)


def test_transfinite_aleph_symbolic() -> None:
    result = transfinite_aleph(3)
    assert result["aleph"] == "ℵ_3"


def test_ch_independence_message() -> None:
    assert "ZFC" in transfinite_continuum_hypothesis()["answer"]


def test_complexity_phrase() -> None:
    assert "P ≠ NP" in complexity_p_vs_np()["statement"]
