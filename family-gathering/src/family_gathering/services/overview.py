"""总览统计。"""

from dataclasses import dataclass

from family_gathering.models import DishStatus, Gathering, ParticipantStatus


@dataclass
class OverviewStats:
    participant_count: int
    coming_headcount: int
    dish_count: int
    open_dish_count: int
    claimed_dish_count: int


def build_overview(gathering: Gathering) -> tuple[OverviewStats, Gathering]:
    coming_headcount = sum(
        p.headcount
        for p in gathering.participants
        if p.status == ParticipantStatus.COMING
    )
    open_count = sum(1 for d in gathering.dishes if d.status == DishStatus.OPEN)
    claimed_count = sum(1 for d in gathering.dishes if d.status == DishStatus.CLAIMED)

    stats = OverviewStats(
        participant_count=len(gathering.participants),
        coming_headcount=coming_headcount,
        dish_count=len(gathering.dishes),
        open_dish_count=open_count,
        claimed_dish_count=claimed_count,
    )
    return stats, gathering
