#!/usr/bin/env bash
# CinePulse Development Runner (Bash for Linux/macOS)
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$DIR"

echo "=========================================================="
echo " Starting CinePulse Platform (Backend + Frontend)"
echo "=========================================================="

# 1. Build artifacts if missing
ARTIFACT="backend/app/recommender/artifacts/catalog_nlp_bundle.joblib"
if [ ! -f "$ARTIFACT" ]; then
    echo "[1/3] Building NLP catalog artifacts..."
    python3 scripts/build_catalog.py
else
    echo "[1/3] NLP artifacts verified ($ARTIFACT)"
fi

# 2. Trap cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null || true
}
trap cleanup EXIT

# 3. Start Backend
echo "[2/3] Starting FastAPI Backend on http://127.0.0.1:8000..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend &

# 4. Start Frontend
echo "[3/3] Starting Next.js Frontend on http://localhost:3000..."
cd frontend
npm run dev &

echo "=========================================================="
echo " CinePulse is RUNNING!"
echo " -> Frontend Web App:     http://localhost:3000"
echo " -> Backend REST API:     http://127.0.0.1:8000"
echo " -> Interactive API Docs: http://127.0.0.1:8000/docs"
echo "=========================================================="
wait
