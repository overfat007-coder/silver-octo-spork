"""Module 51 - Infinite creator regress simulation."""


def regress(n: int) -> list[str]:
    return [f"creator_level_{i}" for i in range(1, max(1, n) + 1)]


def turtles(count: int = 10) -> list[str]:
    return ["turtle" for _ in range(count)]


def base_case() -> str:
    return "Базового случая нет. Только черепахи."
