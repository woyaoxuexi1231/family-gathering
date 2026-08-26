"""应用配置 — 与参考版同一端口，切换运行哪个包即可。"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "my_gathering.json"


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

    gathering_title: str = "我的家庭聚餐（练习）"
    gathering_when: str = "待定"
    gathering_where: str = "待定"
    gathering_note: str = "这是练习版，对照 family_gathering 抄写"

    data_path: Path = DEFAULT_DATA_PATH


@lru_cache
def get_settings() -> Settings:
    return Settings()
