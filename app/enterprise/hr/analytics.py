"""HR analytics helpers."""

def turnover_rate(leavers:int, avg_headcount:int)->float:
    return round((leavers/max(1,avg_headcount))*100,2)
