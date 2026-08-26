"""报名：谁来、自己做什么菜。"""

from family_gathering.errors import ConflictError, NotFoundError, ValidationError
from family_gathering.models import Entry, Gathering, new_id


def add_entry(
    gathering: Gathering,
    *,
    name: str,
    dish: str,
    headcount: int = 1,
    note: str = "",
) -> Entry:
    cleaned_name = name.strip()
    cleaned_dish = dish.strip()
    if not cleaned_name:
        raise ValidationError("名字不能为空")
    if not cleaned_dish:
        raise ValidationError("菜名不能为空")
    if headcount < 1:
        raise ValidationError("人数至少为 1")

    for existing in gathering.entries:
        if existing.name == cleaned_name:
            raise ConflictError(f"名字已存在: {cleaned_name}")

    entry = Entry(
        id=new_id(),
        name=cleaned_name,
        dish=cleaned_dish,
        headcount=headcount,
        note=note.strip(),
    )
    gathering.entries.append(entry)
    return entry


def remove_entry(gathering: Gathering, entry_id: str) -> None:
    if gathering.find_entry(entry_id) is None:
        raise NotFoundError(f"报名不存在: {entry_id}")
    gathering.entries = [e for e in gathering.entries if e.id != entry_id]
