@echo off
echo ========================================
echo Installing Backend Dependencies
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo Installing core dependencies...
pip install fastapi==0.109.0
pip install "uvicorn[standard]==0.27.0"
pip install python-multipart==0.0.6
pip install sqlalchemy==2.0.25
pip install psycopg2-binary
pip install alembic==1.13.1
pip install pydantic==2.5.3
pip install pydantic-settings==2.1.0
pip install email-validator==2.1.0
pip install "python-jose[cryptography]==3.3.0"
pip install "passlib[bcrypt]==1.7.4"
pip install python-dotenv==1.0.0

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now run: python -m uvicorn app.main:app --reload
echo.
pause
