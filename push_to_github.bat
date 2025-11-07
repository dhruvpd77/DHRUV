@echo off
echo ========================================
echo QuizNjoy - Push to GitHub
echo Repository: dhruvpd77/quiznjoy
echo Branch: quiznjoyfinal
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Install Git (use default settings)
    echo 3. Restart this terminal/PowerShell
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed!
echo.

REM Initialize git if not already done
if not exist .git (
    echo [STEP 1] Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize git repository
        pause
        exit /b 1
    )
    echo [OK] Repository initialized!
    echo.
) else (
    echo [INFO] Git repository already initialized
    echo.
)

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [STEP 2] Adding GitHub remote...
    git remote add origin https://github.com/dhruvpd77/quiznjoy.git
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to add remote
        pause
        exit /b 1
    )
    echo [OK] Remote added!
    echo.
) else (
    echo [INFO] Remote already exists
    git remote set-url origin https://github.com/dhruvpd77/quiznjoy.git
    echo [OK] Remote URL updated!
    echo.
)

REM Add all files
echo [STEP 3] Adding all files to staging...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] Files added!
echo.

REM Create commit
echo [STEP 4] Creating commit...
git commit -m "Initial commit: QuizNjoy Django project - Full implementation"
if %errorlevel% neq 0 (
    echo [WARNING] Commit failed or no changes to commit
    echo.
)

REM Create and switch to quiznjoyfinal branch
echo [STEP 5] Creating branch 'quiznjoyfinal'...
git checkout -b quiznjoyfinal
if %errorlevel% neq 0 (
    echo [INFO] Branch might already exist, switching to it...
    git checkout quiznjoyfinal
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create/switch branch
        pause
        exit /b 1
    )
)
echo [OK] On branch 'quiznjoyfinal'!
echo.

REM Push to GitHub
echo [STEP 6] Pushing to GitHub...
echo.
echo NOTE: You may be prompted for GitHub credentials.
echo If asked for password, use a Personal Access Token instead.
echo.
git push -u origin quiznjoyfinal
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo 1. Authentication required - use Personal Access Token
    echo 2. Network issues - check internet connection
    echo.
    echo To generate a Personal Access Token:
    echo 1. Go to GitHub.com
    echo 2. Settings ^> Developer settings ^> Personal access tokens ^> Tokens (classic)
    echo 3. Generate new token with 'repo' permissions
    echo 4. Use the token as password when prompted
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Project pushed to GitHub!
echo ========================================
echo.
echo Repository: https://github.com/dhruvpd77/quiznjoy
echo Branch: quiznjoyfinal
echo.
echo You can view your code at:
echo https://github.com/dhruvpd77/quiznjoy/tree/quiznjoyfinal
echo.
pause

