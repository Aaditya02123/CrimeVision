@echo off
setlocal

echo ========================================================
echo Launching CrimeVision AI Forensic Intelligence Platform
echo ========================================================

:: Terminate existing instances holding backend (8000) or frontend (5173) ports
echo [*] Terminating existing instances on ports 8000 and 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    if not "%%a"=="" taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do (
    if not "%%a"=="" taskkill /f /pid %%a >nul 2>&1
)

:: ponytail: simple delay check via timeout, no heavy polling loops
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000...
start "CrimeVision Backend (FastAPI)" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Vite Frontend on http://localhost:5173...
start "CrimeVision Frontend (React Vite)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo [*] Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo [*] Opening browser...
start http://localhost:5173

echo.
echo Both servers started!
echo Frontend: http://localhost:5173
echo API Docs: http://127.0.0.1:8000/docs
echo.
pause
