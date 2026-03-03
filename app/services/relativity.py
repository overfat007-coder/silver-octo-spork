"""Module 26 - Relativistic time correction simulation."""

from datetime import datetime, timedelta

C = 299_792_458
G = 9.80665


def gravity(lat: float, lon: float, alt: float) -> float:
    base = 9.780327
    return max(9.5, base - alt * 3e-6)


def due_date_with_relativity(due_date: datetime, speed_kmh: float, alt_m: float) -> datetime:
    v = speed_kmh / 3.6
    gamma = 1 - (v * v) / (2 * C * C)
    grav = 1 + (G * alt_m) / (C * C)
    factor = gamma * grav
    delta = (factor - 1) * 3600
    return due_date + timedelta(seconds=delta)


def earth_to_mars_time(dt: datetime) -> str:
    # lightweight MSD-like placeholder
    return f"MSD-{int(dt.timestamp() / 88775)}"
