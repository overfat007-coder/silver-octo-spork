"""Knowledge graph operations for task relations and critical path."""

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_relation import TaskRelation


def detect_cycle(db: Session, source: int, target: int) -> bool:
    """Cycle check for depends_on edges by DFS from target to source."""
    stack = [target]
    visited: set[int] = set()
    while stack:
        node = stack.pop()
        if node == source:
            return True
        if node in visited:
            continue
        visited.add(node)
        children = db.query(TaskRelation).filter(TaskRelation.source_task_id == node, TaskRelation.relation_type == "depends_on").all()
        stack.extend([c.target_task_id for c in children])
    return False


def graph_neighbors(db: Session, task_id: int, depth: int = 3) -> list[dict]:
    result = []
    frontier = [(task_id, 0)]
    seen = set()
    while frontier:
        node, d = frontier.pop(0)
        if (node, d) in seen or d > depth:
            continue
        seen.add((node, d))
        rels = db.query(TaskRelation).filter((TaskRelation.source_task_id == node) | (TaskRelation.target_task_id == node)).all()
        for rel in rels:
            nxt = rel.target_task_id if rel.source_task_id == node else rel.source_task_id
            result.append({"from": rel.source_task_id, "to": rel.target_task_id, "type": rel.relation_type})
            frontier.append((nxt, d + 1))
    return result


def critical_path(db: Session, task_id: int) -> dict:
    memo: dict[int, tuple[list[int], int]] = {}

    def dfs(node: int) -> tuple[list[int], int]:
        if node in memo:
            return memo[node]
        outgoing = db.query(TaskRelation).filter(TaskRelation.source_task_id == node, TaskRelation.relation_type == "depends_on").all()
        base_task = db.query(Task).filter(Task.id == node).first()
        base_time = (base_task.estimated_minutes or 0) if base_task else 0
        best_path, best_time = [node], base_time
        for edge in outgoing:
            child_path, child_time = dfs(edge.target_task_id)
            if base_time + child_time > best_time:
                best_time = base_time + child_time
                best_path = [node] + child_path
        memo[node] = (best_path, best_time)
        return memo[node]

    path, total = dfs(task_id)
    return {"task_ids": path, "total_estimated_minutes": total}
