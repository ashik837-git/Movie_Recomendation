"""
Integration tests for CinePulse FastAPI Service
Validates API contracts, search, recommendation endpoints, watchlist isolation, and payment flows.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["catalog_loaded"] is True
    assert data["catalog_size"] > 0

def test_list_movies_pagination(client):
    res = client.get("/api/v1/movies?page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 10
    assert data["total"] == 40
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 4

def test_get_movie_details_and_404(client):
    res = client.get("/api/v1/movies/10001")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 10001
    assert data["title"] == "Quantum Horizon"
    assert "Science Fiction" in data["genres"]

    # Unknown ID returns 404 with suggestions
    res_404 = client.get("/api/v1/movies/999999")
    assert res_404.status_code == 404
    err_data = res_404.json()
    assert "suggested_movies" in err_data["detail"]

def test_similar_movies_with_explanations(client):
    res = client.get("/api/v1/movies/10001/similar?limit=5")
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) > 0

    # Self-exclusion
    assert all(r["id"] != 10001 for r in recs)

    top = recs[0]
    assert "similarity_score" in top
    assert "recommendation_explanation" in top
    explanation = top["recommendation_explanation"]
    assert "summary" in explanation
    assert "shared_genres" in explanation

def test_search_and_genre_filtering(client):
    res = client.get("/api/v1/search?q=quantum")
    assert res.status_code == 200
    results = res.json()
    assert len(results) >= 2
    assert any("Quantum Horizon" in r["title"] for r in results)

    # Genre filter search
    res_comedy = client.get("/api/v1/search?genre=Comedy")
    assert res_comedy.status_code == 200
    assert all("Comedy" in r["genres"] for r in res_comedy.json())

def test_popular_and_featured(client):
    res_pop = client.get("/api/v1/popular?limit=5")
    assert res_pop.status_code == 200
    assert len(res_pop.json()) == 5

    res_feat = client.get("/api/v1/featured")
    assert res_feat.status_code == 200
    assert "title" in res_feat.json()

def test_user_watchlist_isolation(client):
    headers_user_a = {"Authorization": "Bearer mock_user_alice"}
    headers_user_b = {"Authorization": "Bearer mock_user_bob"}

    # User A adds movie 10001
    add_a = client.post("/api/v1/user/watchlist", json={"movie_id": 10001}, headers=headers_user_a)
    assert add_a.status_code == 200

    # User B adds movie 10003
    add_b = client.post("/api/v1/user/watchlist", json={"movie_id": 10003}, headers=headers_user_b)
    assert add_b.status_code == 200

    # User A's watchlist has 10001, but NOT 10003
    get_a = client.get("/api/v1/user/watchlist", headers=headers_user_a)
    assert get_a.status_code == 200
    ids_a = [m["id"] for m in get_a.json()]
    assert 10001 in ids_a
    assert 10003 not in ids_a

    # User B's watchlist has 10003, but NOT 10001
    get_b = client.get("/api/v1/user/watchlist", headers=headers_user_b)
    assert get_b.status_code == 200
    ids_b = [m["id"] for m in get_b.json()]
    assert 10003 in ids_b
    assert 10001 not in ids_b

def test_payments_plans_and_checkout(client):
    plans_res = client.get("/api/v1/payments/plans")
    assert plans_res.status_code == 200
    plans = plans_res.json()
    assert len(plans) >= 3

    # Create checkout session
    checkout_res = client.post(
        "/api/v1/payments/create-checkout-session",
        json={
            "plan_id": "premium",
            "success_url": "http://localhost:3000/pricing?status=success",
            "cancel_url": "http://localhost:3000/pricing?status=canceled"
        }
    )
    assert checkout_res.status_code == 200
    checkout_data = checkout_res.json()
    assert "checkout_url" in checkout_data
    assert "session_id" in checkout_data

def test_webhook_idempotency(client):
    payload = b'{"id": "evt_test_123", "type": "checkout.session.completed"}'
    
    # First webhook submission
    res1 = client.post("/api/v1/payments/webhook", content=payload)
    assert res1.status_code == 200
    assert res1.json()["processed"] is True

    # Duplicate webhook submission
    res2 = client.post("/api/v1/payments/webhook", content=payload)
    assert res2.status_code == 200
    assert res2.json()["processed"] is False
    assert res2.json()["status"] == "duplicate"
