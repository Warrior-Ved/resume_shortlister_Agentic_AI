@echo off
REM Quick Resume Upload Script
REM Just double-click this file and enter your PDF filename!

echo ============================================
echo    RESUME SHORTLISTER - QUICK UPLOAD
echo ============================================
echo.

REM Check if backend virtual environment exists
if not exist "backend\.venv" (
    echo ERROR: Backend not set up!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
cd backend
call .venv\Scripts\activate.bat

echo.
echo Starting automated resume upload...
echo.

REM Run the upload script in interactive mode
python upload_and_process.py --interactive

echo.
echo ============================================
pause
