import pytest

from family_gathering.config import Settings
from family_gathering.errors import ConflictError, NotFoundError
from family_gathering.persistence.store import GatheringStore
from family_gathering.services import dishes as dish_service
from family_gathering.services import participants as participant_service


@pytest.fixture
def store(tmp_path) -> GatheringStore:
    settings = Settings(
        data_path=tmp_path / "gathering.json",
        gathering_title="测试聚餐",
        gathering_when="明天 18:00",
        gathering_where="测试地点",
    )
    return GatheringStore(settings.data_path, settings)


def test_add_participant(store: GatheringStore) -> None:
    person = store.update(
        lambda g: participant_service.add_participant(g, name="小明", headcount=2)
    )
    assert person.name == "小明"
    assert person.headcount == 2

    gathering = store.load()
    assert len(gathering.participants) == 1


def test_duplicate_name_rejected(store: GatheringStore) -> None:
    store.update(lambda g: participant_service.add_participant(g, name="小明"))

    with pytest.raises(ConflictError):
        store.update(lambda g: participant_service.add_participant(g, name="小明"))


def test_remove_participant_unclaims_dish(store: GatheringStore) -> None:
    person = store.update(lambda g: participant_service.add_participant(g, name="小红"))
    dish = store.update(lambda g: dish_service.add_dish(g, name="红烧肉"))
    store.update(lambda g: dish_service.claim_dish(g, dish.id, person.id))

    store.update(lambda g: participant_service.remove_participant(g, person.id))

    gathering = store.load()
    assert gathering.find_participant(person.id) is None
    saved_dish = gathering.find_dish(dish.id)
    assert saved_dish is not None
    assert saved_dish.claimed_by is None
    assert saved_dish.status.value == "open"


def test_claim_dish_requires_participant(store: GatheringStore) -> None:
    dish = store.update(lambda g: dish_service.add_dish(g, name="凉拌黄瓜"))

    with pytest.raises(NotFoundError):
        store.update(lambda g: dish_service.claim_dish(g, dish.id, "missing"))


def test_claim_conflict_when_already_claimed(store: GatheringStore) -> None:
    a = store.update(lambda g: participant_service.add_participant(g, name="甲"))
    b = store.update(lambda g: participant_service.add_participant(g, name="乙"))
    dish = store.update(lambda g: dish_service.add_dish(g, name="清蒸鱼"))
    store.update(lambda g: dish_service.claim_dish(g, dish.id, a.id))

    with pytest.raises(ConflictError):
        store.update(lambda g: dish_service.claim_dish(g, dish.id, b.id))


def test_empty_gathering_meta_from_settings(store: GatheringStore) -> None:
    gathering = store.load()
    assert gathering.meta.title == "测试聚餐"
    assert gathering.participants == []
    assert gathering.dishes == []
