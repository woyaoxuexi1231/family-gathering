from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.dish import DishOut
from family_gathering.schemas.meta import MetaOut
from family_gathering.schemas.overview import OverviewOut, OverviewStatsOut
from family_gathering.schemas.participant import ParticipantOut
from family_gathering.services import overview as overview_service

router = APIRouter(prefix="/overview", tags=["overview"])


@router.get("", response_model=OverviewOut)
def read_overview(store: GatheringStore = Depends(get_store)) -> OverviewOut:
    gathering = store.load()
    stats, gathering = overview_service.build_overview(gathering)
    return OverviewOut(
        meta=MetaOut.model_validate(gathering.meta, from_attributes=True),
        stats=OverviewStatsOut.model_validate(stats, from_attributes=True),
        participants=[
            ParticipantOut.model_validate(person, from_attributes=True)
            for person in gathering.participants
        ],
        dishes=[
            DishOut.model_validate(dish, from_attributes=True)
            for dish in gathering.dishes
        ],
    )
