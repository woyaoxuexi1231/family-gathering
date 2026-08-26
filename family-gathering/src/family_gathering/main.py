"""FastAPI 入口。"""

from __future__ import annotations

import logging

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from family_gathering.api import dishes, meta, overview, participants
from family_gathering.config import get_settings
from family_gathering.errors import ConflictError, DomainError, NotFoundError
from family_gathering.web import routes as web_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="Family Gathering",
    description="单次家庭聚餐：参与人报名 + 认领菜品",
    version="0.1.0",
)

app.include_router(web_routes.router)
app.include_router(meta.router, prefix="/api")
app.include_router(participants.router, prefix="/api")
app.include_router(dishes.router, prefix="/api")
app.include_router(overview.router, prefix="/api")

STATIC_DIR = Path(__file__).resolve().parent / "web" / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(NotFoundError)
def handle_not_found(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
def handle_conflict(_request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DomainError)
def handle_domain(_request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def main() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "family_gathering.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
