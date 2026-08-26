from fastapi import APIRouter, Depends

from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.schemas.dish import DishClaim, DishCreate, DishOut
from family_gathering.services import dishes as dish_service

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("", response_model=list[DishOut])
def list_dishes(store: GatheringStore = Depends(get_store)) -> list[DishOut]:
    gathering = store.load()
    return [
        DishOut.model_validate(dish, from_attributes=True)
        for dish in gathering.dishes
    ]


@router.post("", response_model=DishOut, status_code=201)
def create_dish(
    body: DishCreate,
    store: GatheringStore = Depends(get_store),
) -> DishOut:
    def mutate(gathering):
        return dish_service.add_dish(
            gathering,
            name=body.name,
            servings=body.servings,
        )

    dish = store.update(mutate)
    return DishOut.model_validate(dish, from_attributes=True)


@router.post("/{dish_id}/claim", response_model=DishOut)
def claim_dish(
    dish_id: str,
    body: DishClaim,
    store: GatheringStore = Depends(get_store),
) -> DishOut:
    def mutate(gathering):
        return dish_service.claim_dish(gathering, dish_id, body.participant_id)

    dish = store.update(mutate)
    return DishOut.model_validate(dish, from_attributes=True)


@router.post("/{dish_id}/unclaim", response_model=DishOut)
def unclaim_dish(
    dish_id: str,
    store: GatheringStore = Depends(get_store),
) -> DishOut:
    def mutate(gathering):
        return dish_service.unclaim_dish(gathering, dish_id)

    dish = store.update(mutate)
    return DishOut.model_validate(dish, from_attributes=True)
