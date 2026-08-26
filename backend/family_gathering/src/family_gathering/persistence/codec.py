"""JSON 与领域对象互转。"""

from typing import Any

from family_gathering.models import Entry, Gathering


def gathering_to_dict(gathering: Gathering) -> dict[str, Any]:
    return {
        "entries": [
            {
                "id": e.id,
                "name": e.name,
                "dish": e.dish,
                "headcount": e.headcount,
                "note": e.note,
            }
            for e in gathering.entries
        ],
    }


def gathering_from_dict(data: dict[str, Any]) -> Gathering:
    return Gathering(
        entries=[
            Entry(
                id=str(item["id"]),
                name=str(item["name"]),
                dish=str(item["dish"]),
                headcount=int(item.get("headcount", 1)),
                note=str(item.get("note", "")),
            )
            for item in data.get("entries", [])
        ],
    )
