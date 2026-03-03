"""GNN recommendation stubs for heterogeneous graph."""


def recommend_assignee_stub(task_title: str, team_members: list[int]) -> int | None:
    if not team_members:
        return None
    return team_members[len(task_title) % len(team_members)]


def similar_tasks_stub(task_id: int) -> list[int]:
    return [task_id + 1, task_id + 2, task_id + 3]


def team_formation_stub(users: list[int]) -> list[int]:
    return users[:3]
