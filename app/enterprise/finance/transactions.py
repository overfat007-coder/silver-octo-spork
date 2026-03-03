"""Double-entry transaction helpers."""

def double_entry(debit: float, credit: float) -> bool:
    return round(debit,2)==round(credit,2)
