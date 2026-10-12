# CinePulse Architecture & System Specification

## 1. System Overview

**CinePulse** is an end-to-end, dark cinematic movie discovery and recommendation platform inspired by modern streaming interfaces. It couples a content-based Natural Language Processing (NLP) recommendation engine built with scikit-learn with a responsive Next.js frontend, FastAPI backend, and Supabase PostgreSQL authentication and persistence layer.

---

## 2. Directory Tree

```
Movie_Recommendation/
├── .env.example                       # Documented environment variable template
├── .gitignore                         # Strict exclusion of secrets, large datasets, and artifacts
├── README.md                          # Full project overview and onboarding guide
├── data/                              # Local dataset store (git-ignored)
│   └── README.md                      # Acquisition guide and Kaggle terms
├── docs/                              # Project technical documentation
│   ├── architecture.md                # System design, API contracts, DB schemas
│   ├── data.md                        # Dataset schemas, verification, and rationale
│   └── evaluation.md                  # Measured offline and latency metrics
├── experiments/                       # Offline experimental scripts
│   └── netflix_svd.py                 # Netflix Prize ratings matrix factorization (isolated)
├── scripts/                           # Reproducible CLI automation tools
│   ├── build_catalog.py               # Preprocesses raw metadata into sparse TF-IDF artifacts
│   ├── download_data.py               # Verifies or downloads datasets
│   ├── evaluate.py                    # Runs offline recommendation evaluation benchmarks
│   └── generate_fixtures.py           # Generates 40 synthetic movies conforming to TMDB schema
├── backend/                           # Python FastAPI Backend & NLP Engine
│   ├── requirements.txt               # Pinned dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entrypoint, middleware, health endpoints
│   │   ├── config.py                  # Pydantic Settings from environment
│   │   ├── api/                       # REST endpoints
│   │   │   ├── __init__.py
│   │   │   ├── movies.py              # Catalog, search, details, popular, genres
│   │   │   ├── recommendations.py     # Content-based similarity with explanations
│   │   │   ├── user.py                # Watchlist and viewing history (authenticated)
│   │   │   └── payments.py            # Checkout and webhook handling
│   │   ├── recommender/               # PURE NLP MODULE (zero web / DB imports)
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Field weights, token rules, vectorizer hyperparams
│   │   │   ├── builder.py             # Preprocessing and sparse TF-IDF fitting
│   │   │   └── engine.py              # On-demand sparse cosine dot product and ranking
│   │   ├── auth/                      # Supabase JWT verification and dependencies
│   │   │   └── jwt_validator.py
│   │   └── payments/                  # Provider-agnostic payment abstraction
│   │       ├── interface.py           # PaymentProvider interface
│   │       ├── sandbox_provider.py    # Sandbox / Local provider (fallback)
│   │       └── stripe_provider.py     # Stripe test-mode provider
│   └── tests/
│       ├── conftest.py
│       ├── test_recommender.py        # NLP engine unit tests
│       ├── test_api.py                # Endpoint integration tests
│       └── fixtures/                  # Synthetic test datasets
├── frontend/                          # Next.js (App Router) + TypeScript + Tailwind
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── src/
│   │   ├── app/                       # App Router pages and routes
│   │   │   ├── layout.tsx             # Root layout with navbar and footer
│   │   │   ├── page.tsx               # Home page (Hero banner + dynamic carousels)
│   │   │   ├── movie/[id]/page.tsx    # Movie details, trailers, similar recommendations
│   │   │   ├── search/page.tsx        # Debounced search & filtering
│   │   │   ├── my-list/page.tsx       # Saved user watchlist
│   │   │   ├── pricing/page.tsx       # Subscription plans and billing checkout
│   │   │   ├── login/page.tsx         # Supabase auth login
│   │   │   └── register/page.tsx      # Supabase auth registration
│   │   ├── components/                # Reusable UI components
│   │   │   ├── Navbar.tsx             # Sticky responsive navigation with keyboard accessibility
│   │   │   ├── HeroBanner.tsx         # Spotlight hero with trailer modal trigger
│   │   │   ├── MovieCard.tsx          # Card with hover expansion, badges, and fallback art
│   │   │   ├── MovieRow.tsx           # Horizontal carousel with smooth desktop/mobile scroll
│   │   │   ├── TrailerModal.tsx       # Accessible modal for official trailers or fallback
│   │   │   └── Toast.tsx              # Dynamic feedback notifications
│   │   ├── lib/                       # API clients and Supabase helpers
│   │   │   ├── api.ts                 # Strongly typed backend API client
│   │   │   ├── supabaseClient.ts      # Client-side Supabase client
│   │   │   └── supabaseServer.ts      # Server-side cookie session helper
│   │   └── types/                     # Shared TypeScript interfaces
└── supabase/                          # Supabase PostgreSQL configuration
    └── migrations/
        └── 20261012000000_init_schema.sql # Tables, RLS, indexes, and triggers
```

