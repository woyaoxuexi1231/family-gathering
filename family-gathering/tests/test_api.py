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


def test_web_home(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "API 测试聚餐" in response.text


def test_web_add_participant_form(client: TestClient) -> None:
    response = client.post(
        "/participants",
        data={"name": "老王", "headcount": "2", "status": "coming", "note": ""},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].startswith("/?msg=")

    home = client.get("/")
    assert "老王" in home.text
