"""Module 62 - Journey to task core simulation."""


def standard_model() -> dict:
    return {
        "leptons": ["created_at", "updated_at"],
        "bosons": ["notifications"],
        "higgs": "priority",
    }


def core_singularity(task_id: int) -> dict:
    return {"task_id": task_id, "event_horizon": True, "info_paradox": True}