---

## 3. Technology Stack & Architectural Decisions

| Layer | Selected Technology | Rationale & Trade-offs |
| :--- | :--- | :--- |
| **Frontend** | Next.js 14+ (App Router), TypeScript, Tailwind CSS, Lucide Icons | Server Components for initial fast load; client components for interactive carousels and debounced search. Strong typing catches contract drift early. |
| **Backend API** | FastAPI (Python 3.11–3.13), Pydantic v2, Uvicorn | High asynchronous I/O performance, automated OpenAPI generation, and native integration with Python's scientific computing stack (NumPy, SciPy, scikit-learn). |
| **NLP Engine** | `scikit-learn` (`TfidfVectorizer`), `SciPy` CSR sparse matrix, `joblib` | Content-based TF-IDF vectorization with configurable field weighting. Storing normalized sparse vectors avoids precomputing an $O(N^2)$ 4,803 x 4,803 dense matrix, keeping RAM under 60 MB and inference latency under 5 ms. |
| **Database & Auth** | Supabase (PostgreSQL 15+ & Supabase Auth) | Managed relational database with Row-Level Security (RLS) guaranteeing user-data isolation at the database layer. Cookie-based session tokens prevent localStorage XSS leakage. |
| **Payments** | Provider-Agnostic Interface (`PaymentProvider`) with Sandbox & Stripe test support | Bangladesh-based merchants face restrictions onboarding to standard Stripe. An interface pattern allows zero-friction switching to sandbox mocks, SSLCommerz, or Merchant-of-Record (Paddle/LemonSqueezy) without rewriting billing logic. |

---

## 4. API Contract (OpenAPI Specification)

All API responses follow consistent JSON payloads. Base URL prefix: `/api/v1`.

### A. Health & System
- `GET /health`: Returns `{ "status": "healthy", "catalog_loaded": bool, "catalog_size": int, "version": str }`.

### B. Catalog & Movies
- `GET /movies`: Query params: `page` (default: 1), `page_size` (default: 20, max: 50), `genre` (optional string). Returns paginated movies list with total counts.
- `GET /movies/{id}`: Returns complete movie metadata, cast, crew, director, keywords, and trailer key if available. Returns 404 with suggested titles if not found.
- `GET /movies/{id}/similar`: Query params: `limit` (default: 10, max: 50). Returns ranked list of similar movies, including similarity score and **truthful explanations** (shared genres, keywords, cast, and director). Excludes the queried movie itself.
- `GET /search`: Query params: `q` (string), `genre` (optional), `limit` (default: 20). Performs case-insensitive, punctuation-tolerant substring and token matching.
- `GET /featured`: Returns the top curated movie for the hero banner.
- `GET /popular`: Returns top movies ranked via the **IMDb Weighted Rating formula**:
  $$W = \frac{v}{v + m} \times R + \frac{m}{v + m} \times C$$
  where $v$ is vote count, $m$ is the 90th percentile threshold, $R$ is movie vote average, and $C$ is the catalog mean vote average.
- `GET /genres`: Returns distinct list of available genres and movie counts.

### C. User & Watchlist (Authenticated via Bearer JWT)
- `GET /user/watchlist`: Returns user's saved movies.
- `POST /user/watchlist`: Body: `{ "movie_id": int }`. Adds movie to user's list.
- `DELETE /user/watchlist/{movie_id}`: Removes movie from user's list.
- `GET /user/history`: Returns recently viewed movie history.
- `POST /user/history`: Body: `{ "movie_id": int }`. Records movie view.

