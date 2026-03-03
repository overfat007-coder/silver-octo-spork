"""Promotion and coupon engine."""

def apply_percent(total:float,percent:float)->float:
    return round(total*(1-max(0.0,min(percent,100.0))/100.0),2)
