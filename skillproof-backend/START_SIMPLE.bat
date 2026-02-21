@echo off
echo ========================================
echo Starting SatyaHire Backend (Simple Mode)
echo ========================================
echo.
echo No database required!
echo This version works immediately.
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo Starting server on http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo.

python -m uvicorn simple_main:app --reload --host 0.0.0.0 --port 8000

pause
