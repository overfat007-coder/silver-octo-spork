"""CMS versioning helpers."""

def snapshot(entry: dict) -> dict:
    return {"version": entry["version"], "data": dict(entry["data"]), "status": entry["status"]}
