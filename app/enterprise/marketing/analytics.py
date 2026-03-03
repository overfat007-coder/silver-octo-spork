"""Marketing analytics metrics."""

def conversion_rate(conversions:int, visits:int)->float:
    return round((conversions/max(1,visits))*100,2)
