"""练习版 FastAPI 入口 — 目前只有 health，其余待抄写。"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from my_family_gathering.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="My Family Gathering API (练习版)",
    description="对照 backend/family_gathering 逐文件抄写",
    version="0.1.0",
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: 抄完 api/ 后在这里 include_router，参考 ../family_gathering/src/family_gathering/main.py


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "my-family-gathering"}


def main() -> None:
    import uvicorn

    uvicorn.run(
        "my_family_gathering.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
