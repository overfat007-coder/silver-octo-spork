from tools.elevator_sim.engine import ElevatorEngine, ElevatorState


def step_many(engine: ElevatorEngine, steps: int = 1200, dt: float = 0.02) -> None:
    for _ in range(steps):
        engine.step(dt)


def test_fsm_reaches_open_state_after_request() -> None:
    engine = ElevatorEngine()
    engine.request_inside(3)
    step_many(engine)
    assert engine.current_floor == 3
    assert engine.state in {ElevatorState.STOIT_OTKRYT, ElevatorState.STOIT_ZAKRYT}


def test_scheduler_prefers_same_direction() -> None:
    engine = ElevatorEngine()
    engine.request_inside(6)
    engine.request_inside(2)
    assert engine.next_target() == 2

    # Move cabin to floor 4 and continue upward: should keep serving upward first
    engine.position_m = engine.floor_to_position(4)
    engine.velocity_m_s = 0.5
    assert engine.next_target() == 6


def test_emergency_state_stops_elevator() -> None:
    engine = ElevatorEngine()
    engine.request_inside(9)
    step_many(engine, 100)
    engine.set_emergency(True)
    assert engine.state == ElevatorState.AVARIYA
    v = engine.velocity_m_s
    step_many(engine, 50)
    assert engine.velocity_m_s == v == 0.0
