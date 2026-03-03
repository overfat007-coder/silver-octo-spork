import pytest

from app.ecosystem.utils.retry import retry


def test_retry_success_after_failures() -> None:
    state = {"n": 0}

    def op() -> str:
        state["n"] += 1
        if state["n"] < 3:
            raise RuntimeError("x")
        return "ok"

    assert retry(op, attempts=3, delay_s=0) == "ok"


def test_retry_raises_when_exhausted() -> None:
    with pytest.raises(RuntimeError):
        retry(lambda: (_ for _ in ()).throw(RuntimeError("fail")), attempts=2, delay_s=0)
