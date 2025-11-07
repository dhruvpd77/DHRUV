@echo off
REM QuizNjoy Excel File Fixer - Batch Script
REM Just double-click this file to fix your Excel!

color 0A
echo.
echo ============================================================
echo    QuizNjoy - Excel File Fixer
echo ============================================================
echo.
echo This script will fix corrupted Excel files automatically.
echo.
echo ============================================================
echo.

REM Get the file path
set /p filepath="Drag and drop your Excel file here (or paste path): "

REM Remove quotes if present
set filepath=%filepath:"=%

REM Check if file exists
if not exist "%filepath%" (
    color 0C
    echo.
    echo ERROR: File not found!
    echo Please check the path and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo Starting file repair...
echo.

REM Run the Python fixer
python fix_excel_file.py "%filepath%"

echo.
echo ============================================================
echo.
pause
