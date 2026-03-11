"""Market analytics helpers."""


def price_per_sqm(price:float, area:float)->float:
    return round(price/max(area,0.1),2)