### D. Subscriptions & Payments
- `GET /payments/plans`: Returns subscription tiers, entitlements, and limits.
- `POST /payments/create-checkout-session`: Body: `{ "plan_id": str, "success_url": str, "cancel_url": str }`. Creates a server-side checkout session.
- `POST /payments/webhook`: Ingests provider webhook events, verifies signatures idempotently, and updates subscription status in Supabase.

---

## 5. Database Schema & RLS Security

### Relational Tables in Supabase PostgreSQL:
1. `profiles`:
   - `id` (UUID, PK, references `auth.users.id` ON DELETE CASCADE)
   - `email` (TEXT)
   - `display_name` (TEXT)
   - `created_at` (TIMESTAMPTZ DEFAULT now())
   - `updated_at` (TIMESTAMPTZ DEFAULT now())
2. `watchlist`:
   - `id` (BIGINT GENERATED ALWAYS AS IDENTITY, PK)
   - `user_id` (UUID, FK -> `profiles.id` ON DELETE CASCADE)
   - `movie_id` (INT NOT NULL)
   - `created_at` (TIMESTAMPTZ DEFAULT now())
   - Unique constraint: `(user_id, movie_id)`
3. `recommendation_history`:
   - `id` (BIGINT GENERATED ALWAYS AS IDENTITY, PK)
   - `user_id` (UUID, FK -> `profiles.id` ON DELETE CASCADE)
   - `movie_id` (INT NOT NULL)
   - `viewed_at` (TIMESTAMPTZ DEFAULT now())
4. `user_preferences`:
   - `user_id` (UUID, PK, FK -> `profiles.id` ON DELETE CASCADE)
   - `favorite_genres` (TEXT[] DEFAULT '{}')
   - `updated_at` (TIMESTAMPTZ DEFAULT now())
5. `subscriptions`:
   - `id` (BIGINT GENERATED ALWAYS AS IDENTITY, PK)
   - `user_id` (UUID, FK -> `profiles.id` ON DELETE CASCADE)
   - `plan_id` (TEXT NOT NULL DEFAULT 'free')
   - `status` (TEXT NOT NULL DEFAULT 'active') -- 'active', 'canceled', 'past_due'
   - `current_period_end` (TIMESTAMPTZ)
   - `provider` (TEXT NOT NULL DEFAULT 'sandbox')
   - `provider_subscription_id` (TEXT)
   - `updated_at` (TIMESTAMPTZ DEFAULT now())
6. `payment_events`:
   - `event_id` (TEXT, PK) -- guarantees idempotency
   - `provider` (TEXT NOT NULL)
   - `payload` (JSONB NOT NULL)
   - `processed_at` (TIMESTAMPTZ DEFAULT now())

### Row-Level Security (RLS) Rules:
- **`watchlist`**: `SELECT`, `INSERT`, `DELETE` allowed **ONLY** where `auth.uid() == user_id`.
- **`recommendation_history`**: `SELECT`, `INSERT` allowed **ONLY** where `auth.uid() == user_id`.
- **`user_preferences`**: `SELECT`, `UPSERT` allowed **ONLY** where `auth.uid() == user_id`.
- **`subscriptions`**: `SELECT` allowed where `auth.uid() == user_id`. **CLIENT WRITES FORBIDDEN**: `INSERT` / `UPDATE` restricted to server-side `service_role` key only.

---

## 6. Hosting & Free-Tier Specifications

| Platform | Role | Free-Tier Limits & Behavior | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Vercel** | Frontend Next.js deployment | 100 GB bandwidth/mo, Serverless execution limits (10s hobby). | Pure static rendering for general pages, client caching with SWR/React Query for API fetches. |
| **Render** | FastAPI Backend | 512 MB RAM, spins down after 15 min of inactivity (cold start 30–50s). | In-memory NLP artifact is kept under 60 MB RAM using SciPy CSR sparse matrix. Startup validation executes in < 300 ms. |
| **Supabase** | PostgreSQL & Auth | 500 MB DB size, 50,000 MAU auth, pauses after 1 week inactivity on free projects. | Movie catalog is maintained in versioned sparse files, not duplicated into DB, keeping DB usage < 10 MB. |
