"""应用配置 — 聚会固定信息与数据文件路径。"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# src/family_gathering/config.py → backend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "gathering.json"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_host: str = "127.0.0.1"
    app_port: int = 8800
    cors_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]

    gathering_title: str = "家庭聚餐"
    gathering_when: str = "2026-08-30 18:00"
    gathering_where: str = "家里"
    gathering_note: str = "欢迎带拿手菜，记得认领想做的菜"

    data_path: Path = DEFAULT_DATA_PATH


@lru_cache
def get_settings() -> Settings:
    return Settings()
