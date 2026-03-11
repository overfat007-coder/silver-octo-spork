"""Telemetry ingest and aggregate helpers."""

def ingest(points:list[float])->dict:
    return {"count":len(points),"avg": round(sum(points)/max(1,len(points)),3)}
