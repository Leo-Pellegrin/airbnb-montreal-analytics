# backend/tests/test_endpoints.py

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from sqlalchemy import select

from app.core.database import engine
from app.main import app
from app.models.calendar_weekly import calendar_weekly
from app.models.review import Reviews
from app.models.listing import Listings
from app.models.neighbourhoods import Neighbourhoods

client = TestClient(app)


def clean_db():
    from sqlalchemy import text

    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    clean_db()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Ajout d'un quartier de test
        test_neighbourhood = Neighbourhoods(neighbourhood="Test Neighbourhood 1")
        session.add(test_neighbourhood)
        session.commit()

        # Ajout d'un listing de test
        test_listing = Listings(
            id=1,
            host_id=1,
            price=100.0,
            latitude=45.5,
            longitude=-73.5,
            neighbourhood=test_neighbourhood.neighbourhood,
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

        review = Reviews(
            id=1,
            listing_id=1,
            date=date.today(),
            reviewer_id=1,
            reviewer_name="Test",
            comments="Bien",
        )
        print("DEBUG review à insérer:", review)

        session.add(review)
        session.commit()

    yield

    # clean_db()


# --- Health Check ---
def test_health_success():
    res = client.get(
        "/api/v1/health",
    )
    assert res.status_code == 200
    json = res.json()
    assert json.get("status") == "ok"
    # 'db' doit être un int (résultat de SELECT 1)
    assert isinstance(json.get("db"), int)


# --- Listings ---


def test_read_listings_default():
    res = client.get(
        "/api/v1/listings",
    )
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
def test_listings_pagination(
    limit,
    offset,
):
    res = client.get(
        f"/api/v1/listings?limit={limit}&offset={offset}",
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= limit


@pytest.mark.parametrize("rt", ["Entire home/apt", "Private room"])
def test_listings_filter_room_type(
    rt,
):
    res = client.get(
        f"/api/v1/listings?room_type={rt}",
    )
    assert res.status_code == 200
    for item in res.json():
        assert item["room_type"] == rt


# --- Listing Detail ---


@pytest.mark.parametrize("invalid_id", [0, 9999999])
def test_listing_detail_not_found(
    invalid_id,
):
    res = client.get(
        f"/api/v1/listings/{invalid_id}",
    )
    assert res.status_code == 404


def test_listing_detail_found():
    # on prend un id existant
    res0 = client.get(
        "/api/v1/listings?limit=1",
    )
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester detail")
    lid = data0[0]["id"]
    res = client.get(
        f"/api/v1/listings/{lid}",
    )
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


def test_stats_by_neigh_invalid():
    """Quartier inconnu → 404"""
    res = client.get(
        "/api/v1/stats/InvalidNeighbourhood",
    )
    assert res.status_code == 404


def test_stats_by_neigh_valid():
    """Quartier valide → 200 + median_price & occupancy_pct floats"""
    # récupère un quartier via /listings
    res0 = client.get(
        "/api/v1/listings?limit=1",
    )
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_by_neigh")
    neigh = data0[0]["neighbourhood"]

    res = client.get(
        f"/api/v1/stats/{neigh}",
    )
    assert res.status_code == 200
    stats = res.json()
    assert "median_price" in stats
    assert "occupancy_pct" in stats
    assert isinstance(stats["median_price"], float)
    assert isinstance(stats["occupancy_pct"], float)


# --- Stats history ---


def test_stats_history_invalid_neigh():
    """History pour un quartier inconnu → liste vide"""
    res = client.get(
        "/api/v1/stats/InvalidNeighbourhood/history",
    )
    assert res.status_code == 200
    assert res.json() == []


def test_stats_history_valid_neigh():
    res0 = client.get(
        "/api/v1/listings?limit=1",
    )
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_history")
    neigh = data0[0]["neighbourhood"]

    res = client.get(
        f"/api/v1/stats/{neigh}/history",
    )
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


# --- Neighbourhoods ---
def test_read_neighbourhoods():
    res = client.get("/api/v1/neighbourhoods")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # Doit contenir au moins le quartier de test
    assert "Test Neighbourhood 1" in data


def test_read_neighbourhoods_empty(monkeypatch):
    # Monkeypatch Listings pour simuler aucun quartier
    orig_exec = Session.exec

    def fake_exec(self, *a, **kw):
        class FakeResult:
            def all(self):
                return []

        return FakeResult()

    monkeypatch.setattr(Session, "exec", fake_exec)
    res = client.get("/api/v1/neighbourhoods")
    assert res.status_code == 200
    assert res.json() == []
    monkeypatch.setattr(Session, "exec", orig_exec)


# --- Reviews for Listing ---
def test_reviews_for_listing_success():
    res = client.get("/api/v1/listings/1/reviews")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(r["reviewer_name"] == "Test" for r in data)


def test_reviews_for_listing_not_found():
    res = client.get("/api/v1/listings/999999/reviews")
    assert res.status_code == 200
    assert res.json() == []


def test_reviews_for_listing_empty():
    # Ajoute un listing sans review
    from app.models.listing import Listings

    with Session(engine) as session:
        listing = Listings(
            id=12345,
            price=10,
            latitude=0,
            longitude=0,
            neighbourhood="Test Neighbourhood 1",
            room_type="Test",
            host_id=1,
        )
        session.add(listing)
        session.commit()
    res = client.get("/api/v1/listings/12345/reviews")
    assert res.status_code == 200
    assert res.json() == []


def test_debug_all_neighs():
    from app.models.neighbourhoods import Neighbourhoods

    with Session(engine) as session:
        all_neighs = session.exec(select(Neighbourhoods)).all()
        print("DEBUG ALL NEIGHS:", all_neighs)
