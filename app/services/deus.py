"""Module 43 - Deity interface simulation."""


def pray(text: str, intention: str) -> dict:
    return {"accepted": True, "intention": intention, "blessing": f"Молитва услышана: {text[:50]}"}


def miracle_request(virtue: int, sins: int) -> dict:
    chance = max(0.0, min(1.0, (virtue - sins) / 100 + 0.3))
    return {"granted": chance > 0.5, "chance": round(chance, 3)}


def judgment(users: list[dict]) -> list[dict]:
    out = []
    for u in users:
        ratio = float(u.get("completed_ratio", 0))
        state = "heaven" if ratio > 0.9 else "hell" if ratio < 0.1 else "purgatory"
        out.append({"user_id": u.get("user_id"), "state": state})
    return out
