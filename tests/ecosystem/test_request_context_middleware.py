import asyncio
from types import SimpleNamespace

from app.ecosystem.middleware.request_context import RequestContextMiddleware


class DummyRequest:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.state = SimpleNamespace()


class DummyResponse:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}


def test_request_context_sets_header() -> None:
    middleware = RequestContextMiddleware()
    request = DummyRequest()

    async def call_next(req):  # type: ignore[no-untyped-def]
        return DummyResponse()

    response = asyncio.run(middleware(request, call_next))
    assert response.headers.get("x-request-id")
    assert request.state.request_id == response.headers.get("x-request-id")
