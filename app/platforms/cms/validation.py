"""CMS validation rules."""

def validate_entry(schema: dict[str,str], data: dict) -> None:
    missing=[k for k in schema if k not in data]
    if missing:
        raise ValueError(f"missing fields: {missing}")
