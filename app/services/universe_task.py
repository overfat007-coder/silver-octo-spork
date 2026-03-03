"""Module 45 - Task universe generation simulation."""


def universe_params(priority: int, due_speed: float, description: str) -> dict:
    return {
        "gravity_constant": priority,
        "speed_of_light": due_speed,
        "laws": description[:120],
    }


def hierarchy(task_id: int, depth: int = 3) -> dict:
    node = {"task_id": task_id, "children": []}
    cur = node
    for i in range(depth):
        child = {"task_id": task_id * 10 + i + 1, "children": []}
        cur["children"].append(child)
        cur = child
    return node
