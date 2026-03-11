from app.services.hundred_cycle import (
    hundred_complete,
    infinite_self_replicating_task,
    toe_final_equation,
)


def test_infinite_task_is_non_terminating_by_design() -> None:
    task = infinite_self_replicating_task()
    assert task["replicates"] is True
    assert task["completes"] is False


def test_toe_final_contains_all_major_terms() -> None:
    equation = toe_final_equation()
    for term in ["L_tasks", "L_quantum", "L_string", "L_mtheory", "L_loop", "L_twistor"]:
        assert term in equation


def test_hundred_complete_has_final_lines() -> None:
    payload = hundred_complete()
    script = "\n".join(payload["script"])
    assert "OM SHANTI SHANTI SHANTI" in script
    assert "# Запусти снова." in script
