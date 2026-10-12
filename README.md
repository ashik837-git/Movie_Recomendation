# CinePulse: Algorithmic Movie Discovery & NLP Recommendation Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000.svg?style=flat&logo=next.js)](https://nextjs.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E.svg?style=flat&logo=scikit-learn)](https://scikit-learn.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%2B%20Auth-3ECF8E.svg?style=flat&logo=supabase)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**CinePulse** is an end-to-end, dark cinematic movie discovery platform inspired by modern streaming interfaces. It is powered by a custom-engineered, content-based Natural Language Processing (NLP) recommendation engine that constructs weighted feature document "soups" (director, genres, keywords, cast, synopsis) and evaluates sparse cosine similarity on demand with **truthful explainability**.

> [!NOTE]
> **Product Nature & Compliance Disclaimer**: CinePulse is a discovery and recommendation platform, **not** a licensed streaming service. In strict accordance with copyright law, it does not host, download, or scrape copyrighted video playback. The "Play" action triggers official trailer search previews or clearly indicates that full-feature playback is unavailable.

---

## 1. System Architecture

```
                       ┌───────────────────────────────┐
                       │      Next.js 14 Frontend      │
                       │    (App Router, TypeScript)   │
                       └───────────────┬───────────────┘
                                       │ REST API (JSON)
                                       ▼
                       ┌───────────────────────────────┐
                       │        FastAPI Backend        │
                       │ (Pydantic v2, JWT Auth, CORS) │
                       └───────┬───────────────┬───────┘
                               │               │
            On-Demand Sparse   │               │ Row-Level Security
            Cosine Similarity  │               │ (RLS) Policies
                               ▼               ▼
      ┌──────────────────────────────┐   ┌───────────────────────────┐
      │     Pure NLP Engine          │   │    Supabase PostgreSQL    │
      │  (scikit-learn CSR Matrix,   │   │ (Profiles, Watchlist,     │
      │   Truthful Explanations)     │   │  Subscriptions, History)  │
      └──────────────────────────────┘   └───────────────────────────┘
```

### Key Architectural Decisions:
1. **On-Demand Sparse Similarity vs. Dense Matrix**: Rather than computing an $O(N^2)$ dense $4,803 \times 4,803$ matrix (which consumes significant RAM and becomes stale on catalog updates), CinePulse stores L2-normalized CSR sparse feature vectors and computes target row dot products on demand via `scipy.sparse` with `numpy.argpartition`. Inference takes **< 1.0 ms** and requires **< 1 MB RAM**.
2. **Weighted Metadata Soup**:
   - Director: **3x** (auteur theory: directorial vision strongly influences tone and cinematography)
   - Genres: **2x** (broad thematic categorization)
   - Thematic Keywords: **2x** (granular motifs: e.g. *wormhole*, *cyberpunk*, *hostile takeover*)
   - Top Cast: **1x** (actor continuity)
   - Synopsis Overview: **1x** (unigrams/bigrams filtered by English stop words)
3. **Truthful Explanations**: Recommendations present exact metadata intersections (shared director, cast members, matching genres, and motifs) rather than fabricated rationales.
4. **Provider-Agnostic Payments**: A unified `PaymentProvider` interface supports local sandbox testing, Stripe test mode, and merchant-of-record gateways (e.g. SSLCommerz / Paddle for merchants in Bangladesh and worldwide).

---

## 2. Directory Structure

```
Movie_Recommendation/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entrypoint & lifespan
│   │   ├── config.py                  # Pydantic Settings
│   │   ├── api/                       # API route handlers
│   │   ├── auth/                      # Supabase JWT verification
│   │   ├── recommender/               # Pure NLP engine (zero DB/web imports)
│   │   │   ├── config.py              # Field weights & version hashing
│   │   │   ├── builder.py             # Preprocessing & TF-IDF fitting
│   │   │   └── engine.py              # Sparse cosine similarity & explainability
│   │   └── payments/                  # PaymentProvider abstraction & Sandbox/Stripe
│   ├── tests/                         # Pytest unit & integration test suite
│   │   └── fixtures/                  # 40 synthetic movies fixture conforming to TMDB schema
│   └── requirements.txt
├── frontend/                          # Next.js 14 App Router UI
│   ├── src/
│   │   ├── app/                       # Pages: Home, Movies, Search, My List, Pricing
│   │   ├── components/                # Reusable UI: Navbar, HeroBanner, MovieCard, MovieRow, Modals
│   │   ├── lib/                       # Typed API client & Supabase helpers
│   │   └── types/                     # TypeScript domain models
│   ├── tailwind.config.ts             # Dark cinematic design tokens
│   └── package.json
├── data/                              # Raw TMDB CSV data (git-ignored)
│   └── README.md
├── docs/                              # Technical specifications
│   ├── architecture.md                # System specification & contracts
│   ├── data.md                        # Dataset schemas & verification
│   └── evaluation.md                  # Empirical latency & diversity measurements
├── scripts/
│   ├── build_catalog.py               # Preprocesses raw CSVs into sparse artifacts
│   ├── download_data.py               # Data acquisition verification script
│   ├── evaluate.py                    # Offline benchmark & report generator
│   └── generate_fixtures.py           # Generates 40 synthetic movies fixture
├── supabase/
│   └── migrations/                    # PostgreSQL tables, RLS policies, and triggers
└── experiments/
    └── netflix_svd.py                 # Offline Netflix Prize SVD exploration (isolated)
```

