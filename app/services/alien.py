"""Module 35 - Alien communication protocol simulation."""


def broadcast_format(tasks: list[dict]) -> dict:
    fib = [1, 1, 2, 3, 5, 8, 13]
    return {"marker_primes": [2, 3, 5, 7, 11], "fibonacci": fib, "tasks": tasks[:100]}


def decode_signal(signal: str) -> dict:
    if "DNA" in signal.upper():
        return {"intent": "request_samples", "task": "Подготовить образцы ДНК"}
    return {"intent": "unknown", "task": "Анализировать сигнал"}
