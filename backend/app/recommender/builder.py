"""
CinePulse Catalog & Feature Matrix Builder
Pure NLP & data pipeline module (zero web / DB imports).
Parses raw metadata, constructs weighted token soups, and serializes sparse TF-IDF artifacts.
"""
from datetime import datetime, timezone
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

from .config import RecommenderConfig, DEFAULT_CONFIG

logger = logging.getLogger("cinepulse.recommender.builder")
logging.basicConfig(level=logging.INFO)

# Regex to strip unwanted punctuation but retain alphanumeric characters
TOKEN_CLEAN_RE = re.compile(r"[^a-zA-Z0-9]")

def safe_parse_json_list(value: Any, key: str = "name") -> List[str]:
    """Safely extracts a list of string values from a JSON string column without eval()."""
    if pd.isna(value) or not value:
        return []
    if isinstance(value, list):
        return [str(item.get(key, "")) for item in value if isinstance(item, dict) and key in item]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                res = []
                for item in parsed:
                    if isinstance(item, dict) and key in item and item[key]:
                        res.append(str(item[key]).strip())
                return res
        except (json.JSONDecodeError, TypeError, ValueError):
            return []
    return []

def safe_extract_director(crew_value: Any) -> Optional[str]:
    """Extracts the first director name from the crew JSON list safely."""
    if pd.isna(crew_value) or not crew_value:
        return None
    if isinstance(crew_value, str):
        try:
            crew_list = json.loads(crew_value)
            if isinstance(crew_list, list):
                for member in crew_list:
                    if isinstance(member, dict) and member.get("job") == "Director":
                        name = member.get("name")
                        if name:
                            return str(name).strip()
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
    elif isinstance(crew_value, list):
        for member in crew_value:
            if isinstance(member, dict) and member.get("job") == "Director":
                name = member.get("name")
                if name:
                    return str(name).strip()
    return None

def normalize_entity_token(text: str) -> str:
    """
    Normalizes multi-word entity names to avoid spurious unigram collisions.
    Example: 'Johnny Depp' -> 'johnnydepp', 'Science Fiction' -> 'sciencefiction'
    """
    if not text:
        return ""
    # Lowercase and remove all whitespace and punctuation
    cleaned = TOKEN_CLEAN_RE.sub("", text.lower())
    return cleaned

def clean_overview_text(text: str) -> str:
    """Normalizes synopsis text, lowers case, and filters English stopwords."""
    if pd.isna(text) or not text:
        return ""
    # Lowercase and tokenize
    words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    filtered = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return " ".join(filtered)

