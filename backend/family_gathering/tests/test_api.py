import pytest
from fastapi.testclient import TestClient

from family_gathering.config import Settings, get_settings
from family_gathering.main import app
from family_gathering.persistence.store import GatheringStore, get_store


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_path = tmp_path / "gathering.json"
    settings = Settings(
        data_path=data_path,
        gathering_title="API 测试聚餐",
        gathering_when="周日 18:00",
        gathering_where="家里",
    )

    store = GatheringStore(settings.data_path, settings)

    monkeypatch.setattr("family_gathering.config.get_settings", lambda: settings)
    app.dependency_overrides[get_store] = lambda: store

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_overview_empty(client: TestClient) -> None:
    response = client.get("/api/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["title"] == "API 测试聚餐"
    assert body["stats"]["participant_count"] == 0


def test_participant_and_dish_flow(client: TestClient) -> None:
    p = client.post(
        "/api/participants",
        json={"name": "小李", "headcount": 3, "status": "coming"},
    )
    assert p.status_code == 201
    participant_id = p.json()["id"]

    d = client.post("/api/dishes", json={"name": "糖醋排骨", "servings": "一大份"})
    assert d.status_code == 201
    dish_id = d.json()["id"]

    claimed = client.post(
        f"/api/dishes/{dish_id}/claim",
        json={"participant_id": participant_id},
    )
    assert claimed.status_code == 200
    assert claimed.json()["claimed_by"] == participant_id

    overview = client.get("/api/overview")
    assert overview.json()["stats"]["coming_headcount"] == 3
    assert overview.json()["stats"]["claimed_dish_count"] == 1


def test_signup_api(client: TestClient) -> None:
    created = client.post(
        "/api/signups",
        json={"name": "老王", "task": "带水果", "headcount": 2, "note": ""},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["participant"]["name"] == "老王"
    assert body["task"]["name"] == "带水果"

    listed = client.get("/api/signups")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["participant"]["name"] == "老王"

    participant_id = body["participant"]["id"]
    deleted = client.delete(f"/api/signups/{participant_id}")
    assert deleted.status_code == 204
    assert client.get("/api/signups").json() == []
