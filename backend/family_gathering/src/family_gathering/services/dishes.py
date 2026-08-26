"""菜品业务规则。"""

from family_gathering.errors import ConflictError, NotFoundError
from family_gathering.models import Dish, DishStatus, Gathering, new_id


def _normalize_name(name: str) -> str:
    return name.strip()


def add_dish(
    gathering: Gathering,
    *,
    name: str,
    servings: str = "",
) -> Dish:
    clean_name = _normalize_name(name)
    if not clean_name:
        raise ConflictError("菜名不能为空")

    dish = Dish(
        id=new_id(),
        name=clean_name,
        servings=servings.strip(),
        status=DishStatus.OPEN,
    )
    gathering.dishes.append(dish)
    return dish


def claim_dish(
    gathering: Gathering,
    dish_id: str,
    participant_id: str,
) -> Dish:
    dish = gathering.find_dish(dish_id)
    if dish is None:
        raise NotFoundError(f"菜品不存在: {dish_id}")

    person = gathering.find_participant(participant_id)
    if person is None:
        raise NotFoundError(f"参与人不存在: {participant_id}")

    if dish.claimed_by and dish.claimed_by != participant_id:
        raise ConflictError("这道菜已被别人认领")

    dish.claimed_by = participant_id
    dish.status = DishStatus.CLAIMED
    return dish


def unclaim_dish(gathering: Gathering, dish_id: str) -> Dish:
    dish = gathering.find_dish(dish_id)
    if dish is None:
        raise NotFoundError(f"菜品不存在: {dish_id}")

    if not dish.claimed_by:
        raise ConflictError("这道菜尚未被认领")

    dish.claimed_by = None
    dish.status = DishStatus.OPEN
    return dish
