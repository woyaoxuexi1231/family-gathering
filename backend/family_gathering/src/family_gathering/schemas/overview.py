from pydantic import BaseModel

from family_gathering.schemas.entry import EntryOut
from family_gathering.schemas.meta import MetaOut


class OverviewStatsOut(BaseModel):
    entry_count: int
    headcount_total: int


class OverviewOut(BaseModel):
    meta: MetaOut
    stats: OverviewStatsOut
    entries: list[EntryOut]
