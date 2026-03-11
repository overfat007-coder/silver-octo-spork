"""Application entrypoint."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.api.router import api_router
from app.api.routes.realtime import router as realtime_router
from app.core.config import settings
from app.database import init_db
from app.events.registry import register_default_handlers
from app.utils.logging import configure_logging
from app.utils.middleware import RequestContextFilter, RequestLoggingMiddleware

configure_logging()
logging.getLogger().addFilter(RequestContextFilter())

app = FastAPI(title=settings.app_name, version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


@app.on_event("startup")
def startup() -> None:
    init_db()
    register_default_handlers()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "-")
    logging.getLogger("smartflow").exception("Unhandled exception", extra={"request_id": request_id})
    return JSONResponse(status_code=500, content={"error": "Internal server error", "request_id": request_id})


@app.get("/")
def index() -> FileResponse:
    return FileResponse("app/templates/index.html")


@app.get("/tictactoe")
def tictactoe_client() -> FileResponse:
    return FileResponse("app/templates/tictactoe.html")

app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(realtime_router)
