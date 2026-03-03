"""Module 49 - Techno-shamanism simulation."""


def call_ancestor(task_id: int) -> dict:
    return {"task_id": task_id, "ancestor": "создатель задачи", "answer": "Я создал её из надежды"}


def drum_to_api(pattern: str) -> str:
    mapping = {
        "бум-бум-така-бум": "GET /tasks",
        "бум-така-така-бум": "POST /tasks",
    }
    return mapping.get(pattern, "GET /tasks")


def project_totem(project_name: str) -> str:
    p = project_name.lower()
    if "баг" in p:
        return "змея"
    if "молоко" in p:
        return "корова"
    return "ворон"
