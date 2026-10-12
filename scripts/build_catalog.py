"""
CinePulse Catalog Build Script (CLI)
Builds and serializes sparse TF-IDF NLP artifacts from TMDB CSVs or fallback fixtures.
Usage:
    python scripts/build_catalog.py [--data-dir data/] [--output-dir backend/app/recommender/artifacts/]
"""
import argparse
import logging
import sys
import time
from pathlib import Path

# Add backend directory to path so recommender package can be imported directly
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.recommender.config import DEFAULT_CONFIG
from app.recommender.builder import CatalogBuilder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_catalog")

def main():
    parser = argparse.ArgumentParser(description="Build CinePulse NLP recommendation artifacts.")
    parser.add_argument("--data-dir", type=str, default="data", help="Directory containing raw TMDB CSVs")
    parser.add_argument("--output-dir", type=str, default="backend/app/recommender/artifacts", help="Output directory for joblib artifact")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    data_dir = (project_root / args.data_dir).resolve()
    output_dir = (project_root / args.output_dir).resolve()

    movies_path = data_dir / "tmdb_5000_movies.csv"
    credits_path = data_dir / "tmdb_5000_credits.csv"

    is_synthetic = False
    if not (movies_path.exists() and credits_path.exists()):
        logger.warning(f"Raw TMDB dataset files not found in {data_dir}.")
        fixtures_dir = project_root / "backend" / "tests" / "fixtures"
        movies_path = fixtures_dir / "synthetic_tmdb_movies.csv"
        credits_path = fixtures_dir / "synthetic_tmdb_credits.csv"
        is_synthetic = True

        if not (movies_path.exists() and credits_path.exists()):
            logger.error("Neither raw data nor synthetic fixtures were found! Run scripts/generate_fixtures.py first.")
            sys.exit(1)

        logger.info(f"==> Utilizing verified synthetic fixtures from {fixtures_dir}")
    else:
        logger.info(f"==> Utilizing real TMDB datasets from {data_dir}")

    start_time = time.time()
    builder = CatalogBuilder(config=DEFAULT_CONFIG)
    artifact_file = builder.build_and_save_artifacts(movies_path, credits_path, output_dir)
    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print(" CINEPULSE NLP CATALOG BUILD COMPLETED")
    print("=" * 60)
    print(f" Source:           {'Synthetic Test Fixture' if is_synthetic else 'Real TMDB 5000 Dataset'}")
    print(f" Artifact path:    {artifact_file}")
    print(f" Artifact size:    {artifact_file.stat().st_size / 1024:.2f} KB")
    print(f" Build time:       {elapsed:.2f} seconds")
    print(f" Config hash:      {DEFAULT_CONFIG.compute_hash()}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
