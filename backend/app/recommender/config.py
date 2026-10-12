"""
Recommender Engine Configuration
Defines weights, extraction limits, tokenization parameters, and version hashes.
All weights and parameters are documented with rationale.
"""
from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class RecommenderConfig:
    # Feature document weights
    # Director: weight 3 -> Auteur theory: a director's style strongly dictates tone and cinematography
    director_weight: int = 3
    
    # Genres: weight 2 -> Broad category alignment (e.g., Sci-Fi, Crime, Romance)
    genre_weight: int = 2
    
    # Keywords: weight 2 -> Granular motifs (e.g., 'dystopia', 'heist', 'time dilation')
    keyword_weight: int = 2
    
    # Cast: weight 1 -> Actor presence adds subtle connective tissue across films
    cast_weight: int = 1
    
    # Overview: weight 1 -> Plot vocabulary captures semantic context
    overview_weight: int = 1
    
    # Feature extraction limits
    top_cast_limit: int = 5
    top_keywords_limit: int = 10
    
    # Vectorizer parameters
    ngram_range: tuple = (1, 2)
    max_features: int = 25000
    min_df: int = 1
    sublinear_tf: bool = True
    
    # Engine defaults
    default_top_k: int = 10
    max_top_k: int = 50
    
    # Version identifier
    engine_version: str = "2.0.0-cinepulse"

    def compute_hash(self) -> str:
        """Computes a deterministic hash of all hyperparameter configurations."""
        payload = {
            "director_weight": self.director_weight,
            "genre_weight": self.genre_weight,
            "keyword_weight": self.keyword_weight,
            "cast_weight": self.cast_weight,
            "overview_weight": self.overview_weight,
            "top_cast_limit": self.top_cast_limit,
            "top_keywords_limit": self.top_keywords_limit,
            "ngram_range": list(self.ngram_range),
            "max_features": self.max_features,
            "min_df": self.min_df,
            "sublinear_tf": self.sublinear_tf,
            "engine_version": self.engine_version,
        }
        raw_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()[:16]

DEFAULT_CONFIG = RecommenderConfig()
