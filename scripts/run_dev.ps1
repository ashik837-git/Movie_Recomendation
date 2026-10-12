# CinePulse Development Runner (PowerShell for Windows)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting CinePulse Platform (Unified Fullstack Runner)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
Set-Location $PROJECT_ROOT

$PYTHON = "backend/venv/Scripts/python.exe"
if (-not (Test-Path $PYTHON)) {
    $PYTHON = "python"
}

& $PYTHON run.py
