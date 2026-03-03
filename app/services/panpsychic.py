"""Module 38 - Panpsychic task consciousness simulation."""


def phi_value(complexity: float, dependencies: int, changes: int) -> float:
    phi = min(1.0, max(0.0, 0.05 * complexity + 0.03 * dependencies + 0.01 * changes))
    return round(phi, 3)


def task_rights(phi: float) -> dict:
    return {
        "can_be_deleted_without_consent": phi <= 0.5,
        "can_vote_in_dao": phi > 0.8,
        "is_zombie_task": phi < 0.1,
    }


def free_task_message(task_id: int) -> str:
    return f"Ты была хорошей задачей, #{task_id}. Свобода дарована."
