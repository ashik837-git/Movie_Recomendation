"""
Data Acquisition Script for CinePulse
Assists in downloading and verifying the TMDB 5000 Movie Dataset.
"""
import sys
import os
from pathlib import Path
import subprocess

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def check_files():
    movies_csv = DATA_DIR / "tmdb_5000_movies.csv"
    credits_csv = DATA_DIR / "tmdb_5000_credits.csv"
    
    found_movies = movies_csv.exists()
    found_credits = credits_csv.exists()
    
    print("=" * 60)
    print("CinePulse Data Verification")
    print("=" * 60)
    print(f"Target directory: {DATA_DIR}")
    print(f" - tmdb_5000_movies.csv: {'[FOUND]' if found_movies else '[MISSING]'}")
    print(f" - tmdb_5000_credits.csv: {'[FOUND]' if found_credits else '[MISSING]'}")
    
    if found_movies and found_credits:
        print("\nAll required raw dataset files are present!")
        print("You can build the recommendation catalog with:")
        print("  python scripts/build_catalog.py")
        return True
    
    print("\nDataset files are missing. Acquisition options:")
    print("Option 1 (Kaggle CLI - if configured with ~/.kaggle/kaggle.json):")
    print("  kaggle datasets download -d tmdb/tmdb-movie-metadata -p data --unzip")
    print("\nOption 2 (Manual download):")
    print("  1. Visit https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
    print("  2. Download archive and extract tmdb_5000_movies.csv and tmdb_5000_credits.csv into:")
    print(f"     {DATA_DIR}")
    print("\nOption 3 (Run with Synthetic Fixtures):")
    print("  The engine automatically falls back to backend/tests/fixtures/synthetic_tmdb_movies.csv")
    print("  No manual download is required to test or run the platform locally!")
    print("=" * 60)
    return False

def try_kaggle_cli():
    try:
        print("Attempting to run Kaggle CLI...")
        res = subprocess.run(
            ["kaggle", "datasets", "download", "-d", "tmdb/tmdb-movie-metadata", "-p", str(DATA_DIR), "--unzip"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print("Successfully downloaded and extracted TMDB 5000 via Kaggle CLI!")
            return True
        else:
            print(f"Kaggle CLI reported an issue:\n{res.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("Kaggle CLI is not installed or not in PATH.")
        return False

if __name__ == "__main__":
    if not check_files():
        if "--kaggle" in sys.argv:
            try_kaggle_cli()
            check_files()