class CatalogBuilder:
    def __init__(self, config: RecommenderConfig = DEFAULT_CONFIG):
        self.config = config

    def load_and_merge_datasets(self, movies_path: Path, credits_path: Path) -> pd.DataFrame:
        """Loads movies and credits CSVs and performs a strict join on movie ID."""
        logger.info(f"Loading movies from {movies_path} and credits from {credits_path}")
        movies_df = pd.read_csv(movies_path, low_memory=False)
        credits_df = pd.read_csv(credits_path, low_memory=False)

        # Standardize ID column types
        movies_df["id"] = pd.to_numeric(movies_df["id"], errors="coerce")
        movies_df = movies_df.dropna(subset=["id"])
        movies_df["id"] = movies_df["id"].astype(int)

        # Credits may have 'movie_id' or 'id'
        if "movie_id" in credits_df.columns:
            credits_df["movie_id"] = pd.to_numeric(credits_df["movie_id"], errors="coerce")
            credits_df = credits_df.dropna(subset=["movie_id"])
            credits_df["movie_id"] = credits_df["movie_id"].astype(int)
            join_col = "movie_id"
        elif "id" in credits_df.columns:
            credits_df["id"] = pd.to_numeric(credits_df["id"], errors="coerce")
            credits_df = credits_df.dropna(subset=["id"])
            credits_df["id"] = credits_df["id"].astype(int)
            join_col = "id"
        else:
            raise ValueError("Credits dataset missing both 'movie_id' and 'id' columns.")

        # Drop duplicate titles or conflicting columns in credits before merge
        credits_drop = [c for c in ["title", "tittle"] if c in credits_df.columns]
        credits_subset = credits_df.drop(columns=credits_drop)

        # Strict inner join on ID, never on title
        merged = movies_df.merge(credits_subset, left_on="id", right_on=join_col, how="inner")
        
        # Deduplicate on ID (keep first occurrence)
        merged = merged.drop_duplicates(subset=["id"]).reset_index(drop=True)
        logger.info(f"Successfully merged {len(merged)} unique movie records on ID.")
        return merged

    def preprocess_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parses structured JSON strings, extracts entities, and normalizes fields."""
        df = df.copy()

        # Handle missing titles
        df["title"] = df["title"].fillna("Untitled").astype(str).str.strip()

        # Extract release year for disambiguation
        df["release_year"] = df["release_date"].apply(
            lambda d: str(d).split("-")[0] if pd.notna(d) and str(d).strip() else "Unknown"
        )

        # Parse entities
        logger.info("Extracting genres, keywords, cast, and director entities...")
        df["raw_genres"] = df["genres"].apply(lambda v: safe_parse_json_list(v, key="name"))
        df["raw_keywords"] = df["keywords"].apply(lambda v: safe_parse_json_list(v, key="name")[:self.config.top_keywords_limit])
        df["raw_cast"] = df["cast"].apply(lambda v: safe_parse_json_list(v, key="name")[:self.config.top_cast_limit])
        df["raw_director"] = df["crew"].apply(safe_extract_director)

        # Fill missing text fields cleanly
        df["overview"] = df["overview"].fillna("").astype(str)
        df["tagline"] = df["tagline"].fillna("").astype(str)
        df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce").fillna(0.0)
        df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce").fillna(0).astype(int)
        df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce").fillna(0.0)
        df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce").fillna(0).astype(int)

        # Normalized entity tokens
        df["clean_director"] = df["raw_director"].apply(lambda d: normalize_entity_token(d) if d else "")
        df["clean_cast"] = df["raw_cast"].apply(lambda names: [normalize_entity_token(n) for n in names if n])
        df["clean_genres"] = df["raw_genres"].apply(lambda names: [normalize_entity_token(n) for n in names if n])
        df["clean_keywords"] = df["raw_keywords"].apply(lambda names: [normalize_entity_token(n) for n in names if n])
        df["clean_overview"] = df["overview"].apply(clean_overview_text)

        return df

    def construct_metadata_soup(self, df: pd.DataFrame) -> List[str]:
        """
        Constructs the weighted document soup for each film using configurable field weights.
        Director tokens are repeated (default x3)
        Genre tokens are repeated (default x2)
        Keyword tokens are repeated (default x2)
        Cast tokens are added (default x1)
        Cleaned overview tokens are added (default x1)
        """
        soups = []
        for _, row in df.iterrows():
            tokens = []

            # Director (weighted)
            if row["clean_director"]:
                tokens.extend([row["clean_director"]] * self.config.director_weight)

            # Genres (weighted)
            for g in row["clean_genres"]:
                tokens.extend([g] * self.config.genre_weight)

            # Keywords (weighted)
            for k in row["clean_keywords"]:
                tokens.extend([k] * self.config.keyword_weight)

            # Cast (weighted)
            for c in row["clean_cast"]:
                tokens.extend([c] * self.config.cast_weight)

            # Overview tokens
            if row["clean_overview"]:
                overview_part = (" " + row["clean_overview"]) * self.config.overview_weight
                tokens.append(overview_part)

            document = " ".join(tokens)
            soups.append(document.strip())
        return soups

    def build_and_save_artifacts(self, movies_path: Path, credits_path: Path, output_dir: Path) -> Path:
        """Executes full pipeline and writes validated joblib bundle to disk."""
        output_dir.mkdir(parents=True, exist_ok=True)
        merged_df = self.load_and_merge_datasets(movies_path, credits_path)
        processed_df = self.preprocess_metadata(merged_df)
        documents = self.construct_metadata_soup(processed_df)

        logger.info(f"Fitting TfidfVectorizer on {len(documents)} document soups...")
        vectorizer = TfidfVectorizer(
            ngram_range=self.config.ngram_range,
            max_features=self.config.max_features,
            min_df=self.config.min_df,
            sublinear_tf=self.config.sublinear_tf,
            norm="l2"  # L2 normalization ensures sparse dot product == cosine similarity
        )
        tfidf_matrix = vectorizer.fit_transform(documents)
        logger.info(f"TF-IDF sparse matrix built: shape {tfidf_matrix.shape}, non-zero elements: {tfidf_matrix.nnz}")

        # Index maps
        id_to_idx = {int(row["id"]): idx for idx, row in processed_df.iterrows()}
        idx_to_id = {idx: int(row["id"]) for idx, row in processed_df.iterrows()}

        # Disambiguated title lookup
        title_to_ids: Dict[str, List[int]] = {}
        for _, row in processed_df.iterrows():
            norm_title = str(row["title"]).lower().strip()
            if norm_title not in title_to_ids:
                title_to_ids[norm_title] = []
            title_to_ids[norm_title].append(int(row["id"]))

        # Build fast display metadata dictionary
        display_columns = [
            "id", "title", "overview", "tagline", "release_date", "release_year",
            "runtime", "popularity", "vote_average", "vote_count",
            "raw_genres", "raw_keywords", "raw_cast", "raw_director"
        ]
        metadata_lookup = {}
        for _, row in processed_df[display_columns].iterrows():
            metadata_lookup[int(row["id"])] = {
                "id": int(row["id"]),
                "title": row["title"],
                "overview": row["overview"],
                "tagline": row["tagline"],
                "release_date": row["release_date"],
                "release_year": row["release_year"],
                "runtime": int(row["runtime"]),
                "popularity": float(row["popularity"]),
                "vote_average": float(row["vote_average"]),
                "vote_count": int(row["vote_count"]),
                "genres": row["raw_genres"],
                "keywords": row["raw_keywords"],
                "cast": row["raw_cast"],
                "director": row["raw_director"]
            }

        # Calculate dataset fingerprint
        data_hash = hashlib.sha256(
            (str(len(processed_df)) + str(processed_df["id"].sum())).encode("utf-8")
        ).hexdigest()[:16]

        artifact_payload = {
            "tfidf_matrix": tfidf_matrix,
            "vectorizer": vectorizer,
            "id_to_idx": id_to_idx,
            "idx_to_id": idx_to_id,
            "title_to_ids": title_to_ids,
            "metadata_lookup": metadata_lookup,
            "config_hash": self.config.compute_hash(),
            "data_hash": data_hash,
            "catalog_size": len(processed_df),
            "engine_version": self.config.engine_version,
            "build_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        artifact_file = output_dir / "catalog_nlp_bundle.joblib"
        joblib.dump(artifact_payload, artifact_file, compress=3)
        logger.info(f"Serialized catalog NLP bundle to {artifact_file} (size: {artifact_file.stat().st_size / 1024:.1f} KB)")
        return artifact_file
