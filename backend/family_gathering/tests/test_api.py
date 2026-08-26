import pytest
from fastapi.testclient import TestClient

from family_gathering.config import Settings, get_settings
from family_gathering.main import app
from family_gathering.persistence.store import GatheringStore, get_store


@pytest.fixture
def client(tmp_path):
    data_path = tmp_path / "gathering.json"
    settings = Settings(
        data_path=data_path,
        gathering_title="API 测试聚餐",
        gathering_when="周日 18:00",
        gathering_where="家里",
    )

    store = GatheringStore(settings.data_path, settings)

    app.dependency_overrides[get_store] = lambda: store
    app.dependency_overrides[get_settings] = lambda: settings

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_meta_from_settings(client: TestClient) -> None:
    response = client.get("/api/meta")
    assert response.status_code == 200
    assert response.json()["title"] == "API 测试聚餐"


def test_overview_empty(client: TestClient) -> None:
    response = client.get("/api/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["title"] == "API 测试聚餐"
    assert body["stats"]["entry_count"] == 0
    assert body["entries"] == []


def test_entry_api(client: TestClient) -> None:
    created = client.post(
        "/api/entries",
        json={"name": "老王", "dish": "红烧肉", "headcount": 2, "note": ""},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "老王"
    assert body["dish"] == "红烧肉"

    listed = client.get("/api/entries")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    overview = client.get("/api/overview")
    assert overview.json()["stats"]["entry_count"] == 1
    assert overview.json()["stats"]["headcount_total"] == 2

    deleted = client.delete(f"/api/entries/{body['id']}")
    assert deleted.status_code == 204
    assert client.get("/api/entries").json() == []
