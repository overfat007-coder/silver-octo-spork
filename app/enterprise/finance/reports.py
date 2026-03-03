"""Financial reporting helpers."""

def trial_balance(accounts: dict[str,float]) -> float:
    return round(sum(accounts.values()),2)
