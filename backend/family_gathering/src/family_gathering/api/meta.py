from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.meta import MetaOut

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("", response_model=MetaOut)
def read_meta(store: GatheringStore = Depends(get_store)) -> MetaOut:
    gathering = store.load()
    return MetaOut.model_validate(gathering.meta, from_attributes=True)
