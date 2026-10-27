@echo off
echo ========================================================
echo Starting CrimeVision AI Forensic Intelligence Platform API
echo Backend running on http://127.0.0.1:8000
echo Swagger Docs on http://127.0.0.1:8000/docs
echo ========================================================
cd /d "%~dp0backend"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
