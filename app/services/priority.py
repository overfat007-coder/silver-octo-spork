"""Pure python fallback priority analyzer."""


def analyze_task_priority(title: str, description: str = "") -> int:
    text = f"{title} {description}".lower()
    high_priority_keywords = ["срочно", "критично", "дедлайн", "важно", "авария"]
    low_priority_keywords = ["потом", "не срочно", "когда-нибудь", "идея"]
    if any(keyword in text for keyword in high_priority_keywords):
        return 5
    if any(keyword in text for keyword in low_priority_keywords):
        return 1
    return 3
