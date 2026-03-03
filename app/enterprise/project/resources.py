"""Resource planning helpers."""

def allocation(capacity: int, demand: int) -> dict:
    return {"capacity":capacity,"demand":demand,"overload": demand>capacity}
