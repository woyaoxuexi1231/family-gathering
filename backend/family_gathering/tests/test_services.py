import pytest

from family_gathering.config import Settings
from family_gathering.errors import ConflictError, NotFoundError
from family_gathering.persistence.store import GatheringStore
from family_gathering.services import entries as entry_service


@pytest.fixture
def store(tmp_path) -> GatheringStore:
    settings = Settings(
        data_path=tmp_path / "gathering.json",
        gathering_title="测试聚餐",
        gathering_when="明天 18:00",
        gathering_where="测试地点",
    )
    return GatheringStore(settings.data_path, settings)


def test_empty_gathering(store: GatheringStore) -> None:
    gathering = store.load()
    assert gathering.entries == []


def test_add_entry(store: GatheringStore) -> None:
    entry = store.update(
        lambda g: entry_service.add_entry(g, name="小明", dish="红烧肉", headcount=2)
    )
    assert entry.name == "小明"
    assert entry.dish == "红烧肉"
    assert entry.headcount == 2

    gathering = store.load()
    assert len(gathering.entries) == 1


def test_duplicate_name_rejected(store: GatheringStore) -> None:
    store.update(lambda g: entry_service.add_entry(g, name="小明", dish="红烧肉"))

    with pytest.raises(ConflictError):
        store.update(lambda g: entry_service.add_entry(g, name="小明", dish="清蒸鱼"))


def test_remove_entry(store: GatheringStore) -> None:
    entry = store.update(
        lambda g: entry_service.add_entry(g, name="小红", dish="凉拌黄瓜")
    )
    store.update(lambda g: entry_service.remove_entry(g, entry.id))

    assert store.load().entries == []


def test_remove_missing_entry(store: GatheringStore) -> None:
    with pytest.raises(NotFoundError):
        store.update(lambda g: entry_service.remove_entry(g, "missing"))
