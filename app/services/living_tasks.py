"""Module 60 - Tasks as life forms simulation."""


def replicate(task_title: str) -> list[str]:
    return [task_title, f"{task_title} copy"]


def mutate(task_title: str) -> str:
    return task_title + "*"


def select(population: list[dict]) -> list[dict]:
    return sorted(population, key=lambda x: x.get("fitness", 0), reverse=True)[:3]
