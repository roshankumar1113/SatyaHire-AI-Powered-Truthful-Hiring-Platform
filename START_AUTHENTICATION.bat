@echo off
echo ========================================
echo SkillProof AI - Authentication Setup
echo ========================================
echo.

echo Step 1: Checking Backend Setup...
cd skillproof-backend

if not exist ".env" (
    echo Creating .env file...
    (
        echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/skillproof
        echo SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-characters-long
        echo DEBUG=True
        echo APP_NAME=SkillProof AI
        echo VERSION=1.0.0
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=15
        echo REFRESH_TOKEN_EXPIRE_DAYS=7
    ) > .env
    echo .env file created!
) else (
    echo .env file already exists.
)

echo.
echo Step 2: Checking Frontend Setup...
cd ..\skillproof-frontend

if not exist ".env.local" (
    echo Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 > .env.local
    echo .env.local file created!
) else (
    echo .env.local file already exists.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Make sure PostgreSQL is running
echo 2. Create database: createdb skillproof
echo 3. Start Backend:
echo    cd skillproof-backend
echo    uvicorn app.main:app --reload
echo.
echo 4. Start Frontend (in new terminal):
echo    cd skillproof-frontend
echo    npm run dev
echo.
echo 5. Visit: http://localhost:3000/signup
echo.
echo Read AUTHENTICATION_SETUP_COMPLETE.md for detailed instructions!
echo.
pause
