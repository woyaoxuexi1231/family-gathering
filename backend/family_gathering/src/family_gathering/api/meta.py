from fastapi import APIRouter, Depends

from family_gathering.config import Settings, get_settings
from family_gathering.schemas.meta import MetaOut

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("", response_model=MetaOut)
def read_meta(settings: Settings = Depends(get_settings)) -> MetaOut:
    return MetaOut(
        title=settings.gathering_title,
        when=settings.gathering_when,
        where=settings.gathering_where,
        note=settings.gathering_note,
    )
