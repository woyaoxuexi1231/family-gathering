from pydantic import BaseModel

from family_gathering.schemas.dish import DishOut
from family_gathering.schemas.meta import MetaOut
from family_gathering.schemas.participant import ParticipantOut


class OverviewStatsOut(BaseModel):
    participant_count: int
    coming_headcount: int
    dish_count: int
    open_dish_count: int
    claimed_dish_count: int


class OverviewOut(BaseModel):
    meta: MetaOut
    stats: OverviewStatsOut
    participants: list[ParticipantOut]
    dishes: list[DishOut]
