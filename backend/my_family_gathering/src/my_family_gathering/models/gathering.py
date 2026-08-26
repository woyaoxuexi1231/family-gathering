# TODO: 抄 ../family_gathering/src/family_gathering/models/gathering.py
# 只有 Entry + Gathering；没有 GatheringMeta / Participant / Dish

from dataclasses import dataclass, field
from uuid import uuid4


def new_id() -> str:
    return uuid4().hex[:12]



# 单条报名：谁、做什么菜
# @dataclass 详解见 python-from-zero 第 26 课
@dataclass
class Entry:
    id: str
    name: str
    dish: str
    headcount: int = 1
    note: str = ""


# 报名列表
# entries 的 field(default_factory=list) 见 python-from-zero 第 26 课【3】
@dataclass
class Gathering:
    entries: list[Entry] = field(default_factory=list)

    def find_entry(self, entry_id: str) -> Entry | None:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None
