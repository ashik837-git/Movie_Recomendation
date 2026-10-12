# Data Directory: CinePulse Engine Data

This directory is designated for the raw movie metadata datasets used by CinePulse's NLP recommendation engine.

## 1. Primary Dataset: TMDB 5000 Movie Dataset

The core content-based NLP recommender relies on the **TMDB 5000 Movie Dataset** (originating from The Movie Database, compiled on Kaggle).

### Required Files:
Place the following two files into this `data/` folder:
- `tmdb_5000_movies.csv` (~5.7 MB)
- `tmdb_5000_credits.csv` (~40 MB)

### Source & Acquisition:
- **Source**: [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- **License**: The original dataset is licensed under Open Data Commons Public Domain Dedication and License (PDDL / CC0 1.0 Universal). Film metadata is attributed to TMDB API.
- **Commercial Use Note**: If used in production or commercial applications, adhere to TMDB API's Terms of Use (free non-commercial tier vs. commercial licensing).

### How to Download:
1. Visit [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and log in.
2. Download the archive `tmdb-movie-metadata.zip`.
3. Extract `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` directly into `Movie_Recommendation/data/`.
4. Run the catalog builder:
   ```bash
   python scripts/build_catalog.py --data-dir data/ --output-dir backend/app/recommender/artifacts/
   ```

---

## 2. Synthetic Test Fixture (Pre-packaged)

If the Kaggle CSV files are not yet downloaded in your local environment:
- The system automatically detects their absence and falls back to `backend/tests/fixtures/synthetic_tmdb_movies.csv` and `backend/tests/fixtures/synthetic_tmdb_credits.csv`.
- This contains **40 clearly labeled synthetic/fictional movies** conforming to the identical TMDB schema, allowing the full stack, recommendation engine, APIs, tests, and CI to run cleanly out of the box.

---

## 3. Netflix Prize Ratings Dataset (Separate Offline Experiment)

- **Files**: `combined_data_1.txt` through `combined_data_4.txt`, `movie_titles.csv`.
- **Status**: **NOT USED for the NLP Recommender Engine**.
- **Rationale**:
  1. The Netflix Prize data contains only user IDs, ratings, dates, and plain movie titles. It contains **no movie plots, overviews, genres, cast, crew, or keywords**.
  2. The IDs are internal Netflix IDs and **cannot be joined reliably with TMDB IDs** (joining on title causes collisions and ambiguity).
  3. The uncompressed dataset exceeds 2 GB with 100M+ ratings, which causes memory exhaustion on typical single-node web hosting instances.
- **Experiment Only**: Code for studying matrix factorization / SVD on ratings is housed strictly under `experiments/netflix_svd.py` as an offline research exploration.

---

## 4. Personalization Stretch Goal: MovieLens

If personalized collaborative filtering is desired in a future milestone:
- The recommended dataset is **MovieLens `ratings_small.csv`** paired with **`links.csv`**.
- `links.csv` provides direct, verified mappings between `movieId` and `tmdbId`, eliminating guesswork.

---

## 5. Repository & Git Policy
- **Never commit raw CSV files** exceeding 10 MB or containing production/sensitive data.
- The `.gitignore` excludes `data/*.csv`, `data/*.txt`, `data/*.zip`, and `.env` files.
