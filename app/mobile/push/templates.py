"""Push templates."""

def build_template(event: str, entity_id: str) -> dict:
    return {"title": f"Update: {event}", "body": f"Entity {entity_id} changed"}
