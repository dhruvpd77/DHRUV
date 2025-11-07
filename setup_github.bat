@echo off
echo ========================================
echo QuizNjoy GitHub Setup Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Install and restart this terminal
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed!
echo.

REM Check if already a git repository
if exist .git (
    echo [INFO] Git repository already initialized
) else (
    echo [STEP 1] Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize git repository
        pause
        exit /b 1
    )
    echo [OK] Repository initialized!
    echo.
)

echo [STEP 2] Adding files to staging...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] Files added!
echo.

echo [STEP 3] Creating initial commit...
git commit -m "Initial commit: QuizNjoy Django project"
if %errorlevel% neq 0 (
    echo [WARNING] Commit failed. This might be normal if there are no changes.
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Go to https://github.com and create a new repository
echo 2. Copy the repository URL (e.g., https://github.com/YOUR_USERNAME/QuizNjoy.git)
echo 3. Run these commands:
echo.
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo OR use the commands below after creating your repository:
echo.
echo ========================================
echo.
pause

