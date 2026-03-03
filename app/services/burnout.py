"""Burnout prediction stubs."""


def fatigue_index(response_delay_sec: float, typo_rate: float, night_sessions: int, weekend_work: int) -> float:
    score = response_delay_sec * 0.1 + typo_rate * 40 + night_sessions * 8 + weekend_work * 10
    return max(0.0, min(100.0, score))


def burnout_probability_14d(fatigue: float) -> float:
    return max(0.0, min(1.0, fatigue / 100.0))


def recommendation(prob: float) -> str:
    if prob > 0.7:
        return "Высокий риск выгорания: ограничьте вечерние задачи и возьмите выходной"
    if prob > 0.4:
        return "Средний риск: добавьте перерывы и уменьшите контекст-переключения"
    return "Риск низкий: поддерживайте текущий ритм"
