"""Event correlation helpers."""


def correlated(events:list[dict], key:str, min_count:int=2)->bool:
    values=[e.get(key) for e in events]
    return any(values.count(v)>=min_count for v in set(values) if v is not None)
