"""
CinePulse User Watchlist & Interaction API
Secured with Supabase JWT authentication. Derives user from verified token.
"""
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..auth.jwt_validator import AuthenticatedUser, get_current_user
from .movies import get_engine

router = APIRouter(prefix="/user", tags=["user"])

# In-memory stores for isolated dev sessions (synced to Supabase when active)
USER_WATCHLISTS: Dict[str, List[int]] = {}
USER_HISTORIES: Dict[str, List[int]] = {}

class WatchlistRequest(BaseModel):
    movie_id: int

class HistoryRequest(BaseModel):
    movie_id: int

@router.get("/watchlist")
def get_user_watchlist(current_user: AuthenticatedUser = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """Returns the authenticated user's watchlist with full movie metadata."""
    eng = get_engine()
    user_movie_ids = USER_WATCHLISTS.get(current_user.user_id, [])
    
    items = []
    for m_id in user_movie_ids:
        try:
            m = eng.get_movie_by_id(m_id)
            items.append(m)
        except Exception:
            continue
    return items

@router.post("/watchlist")
def add_to_watchlist(
    body: WatchlistRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Adds a movie to the authenticated user's watchlist."""
    eng = get_engine()
    # Verify movie exists
    try:
        eng.get_movie_by_id(body.movie_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie ID not found in catalog.")

    if current_user.user_id not in USER_WATCHLISTS:
        USER_WATCHLISTS[current_user.user_id] = []

    if body.movie_id not in USER_WATCHLISTS[current_user.user_id]:
        USER_WATCHLISTS[current_user.user_id].append(body.movie_id)

    return {"success": True, "movie_id": body.movie_id, "user_id": current_user.user_id}

@router.delete("/watchlist/{movie_id}")
def remove_from_watchlist(
    movie_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Removes a movie from the authenticated user's watchlist."""
    if current_user.user_id in USER_WATCHLISTS:
        USER_WATCHLISTS[current_user.user_id] = [
            m for m in USER_WATCHLISTS[current_user.user_id] if m != movie_id
        ]
    return {"success": True, "movie_id": movie_id}

@router.get("/history")
def get_user_history(current_user: AuthenticatedUser = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """Returns the user's recently viewed movies."""
    eng = get_engine()
    hist_ids = USER_HISTORIES.get(current_user.user_id, [])
    
    items = []
    for m_id in reversed(hist_ids[-20:]):
        try:
            m = eng.get_movie_by_id(m_id)
            items.append(m)
        except Exception:
            continue
    return items

@router.post("/history")
def record_user_history(
    body: HistoryRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Records a viewed movie for the authenticated user."""
    if current_user.user_id not in USER_HISTORIES:
        USER_HISTORIES[current_user.user_id] = []

    # Move to end
    if body.movie_id in USER_HISTORIES[current_user.user_id]:
        USER_HISTORIES[current_user.user_id].remove(body.movie_id)
    USER_HISTORIES[current_user.user_id].append(body.movie_id)

    return {"success": True, "movie_id": body.movie_id}
