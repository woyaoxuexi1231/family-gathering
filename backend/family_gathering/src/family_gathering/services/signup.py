"""一步报名：参与人 + 分工（带什么/做什么）。"""

from dataclasses import dataclass

from family_gathering.errors import NotFoundError
from family_gathering.models import Dish, Gathering, Participant
from family_gathering.services import dishes as dish_service
from family_gathering.services import participants as participant_service


@dataclass
class Signup:
    participant: Participant
    task: Dish | None


def add_signup(
    gathering: Gathering,
    *,
    name: str,
    task: str,
    headcount: int = 1,
    note: str = "",
) -> Signup:
    person = participant_service.add_participant(
        gathering,
        name=name,
        headcount=headcount,
        note=note,
    )
    dish = dish_service.add_dish(gathering, name=task)
    dish_service.claim_dish(gathering, dish.id, person.id)
    return Signup(participant=person, task=dish)


def remove_signup(gathering: Gathering, participant_id: str) -> None:
    if gathering.find_participant(participant_id) is None:
        raise NotFoundError(f"参与人不存在: {participant_id}")

    gathering.dishes = [d for d in gathering.dishes if d.claimed_by != participant_id]
    gathering.participants = [p for p in gathering.participants if p.id != participant_id]


def list_signups(gathering: Gathering) -> list[Signup]:
    dish_by_person: dict[str, Dish] = {}
    for dish in gathering.dishes:
        if dish.claimed_by:
            dish_by_person[dish.claimed_by] = dish

    return [
        Signup(participant=person, task=dish_by_person.get(person.id))
        for person in gathering.participants
    ]
