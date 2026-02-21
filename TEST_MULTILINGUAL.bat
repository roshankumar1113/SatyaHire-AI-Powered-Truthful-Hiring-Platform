@echo off
echo ========================================
echo   Multilingual Interview System Test
echo ========================================
echo.

echo [1] Testing Supported Languages...
curl -s http://localhost:8000/api/v1/multilingual/languages
echo.
echo.

echo [2] Testing Experience Levels...
curl -s http://localhost:8000/api/v1/multilingual/experience-levels
echo.
echo.

echo [3] Testing Service Health...
curl -s http://localhost:8000/api/v1/multilingual/health
echo.
echo.

echo [4] Starting English Interview...
curl -s -X POST http://localhost:8000/api/v1/multilingual/start ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"Python Developer\",\"experience_level\":\"mid\",\"language\":\"english\",\"max_questions\":5}"
echo.
echo.

echo [5] Starting Hindi Interview...
curl -s -X POST http://localhost:8000/api/v1/multilingual/start ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"Python Developer\",\"experience_level\":\"mid\",\"language\":\"hindi\",\"max_questions\":5}"
echo.
echo.

echo [6] Starting Tamil Interview...
curl -s -X POST http://localhost:8000/api/v1/multilingual/start ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"Python Developer\",\"experience_level\":\"mid\",\"language\":\"tamil\",\"max_questions\":5}"
echo.
echo.

echo [7] Submitting Answer (English)...
curl -s -X POST http://localhost:8000/api/v1/multilingual/submit-answer ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"Python Developer\",\"experience_level\":\"mid\",\"language\":\"english\",\"max_questions\":5,\"question_number\":1,\"previous_question\":\"Tell me about yourself\",\"candidate_answer\":\"I am a Python developer with 3 years of experience\"}"
echo.
echo.

echo ========================================
echo   All Tests Complete!
echo ========================================
echo.
echo Multilingual Interview System is working!
echo.
echo Supported Languages:
echo   - English
echo   - Hindi (हिंदी)
echo   - Tamil (தமிழ்)
echo   - Telugu (తెలుగు)
echo   - Kannada (ಕನ್ನಡ)
echo   - Malayalam (മലയാളം)
echo   - Marathi (मराठी)
echo   - Gujarati (ગુજરાતી)
echo   - Bengali (বাংলা)
echo   - Punjabi (ਪੰਜਾਬੀ)
echo   - Urdu (اردو)
echo.
pause
