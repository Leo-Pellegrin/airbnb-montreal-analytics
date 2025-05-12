# backend/tests/test_endpoints.py

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.core.database import engine
from app.main import app
from app.models.calendar_weekly import calendar_weekly
from app.models.listing import Listings
# Import all models to ensure they're registered with SQLModel
from app.models.neighbourhoods import Neighbourhoods

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Ajout d'un quartier de test
        test_neighbourhood = Neighbourhoods(neighbourhood="Test Neighbourhood")
        session.add(test_neighbourhood)
        session.commit()

        # Ajout d'un listing de test
        test_listing = Listings(
            id=1,  # ID explicite pour référence
            price=100.0,
            latitude=45.5,
            longitude=-73.5,
            neighbourhood="Test Neighbourhood",
            room_type="Entire home/apt",
        )
        session.add(test_listing)
        session.commit()

        # Ajout de données calendar_weekly
        from datetime import date

        today = date.today()
        test_calendar = calendar_weekly(
            listing_id=1,  # Référence au listing créé
            week_id=today,
            avg_price=100.0,
            occupancy_pct=0.5,
        )
        session.add(test_calendar)
        session.commit()

    yield

    from sqlalchemy import text

    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))


@pytest.fixture(scope="module")
def test_user():
    SQLModel.metadata.create_all(engine)

    password = "testpassword"
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": password,
        "full_name": "Test User",
    }
    # Création
    res = client.post("/api/v1/users", json=payload)
    assert res.status_code == 201, f"User creation failed: {res.text}"
    user_id = res.json()["id"]

    yield {"id": user_id, "password": password, "email": payload["email"]}

    # Teardown
    client.delete(f"/api/v1/users/{user_id}")


@pytest.fixture(scope="module")
def auth_headers(test_user):
    """
    Se connecte en POST /login pour récupérer le JWT.
    """
    login_data = {"email": test_user["email"], "password": test_user["password"]}
    res = client.post("/api/v1/login", json=login_data)
    assert res.status_code == 200, f"Login failed: {res.text}"
    token = res.json().get("access_token")
    assert token, "No access_token in login response"
    return {"Authorization": f"Bearer {token}"}


# --- Health Check ---
def test_health_success(auth_headers):
    res = client.get("/api/v1/health", headers=auth_headers)
    assert res.status_code == 200
    json = res.json()
    assert json.get("status") == "ok"
    # 'db' doit être un int (résultat de SELECT 1)
    assert isinstance(json.get("db"), int)


# --- Listings ---


def test_read_listings_default(auth_headers):
    res = client.get("/api/v1/listings", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # par défaut, max 20 résultats
    assert len(data) <= 20
    if data:
        item = data[0]
        # clés essentielles présentes
        assert set(item.keys()) >= {
            "id",
            "price",
            "latitude",
            "longitude",
            "neighbourhood",
            "room_type",
        }


@pytest.mark.parametrize("limit,offset", [(5, 0), (5, 5)])
def test_listings_pagination(limit, offset, auth_headers):
    res = client.get(
        f"/api/v1/listings?limit={limit}&offset={offset}", headers=auth_headers
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= limit


@pytest.mark.parametrize("rt", ["Entire home/apt", "Private room"])
def test_listings_filter_room_type(rt, auth_headers):
    res = client.get(f"/api/v1/listings?room_type={rt}", headers=auth_headers)
    assert res.status_code == 200
    for item in res.json():
        assert item["room_type"] == rt


# --- Listing Detail ---


@pytest.mark.parametrize("invalid_id", [0, 9999999])
def test_listing_detail_not_found(invalid_id, auth_headers):
    res = client.get(f"/api/v1/listings/{invalid_id}", headers=auth_headers)
    assert res.status_code == 404


def test_listing_detail_found(auth_headers):
    # on prend un id existant
    res0 = client.get("/api/v1/listings?limit=1", headers=auth_headers)
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester detail")
    lid = data0[0]["id"]
    res = client.get(f"/api/v1/listings/{lid}", headers=auth_headers)
    assert res.status_code == 200
    detail = res.json()
    assert detail["id"] == lid
    assert set(detail.keys()) >= {
        "id",
        "price",
        "latitude",
        "longitude",
        "neighbourhood",
        "room_type",
    }


# --- Stats by neighbourhood ---


def test_stats_by_neigh_invalid(auth_headers):
    """Quartier inconnu → 404"""
    res = client.get("/api/v1/stats/InvalidNeighbourhood", headers=auth_headers)
    assert res.status_code == 404


def test_stats_by_neigh_valid(auth_headers):
    """Quartier valide → 200 + median_price & occupancy_pct floats"""
    # récupère un quartier via /listings
    res0 = client.get("/api/v1/listings?limit=1", headers=auth_headers)
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_by_neigh")
    neigh = data0[0]["neighbourhood"]

    res = client.get(f"/api/v1/stats/{neigh}", headers=auth_headers)
    assert res.status_code == 200
    stats = res.json()
    assert "median_price" in stats
    assert "occupancy_pct" in stats
    assert isinstance(stats["median_price"], float)
    assert isinstance(stats["occupancy_pct"], float)

# --- Stats history ---

def test_stats_history_invalid_neigh(auth_headers):
    """History pour un quartier inconnu → liste vide"""
    res = client.get("/api/v1/stats/InvalidNeighbourhood/history", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []

def test_stats_history_valid_neigh(auth_headers):
    res0 = client.get("/api/v1/listings?limit=1", headers=auth_headers)
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_history")
    neigh = data0[0]["neighbourhood"]

    res = client.get(f"/api/v1/stats/{neigh}/history", headers=auth_headers)
    assert res.status_code == 200
    hist = res.json()
    assert isinstance(hist, list)
    if hist:
        item = hist[0]
        expected_keys = {"median_price", "occupancy_pct"}
        assert expected_keys.issubset(item.keys())
        # period_id peut être str ou int
        assert isinstance(item["median_price"], float)
        assert isinstance(item["occupancy_pct"], float)
