@echo off
echo ========================================
echo Pushing to GitHub Repository
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init

echo.
echo Step 2: Adding remote repository...
git remote add origin https://github.com/roshankumar1113/SatyaHire-AI-Powered-Truthful-Hiring-Platform.git

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Creating commit...
git commit -m "Initial commit: SatyaHire AI Platform with Authentication, AI Interview Agent, and Resume Parser"

echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ========================================
echo Done! Code pushed to GitHub
echo ========================================
echo.
echo Repository: https://github.com/roshankumar1113/SatyaHire-AI-Powered-Truthful-Hiring-Platform
echo.
pause
