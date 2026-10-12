"""
CinePulse Movie Discovery & Catalog REST API
Exposes endpoints for catalog browsing, weighted popular rankings, search, and similarity recommendations.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from ..recommender.engine import MovieNotFoundError, RecommenderEngine

router = APIRouter(tags=["movies"])

# Global recommender engine instance (injected via main lifespan)
engine: Optional[RecommenderEngine] = None

def get_engine() -> RecommenderEngine:
    if engine is None or not engine.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CinePulse NLP Recommendation Engine is not yet loaded or initialized."
        )
    return engine

class MovieSummary(BaseModel):
    id: int
    title: str = Field(alias="title")
    overview: str
    tagline: str
    release_date: str
    release_year: str
    runtime: int
    popularity: float
    vote_average: float
    vote_count: int
    weighted_rating: float
    genres: List[str]
    keywords: List[str]
    cast: List[str]
    director: Optional[str] = None
    similarity_score: Optional[float] = None
    recommendation_explanation: Optional[Dict[str, Any]] = None
    trailer_url: Optional[str] = None

class PaginatedMoviesResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int

@router.get("/movies", response_model=PaginatedMoviesResponse)
def list_movies(
    page: int = Query(default=1, ge=1, description="Page index (1-based)"),
    page_size: int = Query(default=20, ge=1, le=50, description="Items per page"),
    genre: Optional[str] = Query(default=None, description="Optional genre filter")
):
    """Returns a paginated list of movies from the catalog with optional genre filtering."""
    eng = get_engine()
    all_movies = list(eng.metadata_lookup.values())

    if genre:
        g_lower = genre.lower()
        all_movies = [m for m in all_movies if any(g.lower() == g_lower for g in m.get("genres", []))]

    total = len(all_movies)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    sliced = []
    for m in all_movies[start_idx:end_idx]:
        copy_m = dict(m)
        copy_m["weighted_rating"] = eng.calculate_weighted_rating(copy_m)
        sliced.append(copy_m)

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedMoviesResponse(
        items=sliced,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/movies/{movie_id}")
def get_movie_details(movie_id: int):
    """Fetches comprehensive metadata for a single film by unique TMDB ID."""
    eng = get_engine()
    try:
        movie = eng.get_movie_by_id(movie_id)
        # Mock trailer URL fallback for demo trailer view (YouTube official search link)
        safe_title = movie["title"].replace(" ", "+")
        movie["trailer_url"] = f"https://www.youtube.com/results?search_query={safe_title}+official+trailer"
        return movie
    except MovieNotFoundError:
        # Provide suggestions
        suggestions = eng.get_popular_movies(limit=3)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Movie with ID {movie_id} was not found in catalog.",
                "suggested_movies": [{"id": m["id"], "title": m["title"]} for m in suggestions]
            }
        )

@router.get("/movies/{movie_id}/similar")
def get_similar_movies(
    movie_id: int,
    limit: int = Query(default=10, ge=1, le=50, description="Max recommendations to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset")
):
    """
    Computes on-demand sparse cosine NLP similarity against the weighted metadata soup.
    Returns ranked similar films paired with truthful explainability metadata.
    """
    eng = get_engine()
    try:
        similar = eng.recommend_similar(movie_id, limit=limit, offset=offset)
        return similar
    except MovieNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} was not found in catalog."
        )

@router.get("/search")
def search_movies(
    q: str = Query(default="", description="Search query string"),
    genre: Optional[str] = Query(default=None, description="Optional genre filter"),
    limit: int = Query(default=24, ge=1, le=50, description="Maximum matches")
):
    """Case-insensitive, punctuation-tolerant ranked search across titles, directors, actors, and keywords."""
    eng = get_engine()
    return eng.search_movies(query=q, genre=genre, limit=limit)

@router.get("/popular")
def get_popular_movies(
    limit: int = Query(default=20, ge=1, le=50),
    genre: Optional[str] = Query(default=None)
):
    """Returns top movies ranked using the IMDb weighted rating benchmark formula."""
    eng = get_engine()
    return eng.get_popular_movies(limit=limit, genre=genre)

@router.get("/featured")
def get_featured_movie():
    """Returns the hero spotlight film for the homepage banner."""
    eng = get_engine()
    featured = eng.get_featured_movie()
    if not featured:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No featured movie available.")
    return featured

@router.get("/genres")
def get_genres():
    """Returns the full list of genres present in the catalog along with frequency counts."""
    eng = get_engine()
    return eng.get_genres()
