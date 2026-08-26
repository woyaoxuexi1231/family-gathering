from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.participant import (
    ParticipantCreate,
    ParticipantOut,
    ParticipantUpdate,
)
from family_gathering.services import participants as participant_service

router = APIRouter(prefix="/participants", tags=["participants"])


@router.get("", response_model=list[ParticipantOut])
def list_participants(store: GatheringStore = Depends(get_store)) -> list[ParticipantOut]:
    gathering = store.load()
    return [
        ParticipantOut.model_validate(person, from_attributes=True)
        for person in gathering.participants
    ]


@router.post("", response_model=ParticipantOut, status_code=201)
def create_participant(
    body: ParticipantCreate,
    store: GatheringStore = Depends(get_store),
) -> ParticipantOut:
    def mutate(gathering):
        return participant_service.add_participant(
            gathering,
            name=body.name,
            headcount=body.headcount,
            status=body.status,
            note=body.note,
        )

    person = store.update(mutate)
    return ParticipantOut.model_validate(person, from_attributes=True)


@router.patch("/{participant_id}", response_model=ParticipantOut)
def update_participant(
    participant_id: str,
    body: ParticipantUpdate,
    store: GatheringStore = Depends(get_store),
) -> ParticipantOut:
    def mutate(gathering):
        return participant_service.update_participant(
            gathering,
            participant_id,
            name=body.name,
            headcount=body.headcount,
            status=body.status,
            note=body.note,
        )

    person = store.update(mutate)
    return ParticipantOut.model_validate(person, from_attributes=True)


@router.delete("/{participant_id}", status_code=204)
def delete_participant(
    participant_id: str,
    store: GatheringStore = Depends(get_store),
) -> None:
    def mutate(gathering):
        participant_service.remove_participant(gathering, participant_id)

    store.update(mutate)
