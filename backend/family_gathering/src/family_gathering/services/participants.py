"""参与人业务规则。"""

from family_gathering.errors import ConflictError, NotFoundError
from family_gathering.models import (
    DishStatus,
    Gathering,
    Participant,
    ParticipantStatus,
    new_id,
)


def _normalize_name(name: str) -> str:
    return name.strip()


def _ensure_unique_name(gathering: Gathering, name: str, *, exclude_id: str | None = None) -> None:
    target = name.casefold()
    for person in gathering.participants:
        if exclude_id and person.id == exclude_id:
            continue
        if person.name.casefold() == target:
            raise ConflictError(f"参与人已存在: {name}")


def add_participant(
    gathering: Gathering,
    *,
    name: str,
    headcount: int = 1,
    status: ParticipantStatus = ParticipantStatus.COMING,
    note: str = "",
) -> Participant:
    clean_name = _normalize_name(name)
    if not clean_name:
        raise ConflictError("姓名不能为空")
    if headcount < 1:
        raise ConflictError("人数至少为 1")

    _ensure_unique_name(gathering, clean_name)
    person = Participant(
        id=new_id(),
        name=clean_name,
        headcount=headcount,
        status=status,
        note=note.strip(),
    )
    gathering.participants.append(person)
    return person


def update_participant(
    gathering: Gathering,
    participant_id: str,
    *,
    name: str | None = None,
    headcount: int | None = None,
    status: ParticipantStatus | None = None,
    note: str | None = None,
) -> Participant:
    person = gathering.find_participant(participant_id)
    if person is None:
        raise NotFoundError(f"参与人不存在: {participant_id}")

    if name is not None:
        clean_name = _normalize_name(name)
        if not clean_name:
            raise ConflictError("姓名不能为空")
        _ensure_unique_name(gathering, clean_name, exclude_id=participant_id)
        person.name = clean_name

    if headcount is not None:
        if headcount < 1:
            raise ConflictError("人数至少为 1")
        person.headcount = headcount

    if status is not None:
        person.status = status

    if note is not None:
        person.note = note.strip()

    return person


def remove_participant(gathering: Gathering, participant_id: str) -> None:
    person = gathering.find_participant(participant_id)
    if person is None:
        raise NotFoundError(f"参与人不存在: {participant_id}")

    gathering.participants = [p for p in gathering.participants if p.id != participant_id]

    # 删除参与人时，其认领的菜回到 open
    for dish in gathering.dishes:
        if dish.claimed_by == participant_id:
            dish.claimed_by = None
            dish.status = DishStatus.OPEN
