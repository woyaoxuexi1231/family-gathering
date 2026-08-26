"""聚会数据读写 — 单文件 JSON。"""

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from family_gathering.config import Settings, get_settings
from family_gathering.models import Gathering
from family_gathering.persistence.codec import gathering_from_dict, gathering_to_dict

logger = logging.getLogger(__name__)

T = TypeVar("T")


class GatheringStore:
    def __init__(self, data_path: Path, settings: Settings | None = None) -> None:
        self._data_path = data_path
        self._settings = settings or get_settings()

    @property
    def data_path(self) -> Path:
        return self._data_path

    def load(self) -> Gathering:
        if not self._data_path.exists():
            gathering = Gathering()
            self.save(gathering)
            logger.info("初始化数据文件: %s", self._data_path)
            return gathering

        raw = self._data_path.read_text(encoding="utf-8")
        if not raw.strip():
            gathering = Gathering()
            self.save(gathering)
            return gathering

        return gathering_from_dict(json.loads(raw))

    def save(self, gathering: Gathering) -> None:
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            gathering_to_dict(gathering),
            ensure_ascii=False,
            indent=2,
        )
        tmp_path = self._data_path.with_suffix(".json.tmp")
        tmp_path.write_text(payload + "\n", encoding="utf-8")
        tmp_path.replace(self._data_path)
        logger.debug("已写入 %s", self._data_path)

    def update(self, mutator: Callable[[Gathering], T]) -> T:
        gathering = self.load()
        result = mutator(gathering)
        self.save(gathering)
        return result


def get_store() -> GatheringStore:
    settings = get_settings()
    return GatheringStore(settings.data_path, settings)
