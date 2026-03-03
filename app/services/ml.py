"""ML inference and feature extraction."""

from datetime import datetime


def build_features(title: str, description: str, created_at: datetime, due_date, assignee_id, team_id, priority: int) -> dict:
    return {
        "title_length": len(title),
        "description_length": len(description or ""),
        "hour_of_day_created": created_at.hour,
        "day_of_week_created": created_at.weekday(),
        "has_due_date": bool(due_date),
        "assignee_id": assignee_id,
        "team_id": team_id,
        "priority": priority,
    }


def predict_task_metrics(features: dict) -> dict:
    """Heuristic placeholder for real model.pkl loading."""
    score = features["priority"] * 30 + features["description_length"] // 15
    overdue_probability = min(0.95, 0.25 + features["priority"] * 0.1)
    return {
        "predicted_completion_time": max(15, score),
        "overdue_probability": overdue_probability,
        "is_risky": overdue_probability >= 0.6,
    }
