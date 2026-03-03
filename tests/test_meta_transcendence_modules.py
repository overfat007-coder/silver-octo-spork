from app.services.meta_transcendence import (
    cycle_complete,
    ergodic_time_vs_ensemble,
    settheory_continuum,
)


def test_ergodic_averages_are_close() -> None:
    result = ergodic_time_vs_ensemble()
    assert result["close"] is True


def test_settheory_continuum_mentions_independence() -> None:
    result = settheory_continuum()
    assert result["ch"] == "independent"


def test_cycle_completion_open_ending() -> None:
    result = cycle_complete()
    assert result["completed"] is True
    assert "новое начало" in result["open_ending"]
