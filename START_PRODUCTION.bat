@echo off
echo ========================================
echo   AI Interview Platform - Production
echo ========================================
echo.

echo [1/6] Checking prerequisites...
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker Compose is not installed!
    pause
    exit /b 1
)

echo ✓ Docker is installed
echo.

echo [2/6] Checking environment file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠ IMPORTANT: Please edit .env file with your credentials!
    echo   - Database passwords
    echo   - JWT secrets
    echo   - AI API keys
    echo.
    pause
)
echo ✓ Environment file exists
echo.

echo [3/6] Stopping existing containers...
docker-compose down
echo ✓ Containers stopped
echo.

echo [4/6] Building Docker images...
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to build Docker images!
    pause
    exit /b 1
)
echo ✓ Images built successfully
echo.

echo [5/6] Starting services...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start services!
    pause
    exit /b 1
)
echo ✓ Services started
echo.

echo [6/6] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo   Services are running!
echo ========================================
echo.
echo   Frontend:        http://localhost:3000
echo   Backend API:     http://localhost:8000
echo   API Docs:        http://localhost:8000/api/docs
echo   RabbitMQ:        http://localhost:15672
echo   Minio Console:   http://localhost:9001
echo.
echo   Database:        localhost:5432
echo   Redis:           localhost:6379
echo.
echo ========================================
echo   Useful Commands:
echo ========================================
echo.
echo   View logs:       docker-compose logs -f
echo   Stop services:   docker-compose down
echo   Restart:         docker-compose restart
echo   Check status:    docker-compose ps
echo.
echo Press any key to view logs...
pause >nul

docker-compose logs -f
