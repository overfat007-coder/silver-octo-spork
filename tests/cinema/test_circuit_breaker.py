import pytest

from microservices.cinema.catalog_service.circuit import CircuitBreaker, CircuitOpenError


def test_circuit_breaker_opens_after_threshold() -> None:
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_s=60)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError('boom')))
    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError('boom')))

    assert breaker.state == 'open'
    with pytest.raises(CircuitOpenError):
        breaker.call(lambda: True)
