"""Automation rules for telemetry thresholds."""

def threshold_rule(value: float, threshold: float) -> bool:
    return value>=threshold
