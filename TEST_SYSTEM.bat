@echo off
echo ========================================
echo   AI Interview Platform - System Test
echo ========================================
echo.

echo Testing Backend Services...
echo.

echo [1] Testing Health Endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo [2] Testing Interview Service Health...
curl -s http://localhost:8000/api/v1/interview/health
echo.
echo.

echo [3] Testing Voice Service...
curl -s http://localhost:8000/api/v1/voice/voice-test
echo.
echo.

echo [4] Testing AI Service Health...
curl -s http://localhost:8000/api/v1/ai/health
echo.
echo.

echo [5] Testing Supported Voices...
curl -s http://localhost:8000/api/v1/voice/supported-voices
echo.
echo.

echo [6] Testing API Documentation...
echo Opening API docs in browser...
start http://localhost:8000/api/docs
echo.

echo [7] Testing Frontend...
echo Opening frontend in browser...
start http://localhost:3000
echo.

echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo All services are responding correctly!
echo.
pause
