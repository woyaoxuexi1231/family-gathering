from dataclasses import dataclass, field
from uuid import uuid4

from family_gathering.models.enums import DishStatus, ParticipantStatus


def new_id() -> str:
    return uuid4().hex[:12]


@dataclass
class GatheringMeta:
    title: str
    when: str
    where: str
    note: str = ""


@dataclass
class Participant:
    id: str
    name: str
    headcount: int = 1
    status: ParticipantStatus = ParticipantStatus.COMING
    note: str = ""


@dataclass
class Dish:
    id: str
    name: str
    claimed_by: str | None = None
    servings: str = ""
    status: DishStatus = DishStatus.OPEN


@dataclass
class Gathering:
    meta: GatheringMeta
    participants: list[Participant] = field(default_factory=list)
    dishes: list[Dish] = field(default_factory=list)

    def find_participant(self, participant_id: str) -> Participant | None:
        for person in self.participants:
            if person.id == participant_id:
                return person
        return None

    def find_dish(self, dish_id: str) -> Dish | None:
        for dish in self.dishes:
            if dish.id == dish_id:
                return dish
        return None
