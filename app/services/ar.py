"""AR payload generator."""


def build_ar_tasks_payload(user_id: int) -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [37.6173, 55.7558, 1.2]},
                "properties": {
                    "task": "Demo task",
                    "user_id": user_id,
                    "anchor": "desk-surface",
                    "model": "task-card.glb",
                },
            }
        ],
    }
