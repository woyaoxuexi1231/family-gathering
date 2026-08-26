from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.entry import EntryCreate, EntryOut
from family_gathering.services import entries as entry_service

router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("", response_model=list[EntryOut])
def list_entries(store: GatheringStore = Depends(get_store)) -> list[EntryOut]:
    gathering = store.load()
    return [EntryOut.model_validate(e, from_attributes=True) for e in gathering.entries]


@router.post("", response_model=EntryOut, status_code=201)
def create_entry(
    body: EntryCreate,
    store: GatheringStore = Depends(get_store),
) -> EntryOut:
    entry = store.update(
        lambda g: entry_service.add_entry(
            g,
            name=body.name,
            dish=body.dish,
            headcount=body.headcount,
            note=body.note,
        )
    )
    return EntryOut.model_validate(entry, from_attributes=True)


@router.delete("/{entry_id}", status_code=204)
def delete_entry(
    entry_id: str,
    store: GatheringStore = Depends(get_store),
) -> None:
    store.update(lambda g: entry_service.remove_entry(g, entry_id))
