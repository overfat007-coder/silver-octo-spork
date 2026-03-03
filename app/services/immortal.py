"""Module 36 - Digital immortality simulation."""


def avatar_reply(message: str) -> str:
    return f"Я цифровой аватар и думаю так: {message[:60]}"


def cemetery_tour() -> list[dict]:
    return [{"task": "Купить хлеб", "owner": "grandma", "status": "memorial"}]


def reborn_task(title: str) -> dict:
    return {"title": title, "status": "reborn"}
