"""Media validation utilities."""

def validate(filename: str, size: int, max_size: int = 5_000_000) -> None:
    if size > max_size:
        raise ValueError("file too large")
    if "." not in filename:
        raise ValueError("missing extension")
