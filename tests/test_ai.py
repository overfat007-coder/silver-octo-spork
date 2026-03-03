from app.services.priority import analyze_task_priority


def test_high_priority() -> None:
    assert analyze_task_priority("Срочно исправить баг") == 5


def test_low_priority() -> None:
    assert analyze_task_priority("Идея для отпуска") == 1


def test_medium_priority() -> None:
    assert analyze_task_priority("Купить молоко") == 3
