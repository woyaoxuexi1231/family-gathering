"""总览统计。"""

from dataclasses import dataclass

from family_gathering.models import Gathering


@dataclass
class OverviewStats:
    entry_count: int
    headcount_total: int


def build_overview(gathering: Gathering) -> OverviewStats:
    return OverviewStats(
        entry_count=len(gathering.entries),
        headcount_total=sum(e.headcount for e in gathering.entries),
    )
