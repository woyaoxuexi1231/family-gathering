from fastapi import APIRouter, Depends

from family_gathering.config import Settings, get_settings
from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.entry import EntryOut
from family_gathering.schemas.meta import MetaOut
from family_gathering.schemas.overview import OverviewOut, OverviewStatsOut
from family_gathering.services import overview as overview_service

router = APIRouter(prefix="/overview", tags=["overview"])


@router.get("", response_model=OverviewOut)
def read_overview(
    store: GatheringStore = Depends(get_store),
    settings: Settings = Depends(get_settings),
) -> OverviewOut:
    gathering = store.load()
    stats = overview_service.build_overview(gathering)
    return OverviewOut(
        meta=MetaOut(
            title=settings.gathering_title,
            when=settings.gathering_when,
            where=settings.gathering_where,
            note=settings.gathering_note,
        ),
        stats=OverviewStatsOut.model_validate(stats, from_attributes=True),
        entries=[
            EntryOut.model_validate(entry, from_attributes=True)
            for entry in gathering.entries
        ],
    )
