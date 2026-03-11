"""Workflow state transitions for CMS."""

ALLOWED={"draft":{"review"},"review":{"approved","draft"},"approved":{"published"},"published":{"draft"}}

def transit(current:str,target:str)->str:
    if target not in ALLOWED.get(current,set()):
        raise ValueError(f"invalid transition {current}->{target}")
    return target
