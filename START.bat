@echo off
echo ========================================
echo   SatyaHire AI Platform - Quick Start
echo ========================================
echo.

REM Start Backend (Simple Version - No Database Required)
echo [1/2] Starting Backend Server (No Database)...
start "SatyaHire Backend" cmd /k "cd skillproof-backend && python -m uvicorn simple_main:app --reload"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend
echo [2/2] Starting Frontend Server...
start "SatyaHire Frontend" cmd /k "cd skillproof-frontend && npm run dev"

echo.
echo ========================================
echo   Platform Started Successfully!
echo ========================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/api/docs
echo.
echo Features Available:
echo  - AI Voice Interview
echo  - Speech Recognition
echo  - Authentication System
echo  - Resume Parser
echo.
echo Note: Using simple backend (no database required)
echo For full backend with PostgreSQL, run START_AUTHENTICATION.bat
echo.
echo Press any key to close this window...
pause
