"""Route planning helpers."""


def eta(distance_km:float,speed_kmh:float)->float:
    return round(distance_km/max(speed_kmh,1),2)
