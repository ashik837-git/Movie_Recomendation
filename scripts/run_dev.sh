#!/usr/bin/env bash
# CinePulse Unified Development Runner (Linux / macOS)
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$DIR"

PYTHON="backend/venv/bin/python"
if [ ! -f "$PYTHON" ]; then
    PYTHON="python3"
fi

exec "$PYTHON" run.py
