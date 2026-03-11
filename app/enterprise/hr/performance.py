"""Performance review helpers."""

def review_score(scores:list[float])->float:
    return round(sum(scores)/max(1,len(scores)),2)
