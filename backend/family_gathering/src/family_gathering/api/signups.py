from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.signup import SignupCreate, SignupOut, SignupTaskOut
from family_gathering.schemas.participant import ParticipantOut
from family_gathering.services import signup as signup_service

router = APIRouter(prefix="/signups", tags=["signups"])


def _to_signup_out(signup: signup_service.Signup) -> SignupOut:
    task = None
    if signup.task is not None:
        task = SignupTaskOut(id=signup.task.id, name=signup.task.name)
    return SignupOut(
        participant=ParticipantOut.model_validate(signup.participant, from_attributes=True),
        task=task,
    )


@router.get("", response_model=list[SignupOut])
def list_signups(store: GatheringStore = Depends(get_store)) -> list[SignupOut]:
    gathering = store.load()
    return [_to_signup_out(item) for item in signup_service.list_signups(gathering)]


@router.post("", response_model=SignupOut, status_code=201)
def create_signup(
    body: SignupCreate,
    store: GatheringStore = Depends(get_store),
) -> SignupOut:
    def mutate(gathering):
        return signup_service.add_signup(
            gathering,
            name=body.name,
            task=body.task,
            headcount=body.headcount,
            note=body.note,
        )

    signup = store.update(mutate)
    return _to_signup_out(signup)


@router.delete("/{participant_id}", status_code=204)
def delete_signup(
    participant_id: str,
    store: GatheringStore = Depends(get_store),
) -> None:
    def mutate(gathering):
        signup_service.remove_signup(gathering, participant_id)

    store.update(mutate)
