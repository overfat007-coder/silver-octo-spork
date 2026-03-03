"""AI services for task enrichment with circuit-breaker and fallback."""

import json

from app.services.priority import analyze_task_priority


def enhance_task_with_ai(title: str, description: str = "") -> dict:
    """Get priority/category/estimate via LLM with robust fallback."""
    fallback = {
        "priority": analyze_task_priority(title, description),
        "category": "Личное",
        "estimated_minutes": 30,
    }
    from app.core.config import settings
    from app.services.wasm_runtime import run_wasm_priority_plugin

    wasm_priority = run_wasm_priority_plugin(title, description)
    if wasm_priority is not None:
        fallback["priority"] = wasm_priority

    if not settings.openai_api_key:
        return fallback

    prompt = (
        "Проанализируй задачу: "
        f"'Заголовок: {title}, Описание: {description}'. "
        "Определи её приоритет (1-5), предполагаемую категорию "
        "(Работа, Личное, Покупки, Здоровье) и примерное время выполнения в минутах. "
        'Ответ верни в формате JSON: {"priority": int, "category": str, "estimated_minutes": int}'
    )

    try:
        import pybreaker
        import requests

        breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)

        @breaker
        def _call() -> dict:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1},
                timeout=8,
            )
            response.raise_for_status()
            return response.json()

        payload = _call()
        content = payload["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return {
            "priority": int(parsed.get("priority", fallback["priority"])),
            "category": parsed.get("category", fallback["category"]),
            "estimated_minutes": int(parsed.get("estimated_minutes", fallback["estimated_minutes"])),
        }
    except Exception:
        return fallback
