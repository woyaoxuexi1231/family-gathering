"""JSON 与领域对象互转。"""

from typing import Any

from family_gathering.models import (
    Dish,
    DishStatus,
    Gathering,
    GatheringMeta,
    Participant,
    ParticipantStatus,
)


def gathering_to_dict(gathering: Gathering) -> dict[str, Any]:
    return {
        "meta": {
            "title": gathering.meta.title,
            "when": gathering.meta.when,
            "where": gathering.meta.where,
            "note": gathering.meta.note,
        },
        "participants": [
            {
                "id": p.id,
                "name": p.name,
                "headcount": p.headcount,
                "status": p.status.value,
                "note": p.note,
            }
            for p in gathering.participants
        ],
        "dishes": [
            {
                "id": d.id,
                "name": d.name,
                "claimed_by": d.claimed_by,
                "servings": d.servings,
                "status": d.status.value,
            }
            for d in gathering.dishes
        ],
    }


def gathering_from_dict(data: dict[str, Any]) -> Gathering:
    meta_raw = data.get("meta") or {}
    return Gathering(
        meta=GatheringMeta(
            title=str(meta_raw.get("title", "")),
            when=str(meta_raw.get("when", "")),
            where=str(meta_raw.get("where", "")),
            note=str(meta_raw.get("note", "")),
        ),
        participants=[
            Participant(
                id=str(item["id"]),
                name=str(item["name"]),
                headcount=int(item.get("headcount", 1)),
                status=ParticipantStatus(item.get("status", ParticipantStatus.COMING)),
                note=str(item.get("note", "")),
            )
            for item in data.get("participants", [])
        ],
        dishes=[
            Dish(
                id=str(item["id"]),
                name=str(item["name"]),
                claimed_by=item.get("claimed_by"),
                servings=str(item.get("servings", "")),
                status=DishStatus(item.get("status", DishStatus.OPEN)),
            )
            for item in data.get("dishes", [])
        ],
    )