---

## 3. Quick Start & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (Node 20+ recommended)
- Git

### Step 1: Clone & Configure Environment
```bash
git clone https://github.com/your-username/cinepulse.git
cd cinepulse
cp .env.example .env
```

### Step 2: Set Up Backend Virtual Environment
```bash
# Windows
python -m venv backend/venv
& "backend/venv/Scripts/pip.exe" install -r backend/requirements.txt

# Linux / macOS
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Step 3: Build the NLP Catalog Artifacts
If raw TMDB CSVs are not yet in `data/`, the build script automatically uses the verified synthetic test fixture (40 movies):
```bash
# Windows
& "backend/venv/Scripts/python.exe" scripts/build_catalog.py

# Linux / macOS
python scripts/build_catalog.py
```

### Step 4: Run the Backend API
```bash
# Windows
& "backend/venv/Scripts/uvicorn.exe" backend.app.main:app --reload --port 8000

# Linux / macOS
uvicorn backend.app.main:app --reload --port 8000
```
Visit the interactive Swagger API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 5: Run the Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 4. Dataset Acquisition (Real 4,803 TMDB Movies)

To populate the full 4,803 TMDB dataset:
1. Download the [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
2. Extract `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` into `Movie_Recommendation/data/`.
3. Verify files:
   ```bash
   python scripts/download_data.py
   ```
4. Rebuild sparse artifacts:
   ```bash
   python scripts/build_catalog.py
   ```

### Why Netflix Prize Ratings are Excluded from NLP:
- The Netflix Prize dataset (`combined_data_*.txt`) contains only `(CustomerID, Rating, Date)` tuples.
- It contains **zero narrative plots, genres, cast, crew, or keywords**, and uses proprietary IDs incompatible with TMDB.
- Matrix factorization rating experiments are isolated in `experiments/netflix_svd.py`.
- For future collaborative filtering personalization, use MovieLens `ratings_small.csv` + `links.csv` (which directly maps to TMDB IDs).

---

## 5. Testing & Benchmarking

### Running Backend Unit & Integration Tests:
```bash
# Windows
& "backend/venv/Scripts/pytest.exe" -v

# Linux / macOS
pytest -v
```
**Test Coverage Includes**:
- Safe JSON error handling (no `eval`)
- Director extraction & token space-stripping
- Self-exclusion in recommendations
- IMDb Bayesian weighted score computation
- Per-user watchlist isolation via authorization tokens
- Payment checkout session creation & webhook idempotency

### Running Offline Latency Benchmarks:
```bash
python scripts/evaluate.py
```
Outputs empirical performance measurements to `docs/evaluation.md`.
- **p50 Latency**: `0.67 ms`
- **p95 Latency**: `1.08 ms`
- **Sparse Matrix RAM Footprint**: `< 0.05 MB`

---

## 6. Deployment Guide

### Frontend (Vercel)
1. Import repository into [Vercel](https://vercel.com).
2. Set Root Directory to `frontend`.
3. Add environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Deployed backend URL (e.g. `https://cinepulse-api.onrender.com/api/v1`)
   - `NEXT_PUBLIC_SITE_URL`: Frontend deployment URL

### Backend (Render / Railway)
1. Create a New Web Service on [Render](https://render.com) pointing to the repository.
2. Build Command: `pip install -r backend/requirements.txt && python scripts/build_catalog.py`
3. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Free-tier note: Free instances spin down after 15 minutes of inactivity; first cold-start request takes ~30 seconds.

### Database & Auth (Supabase)
1. Create a free project on [Supabase](https://supabase.com).
2. Run the SQL schema in `supabase/migrations/20261012000000_init_schema.sql` via the Supabase SQL Editor.
3. Add `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_JWT_SECRET` to Render and Vercel environments.
