@echo off
echo ========================================
echo   SatyaHire AI - First Time Setup
echo ========================================
echo.

echo [1/2] Installing Backend Dependencies...
cd skillproof-backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install backend dependencies
    echo Please make sure Python is installed
    pause
    exit /b 1
)
cd ..

echo.
echo [2/2] Installing Frontend Dependencies...
cd skillproof-frontend
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install frontend dependencies
    echo Please make sure Node.js is installed
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo  1. Run START.bat to launch the platform
echo  2. Visit http://localhost:3000
echo  3. Create a candidate account
echo  4. Test the AI voice interview
echo.
echo For testing checklist, run:
echo  TEST_VOICE_INTERVIEW.bat
echo.
pause
