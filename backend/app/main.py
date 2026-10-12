"""
CinePulse Backend Service Main Application
Initializes FastAPI, configures CORS, handles lifecycle startup artifact verification, and mounts API routers.
"""
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api import movies, user, payments
from .recommender.engine import RecommenderEngine, ArtifactCompatibilityError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("cinepulse.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence: Load sparse NLP artifacts into memory
    artifact_path = settings.resolved_artifacts_dir / "catalog_nlp_bundle.joblib"
    logger.info(f"Checking NLP artifact bundle at: {artifact_path}")

    if not artifact_path.exists():
        logger.warning(
            f"Artifact bundle missing at {artifact_path}. "
            "Building fallback artifact bundle from test fixtures..."
        )
        # Attempt automatic build if missing
        try:
            from .recommender.builder import CatalogBuilder
            from .recommender.config import DEFAULT_CONFIG
            base = Path(__file__).resolve().parent.parent
            fixtures_dir = base / "tests" / "fixtures"
            movies_csv = fixtures_dir / "synthetic_tmdb_movies.csv"
            credits_csv = fixtures_dir / "synthetic_tmdb_credits.csv"
            builder = CatalogBuilder(config=DEFAULT_CONFIG)
            builder.build_and_save_artifacts(movies_csv, credits_csv, settings.resolved_artifacts_dir)
            logger.info("Successfully bootstrapped initial NLP artifacts from fixtures.")
        except Exception as e:
            logger.error(f"Failed to bootstrap NLP artifacts: {e}")

    try:
        engine = RecommenderEngine(artifact_path=artifact_path)
        movies.engine = engine
        logger.info(
            f"CinePulse Recommender initialized successfully! "
            f"Catalog size: {engine.catalog_size} titles. Config hash: {engine.config_hash}"
        )
    except Exception as e:
        logger.critical(f"FATAL: RecommenderEngine could not be initialized: {e}")
        movies.engine = None

    yield
    # Shutdown sequence
    logger.info("CinePulse backend shutting down cleanly.")

app = FastAPI(
    title="CinePulse Cinematic Recommendation Engine",
    description="NLP-powered content-based movie discovery platform with truthful explainability.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Info & Health Endpoints
@app.get("/", tags=["system"])
def root_info():
    eng = movies.engine
    return {
        "platform": "CinePulse Algorithmic Movie Discovery & NLP Recommendation Platform",
        "version": "1.0.0",
        "status": "online",
        "catalog_size": eng.catalog_size if eng else 0,
        "frontend_url": "http://localhost:3000",
        "api_docs_url": "/docs",
        "health_check": "/health",
        "api_v1_endpoints": {
            "movies": "/api/v1/movies",
            "popular": "/api/v1/popular",
            "featured": "/api/v1/featured",
            "genres": "/api/v1/genres",
            "search": "/api/v1/search?q={query}",
            "recommendations": "/api/v1/movies/{id}/similar",
            "watchlist": "/api/v1/user/watchlist",
            "plans": "/api/v1/payments/plans",
        },
    }

@app.get("/health", status_code=status.HTTP_200_OK, tags=["system"])
def health_check():
    eng = movies.engine
    return {
        "status": "healthy",
        "service": "CinePulse NLP Engine",
        "catalog_loaded": bool(eng and eng.is_loaded),
        "catalog_size": eng.catalog_size if eng else 0,
        "engine_version": eng.config_hash if eng else None,
        "environment": settings.ENVIRONMENT,
    }

# Mount API v1 Routers
app.include_router(movies.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
