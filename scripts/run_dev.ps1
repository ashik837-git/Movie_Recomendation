# CinePulse Development Runner (PowerShell for Windows)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting CinePulse Platform (Backend + Frontend)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
Set-Location $PROJECT_ROOT

# 1. Verify / Build Artifacts
$ARTIFACT = "backend/app/recommender/artifacts/catalog_nlp_bundle.joblib"
if (-not (Test-Path $ARTIFACT)) {
    Write-Host "[1/3] Building NLP catalog artifacts from fixtures..." -ForegroundColor Yellow
    & "backend/venv/Scripts/python.exe" scripts/build_catalog.py
} else {
    Write-Host "[1/3] NLP artifacts verified ($ARTIFACT)" -ForegroundColor Green
}

# 2. Launch FastAPI Backend
Write-Host "[2/3] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
$BackendProcess = Start-Process -FilePath "backend/venv/Scripts/uvicorn.exe" -ArgumentList "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--app-dir", "backend" -PassThru

# 3. Launch Next.js Frontend
Write-Host "[3/3] Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Yellow
Set-Location "$PROJECT_ROOT/frontend"
$FrontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run", "dev" -PassThru
Set-Location $PROJECT_ROOT

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " CinePulse is RUNNING!" -ForegroundColor Green
Write-Host " -> Frontend Web App:     http://localhost:3000" -ForegroundColor White
Write-Host " -> Backend REST API:     http://127.0.0.1:8000" -ForegroundColor White
Write-Host " -> Interactive API Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Press Ctrl+C or close the terminal windows to exit." -ForegroundColor Gray
