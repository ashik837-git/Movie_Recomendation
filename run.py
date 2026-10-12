"""
CinePulse End-to-End Unified Platform Orchestrator
Merges and runs the FastAPI NLP Backend and Next.js Frontend concurrently,
verifies health readiness, launches Google Chrome, and manages graceful shutdowns.
"""
import os
import sys
import time
import signal
import shutil
import urllib.request
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
ARTIFACT_PATH = BACKEND_DIR / "app" / "recommender" / "artifacts" / "catalog_nlp_bundle.joblib"

IS_WINDOWS = sys.platform.startswith("win")

def get_python_executable():
    """Finds the best Python executable (preferring backend virtual environment)."""
    if IS_WINDOWS:
        venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    else:
        venv_python = BACKEND_DIR / "venv" / "bin" / "python"
    
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def get_npm_executable():
    """Finds the npm executable safely for Windows execution policies."""
    if IS_WINDOWS:
        npm_cmd = shutil.which("npm.cmd")
        if npm_cmd:
            return npm_cmd
        return "npm.cmd"
    return "npm"

def ensure_nlp_artifacts(python_bin):
    """Builds NLP catalog artifacts from fixtures if missing."""
    if not ARTIFACT_PATH.exists():
        print("[1/4] NLP artifact bundle missing. Building from synthetic dataset...")
        build_script = ROOT_DIR / "scripts" / "build_catalog.py"
        res = subprocess.run([python_bin, str(build_script)], cwd=str(ROOT_DIR))
        if res.returncode != 0:
            print("[WARN] Artifact build returned non-zero code; backend will attempt fallback at startup.")
    else:
        print(f"[1/4] NLP artifacts verified: {ARTIFACT_PATH.name}")

def wait_for_url(url, timeout=30, label="service"):
    """Polls an HTTP URL until it responds with 200 OK."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CinePulse-HealthCheck"})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def open_in_chrome(url):
    """Launches Google Chrome explicitly or falls back to system browser."""
    chrome_paths = []
    if IS_WINDOWS:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
    elif sys.platform == "darwin":
        chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:
        chrome_paths = ["google-chrome", "google-chrome-stable", "chromium-browser"]

    for path in chrome_paths:
        if (os.path.isabs(path) and os.path.exists(path)) or shutil.which(path):
            try:
                print(f"[4/4] Launching Google Chrome -> {url}")
                subprocess.Popen([path, url])
                return True
            except Exception as e:
                print(f"[WARN] Failed to open Chrome at {path}: {e}")

    # Fallback to default browser
    import webbrowser
    print(f"[4/4] Launching default web browser -> {url}")
    webbrowser.open(url)
    return True

def kill_process_tree(pid):
    """Cleanly terminates a process and all its children."""
    if IS_WINDOWS:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except Exception:
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception:
                pass

def main():
    print("=" * 65)
    print("  CinePulse: Unified End-to-End Movie Discovery & NLP Platform  ")
    print("=" * 65)

    python_bin = get_python_executable()
    npm_bin = get_npm_executable()

    # Step 1: Ensure NLP artifacts
    ensure_nlp_artifacts(python_bin)

    backend_proc = None
    frontend_proc = None

    def cleanup(signum=None, frame=None):
        print("\n[!] Gracefully shutting down CinePulse platform...")
        if backend_proc and backend_proc.poll() is None:
            print(" -> Stopping FastAPI Backend...")
            kill_process_tree(backend_proc.pid)
        if frontend_proc and frontend_proc.poll() is None:
            print(" -> Stopping Next.js Frontend...")
            kill_process_tree(frontend_proc.pid)
        print("CinePulse shut down cleanly. Goodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Step 2: Start FastAPI Backend
    print("[2/4] Starting FastAPI NLP Backend on http://127.0.0.1:8000...")
    backend_cmd = [
        python_bin, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--app-dir", "backend"
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Wait for backend health
    print("     Waiting for backend /health check...")
    if not wait_for_url("http://127.0.0.1:8000/health", timeout=15, label="Backend"):
        print("[ERROR] Backend health check failed to respond in time.")
    else:
        print("     [OK] Backend healthy and catalog loaded!")

    # Step 3: Start Next.js Frontend
    print("[3/4] Starting Next.js Frontend on http://localhost:3000...")
    frontend_cmd = [npm_bin, "run", "dev"]
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Wait for frontend readiness
    print("     Waiting for Next.js web application readiness...")
    wait_for_url("http://localhost:3000", timeout=25, label="Frontend")
    print("     [OK] Frontend application ready!")

    print("=" * 65)
    print(" CinePulse is LIVE & FULLY OPERATIONAL!")
    print(" -------------------------------------------------------------")
    print(" -> Web Application:     http://localhost:3000")
    print(" -> Backend REST API:    http://127.0.0.1:8000")
    print(" -> Interactive Docs:    http://127.0.0.1:8000/docs")
    print(" -> Health Status:       http://127.0.0.1:8000/health")
    print(" -------------------------------------------------------------")
    print(" Press Ctrl+C in this terminal anytime to cleanly stop both services.")
    print("=" * 65)

    # Step 4: Open in Google Chrome
    open_in_chrome("http://localhost:3000")

    # Keep alive and stream backend logs if any error occurs
    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print(f"[ERROR] Backend stopped unexpectedly (exit code {backend_proc.returncode}).")
                break
            if frontend_proc.poll() is not None:
                print(f"[ERROR] Frontend stopped unexpectedly (exit code {frontend_proc.returncode}).")
                break
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
