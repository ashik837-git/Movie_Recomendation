# CinePulse Data Verification & Ingestion Specification

## 1. Status of Dataset Files in Workspace

| File | Status | Expected Location | Description |
| :--- | :--- | :--- | :--- |
| `tmdb_5000_movies.csv` | **Missing locally** (Standard Kaggle download needed) | `data/tmdb_5000_movies.csv` | Primary TMDB movie catalog (4,803 rows). |
| `tmdb_5000_credits.csv` | **Missing locally** (Standard Kaggle download needed) | `data/tmdb_5000_credits.csv` | Primary TMDB credits & crew data (4,803 rows). |
| `synthetic_tmdb_movies.csv` | **Present** (Pre-packaged test fixture) | `backend/tests/fixtures/synthetic_tmdb_movies.csv` | 40 synthetic movies conforming to exact TMDB schema. |
| `synthetic_tmdb_credits.csv` | **Present** (Pre-packaged test fixture) | `backend/tests/fixtures/synthetic_tmdb_credits.csv` | 40 synthetic credits rows conforming to exact TMDB schema. |
| `netflix_movie_recommendation.ipynb` | Missing from initial workspace | `experiments/` (if added) | Netflix Prize ratings notebook (matrix factorization). |
| `combined_data_*.txt` / `movie_titles.csv` | Excluded by design | `experiments/` (offline only) | Raw Netflix prize ratings (no NLP features). |

---

## 2. TMDB 5000 Data Schema & Contract

### A. `tmdb_5000_movies.csv`
- **Primary Key**: `id` (integer)
- **Expected Rows**: ~4,803 (real dataset) / 40 (synthetic fixture)
- **Schema & Dtypes**:
  - `id` (`int64`): Unique TMDB movie identifier.
  - `title` (`object` / `string`): Official title of the film.
  - `overview` (`object` / `string`): Synopsis / narrative summary (primary source for NLP document).
  - `genres` (`object` / JSON string): Serialized list of `[{"id": int, "name": str}]`.
  - `keywords` (`object` / JSON string): Serialized list of `[{"id": int, "name": str}]`.
  - `release_date` (`object` / `string` YYYY-MM-DD): Theatrical or premiere date.
  - `runtime` (`float64`): Duration in minutes.
  - `popularity` (`float64`): TMDB engagement metric.
  - `vote_average` (`float64`): Mean rating (0.0 to 10.0 scale).
  - `vote_count` (`int64`): Total number of ratings cast.
  - `tagline` (`object` / `string`): Short promotional catchphrase.
  - `original_language` (`object` / `string`): ISO 639-1 language code (e.g., `'en'`).
  - `status` (`object` / `string`): Production status (`'Released'`, `'Post Production'`).
  - `budget` (`int64`): Production budget in USD.
  - `revenue` (`int64`): Box office gross in USD.

### B. `tmdb_5000_credits.csv`
- **Foreign Key**: `movie_id` (integer, joins with `movies.id`).
- **Join Rule**: **Strict join on `movies.id == credits.movie_id`**. Never join on `title` to prevent misattribution across remakes, adaptations, and ambiguous names.
- **Schema & Dtypes**:
  - `movie_id` (`int64`): Target movie foreign key.
  - `title` (`object` / `string`): Title string (note: notebook contained a typo column `tittle` which our ingestion pipeline explicitly defends against).
  - `cast` (`object` / JSON string): List of actors with character names, ordering, and actor names.
  - `crew` (`object` / JSON string): List of crew members with job titles (e.g. `job == "Director"`).

---

## 3. Data Acquisition Protocol (Real Dataset)

To populate the real 4,803 TMDB movies dataset:
1. Visit the legal Kaggle repository: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
2. Download the zip archive and place:
   - `tmdb_5000_movies.csv` into `Movie_Recommendation/data/`
   - `tmdb_5000_credits.csv` into `Movie_Recommendation/data/`
3. Verify with the automated verification script:
   ```bash
   python scripts/download_data.py
   ```
4. Build the versioned sparse NLP recommendation artifacts:
   ```bash
   python scripts/build_catalog.py
   ```

---

## 4. Netflix Prize Data Exclusion Rationale

The Netflix Prize dataset (`combined_data_1.txt` ... `combined_data_4.txt`, `movie_titles.csv`) is **excluded from the NLP engine pipeline** due to fundamental architectural mismatches:
1. **Zero Textual Features**: The dataset contains only `(CustomerID, Rating, Date)` tuples and plain movie titles. It lacks plots, overviews, genres, cast, crew, taglines, or thematic keywords.
2. **Incompatible ID Space**: Netflix Prize IDs are proprietary internal integer IDs from 1999–2005. They do not map to TMDB IDs. Joining on title text creates severe collision errors (e.g., matching remakes or mismatched years).
3. **RAM & Compute Bloat**: Loading 24M–100M ratings into single-node memory requires dense pivoting matrices exceeding 16 GB RAM, causing Out-Of-Memory crashes on standard cloud free tiers.
4. **Offline Scope**: Matrix factorization experiments on ratings are preserved in `experiments/` for academic comparison only.

---

## 5. Personalization Roadmap (MovieLens Stretch Goal)

For future collaborative filtering or hybrid recommendations:
- The industry-standard path is **MovieLens 100k / Latest Small** (`ratings_small.csv` + `links.csv`).
- `links.csv` provides direct, verified `tmdbId` mappings for every `movieId`.
