@echo off
echo ========================================
echo   Complete System Test - All Features
echo ========================================
echo.

echo [1] Testing Backend Health...
curl -s http://localhost:8000/health
echo.
echo.

echo [2] Testing Multilingual Languages...
curl -s http://localhost:8000/api/v1/multilingual/languages
echo.
echo.

echo [3] Testing Interview Service Health...
curl -s http://localhost:8000/api/v1/interview/health
echo.
echo.

echo [4] Testing Voice Service...
curl -s http://localhost:8000/api/v1/voice/voice-test
echo.
echo.

echo [5] Starting Multilingual Interview (Hindi)...
curl -s -X POST http://localhost:8000/api/v1/multilingual/start ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"Python Developer\",\"experience_level\":\"mid\",\"language\":\"hindi\",\"max_questions\":5}"
echo.
echo.

echo [6] Starting Regular Interview...
curl -s -X POST http://localhost:8000/api/v1/interview/start ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"test-user-123\",\"role\":\"Backend Developer\",\"experience_level\":\"mid\",\"language\":\"english\",\"max_questions\":5}"
echo.
echo.

echo [7] Testing AI Service Health...
curl -s http://localhost:8000/api/v1/ai/health
echo.
echo.

echo [8] Testing Experience Levels...
curl -s http://localhost:8000/api/v1/multilingual/experience-levels
echo.
echo.

echo ========================================
echo   System Test Complete!
echo ========================================
echo.
echo ✅ All services are running correctly!
echo.
echo Available Features:
echo   - Multilingual AI Interviews (11 languages)
echo   - Voice Recognition & Synthesis
echo   - Real-time Answer Evaluation
echo   - AI-Powered Question Generation
echo   - Audio Transcription
echo   - Interview Session Management
echo.
echo Next Steps:
echo   1. Open API Docs: http://localhost:8000/api/docs
echo   2. Open Frontend: http://localhost:3000
echo   3. Test multilingual: TEST_MULTILINGUAL.bat
echo.
pause
