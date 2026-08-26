from dataclasses import dataclass, field
from uuid import uuid4


def new_id() -> str:
    return uuid4().hex[:12]


@dataclass
class Entry:
    """一条报名：谁来、自己做什么菜。"""

    id: str
    name: str
    dish: str
    headcount: int = 1
    note: str = ""


@dataclass
class Gathering:
    """单次聚餐的可变部分：只是报名列表。时间地点等固定信息在 Settings。"""

    entries: list[Entry] = field(default_factory=list)

    def find_entry(self, entry_id: str) -> Entry | None:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None
