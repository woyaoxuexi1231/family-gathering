"""应用配置 — 与参考版同一端口，切换运行哪个包即可。"""

# functools 是 Python 标准库（装 Python 自带，不用 pip 额外装），里面放了很多“函数工具”。
from functools import lru_cache

# 用来表示文件路径（支持 / 拼接，跨平台友好）。
from pathlib import Path

# 来自 pydantic-settings 这个第三方库（装在项目环境里）。config.py 靠它做配置类：
# BaseSettings：配置基类，继承它就能写一个“带默认值的配置类”，还能自动读 .env 文件。
# SettingsConfigDict：专门用来描述这个配置类怎么读取（比如指定 .env 的路径）。
from pydantic_settings import BaseSettings, SettingsConfigDict

# 当前文件的绝对路径 resolve() 的 上一层 + 上一层 + 上一层 也就是 family-gathering
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# 使用 / 直接拼接路径。 在 family-gathering 路径下的 data/my_gathering.json 文件
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "my_gathering.json"

# 继承到 BaseSettings
class Settings(BaseSettings):
    # pydantic 的“配置的配置”，
    model_config = SettingsConfigDict(
        # 指定加载环境变量的文件路径。额外还要加载这个配置文件的配置
        env_file=str(PROJECT_ROOT / ".env"),
        # 指定读取 .env 文件时使用的字符编码为 utf-8。
        env_file_encoding="utf-8",
        # 忽略模型中未定义的额外字段。
        # 这里我只定义了 app_host, app_port, cors_origins, gathering_title, gathering_when, gathering_where, gathering_note, data_path。
        # 这几个配置，在 extra="ignore" 的情况下，env文件如果有其他的配置，那么是不会去理会的
        extra="ignore",
    )

    # http服务的配置信息
    app_host: str = "127.0.0.1"
    app_port: int = 8800
    cors_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]

    # 聚餐活动的的信息
    gathering_title: str = "我的家庭聚餐（练习）"
    gathering_when: str = "待定"
    gathering_where: str = "待定"
    gathering_note: str = "这是练习版，对照 family_gathering 抄写"

    data_path: Path = DEFAULT_DATA_PATH


@lru_cache
def get_settings() -> Settings:
    return Settings()
