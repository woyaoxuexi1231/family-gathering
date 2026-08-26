from enum import StrEnum


class ParticipantStatus(StrEnum):
    COMING = "coming"
    MAYBE = "maybe"
    DECLINED = "declined"


class DishStatus(StrEnum):
    OPEN = "open"
    CLAIMED = "claimed"
    DONE = "done"
