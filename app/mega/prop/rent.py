"""Renting operations."""


def rent_yield(monthly_rent:float, property_price:float)->float:
    return round((monthly_rent*12/max(property_price,1))*100,2)
