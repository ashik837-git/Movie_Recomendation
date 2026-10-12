"""
CinePulse Recommendation Engine
In-memory sparse cosine similarity execution with truthful explanations.
Zero web/database framework dependencies.
"""
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
from scipy.sparse import csr_matrix

from .config import RecommenderConfig, DEFAULT_CONFIG

logger = logging.getLogger("cinepulse.recommender.engine")

class ArtifactCompatibilityError(Exception):
    """Raised when serialized NLP artifacts are missing, corrupt, or incompatible."""
    pass

class MovieNotFoundError(Exception):
    """Raised when a queried movie ID or title cannot be resolved."""
    pass

class RecommenderEngine:
    def __init__(self, artifact_path: Optional[Path] = None, config: RecommenderConfig = DEFAULT_CONFIG):
        self.config = config
        self.artifact_path = artifact_path
        self.is_loaded = False
        
        # In-memory artifact state
        self.tfidf_matrix: Optional[csr_matrix] = None
        self.vectorizer: Any = None
        self.id_to_idx: Dict[int, int] = {}
        self.idx_to_id: Dict[int, int] = {}
        self.title_to_ids: Dict[str, List[int]] = {}
        self.metadata_lookup: Dict[int, Dict[str, Any]] = {}
        self.catalog_size: int = 0
        self.config_hash: str = ""
        self.data_hash: str = ""
        self.build_timestamp: str = ""
        
        # Weighted rating benchmarks computed upon loading
        self.c_mean_rating: float = 0.0
        self.m_min_votes: float = 0.0
        
        if artifact_path and artifact_path.exists():
            self.load_artifacts(artifact_path)

    def load_artifacts(self, artifact_path: Path) -> None:
        """Loads and verifies the serialized TF-IDF artifact bundle."""
        if not artifact_path.exists():
            raise ArtifactCompatibilityError(
                f"Artifact file not found at: {artifact_path}. "
                "Run 'python scripts/build_catalog.py' to generate artifacts."
            )

        try:
            bundle = joblib.load(artifact_path)
        except Exception as e:
            raise ArtifactCompatibilityError(f"Failed to unpickle artifact bundle: {e}")

        # Check required bundle keys
        required_keys = [
            "tfidf_matrix", "id_to_idx", "idx_to_id", "title_to_ids",
            "metadata_lookup", "config_hash", "data_hash"
        ]
        missing = [k for k in required_keys if k not in bundle]
        if missing:
            raise ArtifactCompatibilityError(f"Artifact bundle is corrupted, missing keys: {missing}")

        self.tfidf_matrix = bundle["tfidf_matrix"]
        self.vectorizer = bundle.get("vectorizer")
        self.id_to_idx = bundle["id_to_idx"]
        self.idx_to_id = bundle["idx_to_id"]
        self.title_to_ids = bundle["title_to_ids"]
        self.metadata_lookup = bundle["metadata_lookup"]
        self.catalog_size = len(self.id_to_idx)
        self.config_hash = bundle["config_hash"]
        self.data_hash = bundle["data_hash"]
        self.build_timestamp = bundle.get("build_timestamp", "")

        # Verify config hash
        current_config_hash = self.config.compute_hash()
        if self.config_hash != current_config_hash:
            logger.warning(
                f"Artifact config hash ({self.config_hash}) differs from current config ({current_config_hash}). "
                "Consider rebuilding catalog with scripts/build_catalog.py."
            )

        # Precompute IMDb weighted rating benchmarks
        self._compute_rating_benchmarks()
        self.is_loaded = True
        logger.info(f"RecommenderEngine successfully loaded {self.catalog_size} movies into sparse memory.")

    def _compute_rating_benchmarks(self) -> None:
        """Computes C (mean vote average) and m (90th percentile vote count)."""
        vote_counts = [m["vote_count"] for m in self.metadata_lookup.values()]
        vote_averages = [m["vote_average"] for m in self.metadata_lookup.values()]

        if vote_counts and vote_averages:
            self.c_mean_rating = float(np.mean(vote_averages))
            # 90th percentile threshold
            self.m_min_votes = float(np.percentile(vote_counts, 85)) if len(vote_counts) >= 10 else 1.0
        else:
            self.c_mean_rating = 6.0
            self.m_min_votes = 100.0

    def calculate_weighted_rating(self, movie: Dict[str, Any]) -> float:
        """
        Calculates the IMDb weighted rating:
        W = (v / (v + m)) * R + (m / (v + m)) * C
        """
        v = float(movie.get("vote_count", 0))
        r = float(movie.get("vote_average", 0))
        m = self.m_min_votes
        c = self.c_mean_rating
        if v + m == 0:
            return 0.0
        weighted = (v / (v + m)) * r + (m / (v + m)) * c
        return round(float(weighted), 2)

    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """Fetches movie metadata by ID or raises MovieNotFoundError."""
        if movie_id not in self.metadata_lookup:
            raise MovieNotFoundError(f"Movie ID {movie_id} was not found in catalog.")
        movie = dict(self.metadata_lookup[movie_id])
        movie["weighted_rating"] = self.calculate_weighted_rating(movie)
        return movie

    def find_movie_id_by_title(self, title: str) -> int:
        """Looks up movie ID by title with case-insensitivity and year disambiguation."""
        norm_title = title.lower().strip()
        ids = self.title_to_ids.get(norm_title)
        if not ids:
            # Substring match attempt
            for t, ids_list in self.title_to_ids.items():
                if norm_title in t or t in norm_title:
                    return ids_list[0]
            raise MovieNotFoundError(f"Movie titled '{title}' was not found in catalog.")
        return ids[0]

    def recommend_similar(self, movie_id: int, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Computes on-demand sparse cosine similarity for the requested movie.
        Excludes the movie itself, enforces maximum limits, and generates truthful explanations.
        """
        if not self.is_loaded or self.tfidf_matrix is None:
            raise ArtifactCompatibilityError("Recommender engine is not initialized with valid artifacts.")

        if movie_id not in self.id_to_idx:
            raise MovieNotFoundError(f"Movie with ID {movie_id} not found in index.")

        target_idx = self.id_to_idx[movie_id]
        target_meta = self.metadata_lookup[movie_id]

        # Extract target sparse vector (1, num_features)
        target_vec = self.tfidf_matrix[target_idx]

        # Sparse dot product with all movies (N, 1) -> (N,)
        scores = self.tfidf_matrix.dot(target_vec.T).toarray().ravel()

        # Exclude self
        scores[target_idx] = -1.0

        # Cap limit
        limit = min(limit, self.config.max_top_k)
        total_needed = offset + limit

        if total_needed >= len(scores):
            top_k_indices = np.argsort(-scores)
        else:
            # Fast partial sort using argpartition
            partitioned = np.argpartition(scores, -total_needed)[-total_needed:]
            top_k_indices = partitioned[np.argsort(-scores[partitioned])]

        results = []
        for idx in top_k_indices[offset:total_needed]:
            score = float(scores[idx])
            if score <= 0.0:
                continue

            cand_id = self.idx_to_id[idx]
            cand_meta = dict(self.metadata_lookup[cand_id])
            cand_meta["similarity_score"] = round(score, 4)
            cand_meta["weighted_rating"] = self.calculate_weighted_rating(cand_meta)

            # Compute truthful explanations from metadata intersection
            explanation = self._build_truthful_explanation(target_meta, cand_meta)
            cand_meta["recommendation_explanation"] = explanation

            results.append(cand_meta)

        return results

    def _build_truthful_explanation(self, target: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Derives truthful shared attributes without fabricating reasons."""
        target_genres = set(target.get("genres", []))
        cand_genres = set(candidate.get("genres", []))
        shared_genres = sorted(list(target_genres & cand_genres))

        target_keywords = set(target.get("keywords", []))
        cand_keywords = set(candidate.get("keywords", []))
        shared_keywords = sorted(list(target_keywords & cand_keywords))

        target_cast = set(target.get("cast", []))
        cand_cast = set(candidate.get("cast", []))
        shared_cast = sorted(list(target_cast & cand_cast))

        t_dir = target.get("director")
        c_dir = candidate.get("director")
        same_director = bool(t_dir and c_dir and t_dir == c_dir)

        # Build dynamic readable rationale
        reasons = []
        if same_director:
            reasons.append(f"Directed by {t_dir}")
        if shared_cast:
            reasons.append(f"Starring {', '.join(shared_cast[:2])}")
        if shared_genres:
            reasons.append(f"Shared genres: {', '.join(shared_genres[:2])}")
        if shared_keywords:
            reasons.append(f"Matching themes: {', '.join(shared_keywords[:2])}")

        summary = " • ".join(reasons) if reasons else "Similar narrative themes & plot motifs"

        return {
            "same_director": same_director,
            "director": t_dir if same_director else None,
            "shared_cast": shared_cast,
            "shared_genres": shared_genres,
            "shared_keywords": shared_keywords,
            "summary": summary
        }

    def search_movies(self, query: str, genre: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Case-insensitive, punctuation-tolerant substring and token search."""
        if not query and not genre:
            return []

        q_clean = re.sub(r"[^a-zA-Z0-9\s]", "", query.lower()).strip() if query else ""
        q_tokens = q_clean.split()

        matched = []
        for movie_id, meta in self.metadata_lookup.items():
            # Genre filter check
            if genre:
                movie_genres = [g.lower() for g in meta.get("genres", [])]
                if genre.lower() not in movie_genres:
                    continue

            if not q_clean:
                matched.append((0, meta))
                continue

            score = 0
            title_clean = re.sub(r"[^a-zA-Z0-9\s]", "", meta["title"].lower())
            
            # Exact title match
            if title_clean == q_clean:
                score += 100
            elif title_clean.startswith(q_clean):
                score += 50
            elif q_clean in title_clean:
                score += 30

            # Director match
            if meta.get("director") and q_clean in meta["director"].lower():
                score += 25

            # Actor match
            for actor in meta.get("cast", []):
                if q_clean in actor.lower():
                    score += 20
                    break

            # Keyword match
            for kw in meta.get("keywords", []):
                if q_clean in kw.lower():
                    score += 10
                    break

            # Token overlap in title / overview
            for tok in q_tokens:
                if tok in title_clean:
                    score += 5
                elif tok in meta.get("overview", "").lower():
                    score += 1

            if score > 0:
                matched.append((score, meta))

        # Sort by match score descending, then by popularity
        matched.sort(key=lambda item: (item[0], item[1].get("popularity", 0.0)), reverse=True)

        results = []
        for _, m in matched[:limit]:
            copy_m = dict(m)
            copy_m["weighted_rating"] = self.calculate_weighted_rating(copy_m)
            results.append(copy_m)
        return results

    def get_popular_movies(self, limit: int = 20, genre: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns top movies ranked using the IMDb Weighted Rating formula."""
        filtered = []
        for meta in self.metadata_lookup.values():
            if genre:
                genres_lower = [g.lower() for g in meta.get("genres", [])]
                if genre.lower() not in genres_lower:
                    continue
            copy_m = dict(meta)
            copy_m["weighted_rating"] = self.calculate_weighted_rating(copy_m)
            filtered.append(copy_m)

        # Sort by weighted rating descending, secondary by popularity
        filtered.sort(key=lambda m: (m["weighted_rating"], m.get("popularity", 0.0)), reverse=True)
        return filtered[:limit]

    def get_featured_movie(self) -> Optional[Dict[str, Any]]:
        """Returns the spotlight movie with high rating, votes, and synopsis."""
        popular = self.get_popular_movies(limit=10)
        for m in popular:
            if len(m.get("overview", "")) > 50:
                return m
        return popular[0] if popular else None

    def get_genres(self) -> List[Dict[str, Any]]:
        """Returns all distinct genres with frequency counts."""
        genre_counts: Dict[str, int] = {}
        for meta in self.metadata_lookup.values():
            for g in meta.get("genres", []):
                genre_counts[g] = genre_counts.get(g, 0) + 1
        return [{"name": name, "count": count} for name, count in sorted(genre_counts.items(), key=lambda x: -x[1])]
