# backend/tests/test_endpoints.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# --- Health Check ---

def test_health_success():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    json = res.json()
    assert json.get("status") == "ok"
    # 'db' doit être un int (résultat de SELECT 1)
    assert isinstance(json.get("db"), int)


# --- Listings ---

def test_read_listings_default():
    res = client.get("/api/v1/listings")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # par défaut, max 20 résultats
    assert len(data) <= 20
    if data:
        item = data[0]
        # clés essentielles présentes
        assert set(item.keys()) >= {
            "id", "price", "latitude", "longitude", "neighbourhood", "room_type"
        }


@pytest.mark.parametrize("limit,offset", [(5, 0), (5, 5)])
def test_listings_pagination(limit, offset):
    res = client.get(f"/api/v1/listings?limit={limit}&offset={offset}")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= limit


@pytest.mark.parametrize("rt", ["Entire home/apt", "Private room"])
def test_listings_filter_room_type(rt):
    res = client.get(f"/api/v1/listings?room_type={rt}")
    assert res.status_code == 200
    for item in res.json():
        assert item["room_type"] == rt


# --- Listing Detail ---

@pytest.mark.parametrize("invalid_id", [0, 9999999])
def test_listing_detail_not_found(invalid_id):
    res = client.get(f"/api/v1/listings/{invalid_id}")
    assert res.status_code == 404


def test_listing_detail_found():
    # on prend un id existant
    res0 = client.get("/api/v1/listings?limit=1")
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester detail")
    lid = data0[0]["id"]
    res = client.get(f"/api/v1/listings/{lid}")
    assert res.status_code == 200
    detail = res.json()
    assert detail["id"] == lid
    assert set(detail.keys()) >= {
        "id", "price", "latitude", "longitude", "neighbourhood", "room_type"
    }


# --- Stats by neighbourhood ---

def test_stats_by_neigh_invalid():
    """Quartier inconnu → 404"""
    res = client.get("/api/v1/stats/InvalidNeighbourhood")
    assert res.status_code == 404


def test_stats_by_neigh_valid():
    """Quartier valide → 200 + median_price & occupancy_pct floats"""
    # récupère un quartier via /listings
    res0 = client.get("/api/v1/listings?limit=1")
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_by_neigh")
    neigh = data0[0]["neighbourhood"]

    res = client.get(f"/api/v1/stats/{neigh}")
    assert res.status_code == 200
    stats = res.json()
    assert "median_price" in stats
    assert "occupancy_pct" in stats
    assert isinstance(stats["median_price"], float)
    assert isinstance(stats["occupancy_pct"], float)


# --- Stats history ---

def test_stats_history_invalid_neigh():
    """History pour un quartier inconnu → liste vide"""
    res = client.get("/api/v1/stats/InvalidNeighbourhood/history")
    assert res.status_code == 200
    assert res.json() == []


def test_stats_history_valid_neigh():
    """History pour un quartier valide → liste d’items avec period_id, median_price, occupancy_pct"""
    res0 = client.get("/api/v1/listings?limit=1")
    data0 = res0.json()
    if not data0:
        pytest.skip("Aucun listing dispo pour tester stats_history")
    neigh = data0[0]["neighbourhood"]

    res = client.get(f"/api/v1/stats/{neigh}/history")
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