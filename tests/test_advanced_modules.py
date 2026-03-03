from app.services.neuromorphic import energy_saved_joules
from app.services.psychohistory import system_state
from app.services.quantum_qkd import bb84_simulate


def test_qkd_simulation_shape() -> None:
    result = bb84_simulate(32, eve=False)
    assert "qber" in result and "intercept_detected" in result


def test_psychohistory_phase() -> None:
    phase = system_state(3, 10, 100, 1.0)
    assert phase["phase"] in {"solid", "liquid", "gas"}


def test_neuromorphic_energy_non_negative() -> None:
    assert energy_saved_joules(100000, 5000) >= 0
