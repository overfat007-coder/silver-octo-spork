"""Shipping calculators and labels."""

def shipping_cost(weight_kg:float,zone:str)->float:
    base=5.0 if zone=='local' else 12.0
    return round(base+weight_kg*1.5,2)
