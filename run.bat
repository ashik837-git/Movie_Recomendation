@echo off
title CinePulse Fullstack Platform
echo ===================================================================
echo   Launching CinePulse Unified Movie Recommendation Platform
echo ===================================================================
cd /d "%~dp0"

REM Prefer virtualenv python if present
if exist "backend\venv\Scripts\python.exe" (
    "backend\venv\Scripts\python.exe" run.py
) else (
    python run.py
)
pause
