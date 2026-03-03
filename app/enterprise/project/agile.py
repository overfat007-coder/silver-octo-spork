"""Scrum/Kanban metrics helpers."""

def velocity(done_points: list[int]) -> float:
    return round(sum(done_points)/max(1,len(done_points)),2)

def burndown(total: int, completed: int) -> int:
    return max(0,total-completed)
