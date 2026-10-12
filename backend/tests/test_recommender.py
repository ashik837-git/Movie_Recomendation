"""
Unit tests for CinePulse NLP Recommendation Engine
Tests feature preprocessing, JSON parsing resilience, sparse vectorization,
self-exclusion, and truthful explainability.
"""
import pytest
from pathlib import Path
import numpy as np

from app.recommender.config import DEFAULT_CONFIG, RecommenderConfig
from app.recommender.builder import (
    safe_parse_json_list,
    safe_extract_director,
    normalize_entity_token,
    clean_overview_text,
    CatalogBuilder
)
from app.recommender.engine import RecommenderEngine, MovieNotFoundError

def test_safe_parse_json_list():
    # Valid JSON string
    valid_json = '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'
    assert safe_parse_json_list(valid_json) == ["Action", "Adventure"]

    # Malformed JSON string
    malformed = '[{"id": 28, "name": "Action"'
    assert safe_parse_json_list(malformed) == []

    # None / Empty
    assert safe_parse_json_list(None) == []
    assert safe_parse_json_list("") == []

def test_safe_extract_director():
    crew_json = '[{"job": "Producer", "name": "Jerry Bruckheimer"}, {"job": "Director", "name": "Denis Villeneuve"}]'
    assert safe_extract_director(crew_json) == "Denis Villeneuve"

    # No director in crew
    crew_no_dir = '[{"job": "Editor", "name": "Joe Walker"}]'
    assert safe_extract_director(crew_no_dir) is None

    # Malformed
    assert safe_extract_director("{bad json") is None

def test_normalize_entity_token():
    # Lowercase and strip whitespace
    assert normalize_entity_token("Christopher Nolan") == "christophernolan"
    assert normalize_entity_token("Science Fiction") == "sciencefiction"
    assert normalize_entity_token("Jean-Luc Moreau") == "jeanlucmoreau"
    assert normalize_entity_token("") == ""

def test_clean_overview_text():
    raw_text = "A bold group of astronauts travels through the deep mysterious space."
    cleaned = clean_overview_text(raw_text)
    # Stop words like 'a', 'of', 'through', 'the' should be stripped
    assert "bold" in cleaned
    assert "astronauts" in cleaned
    assert "deep" in cleaned
    assert "space" in cleaned
    assert " the " not in f" {cleaned} "

def test_engine_recommendations_and_self_exclusion():
    artifacts_path = Path(__file__).resolve().parent.parent / "app" / "recommender" / "artifacts" / "catalog_nlp_bundle.joblib"
    engine = RecommenderEngine(artifact_path=artifacts_path)
    assert engine.is_loaded is True
    assert engine.catalog_size == 40

    # Query 'Quantum Horizon' (ID 10001)
    target_id = 10001
    target_movie = engine.get_movie_by_id(target_id)
    assert target_movie["title"] == "Quantum Horizon"

    # Fetch recommendations
    recs = engine.recommend_similar(target_id, limit=5)
    assert len(recs) > 0

    # Verify self-exclusion: target movie must NEVER appear in recommendations
    rec_ids = [r["id"] for r in recs]
    assert target_id not in rec_ids

    # Verify #1 recommendation is the franchise sequel 'Quantum Horizon: Singularity' (ID 10002)
    assert recs[0]["id"] == 10002
    assert "Singularity" in recs[0]["title"]
    assert recs[0]["similarity_score"] > 0.0

    # Verify truthful explanations
    explanation = recs[0]["recommendation_explanation"]
    assert explanation["same_director"] is True
    assert explanation["director"] == "Elena Vance"
    assert "Science Fiction" in explanation["shared_genres"]
    assert len(explanation["shared_cast"]) > 0

def test_unknown_movie_raises_404():
    artifacts_path = Path(__file__).resolve().parent.parent / "app" / "recommender" / "artifacts" / "catalog_nlp_bundle.joblib"
    engine = RecommenderEngine(artifact_path=artifacts_path)

    with pytest.raises(MovieNotFoundError):
        engine.get_movie_by_id(999999)

    with pytest.raises(MovieNotFoundError):
        engine.find_movie_id_by_title("Non Existent Movie Title ABC 123")
