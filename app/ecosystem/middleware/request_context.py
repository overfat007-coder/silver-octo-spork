"""Request context middleware to propagate correlation IDs."""

from types import SimpleNamespace
from uuid import uuid4


class RequestContextMiddleware:
    """Attach `request_id` to request.state and response headers."""

    async def __call__(self, request, call_next):  # type: ignore[no-untyped-def]
        request_id = getattr(request, "headers", {}).get("x-request-id", str(uuid4()))
        if not hasattr(request, "state"):
            request.state = SimpleNamespace()
        request.state.request_id = request_id
        response = await call_next(request)
        if not hasattr(response, "headers"):
            response.headers = {}
        response.headers["x-request-id"] = request_id
        return response
