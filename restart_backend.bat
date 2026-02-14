@echo off
REM Quick Restart Backend Script

echo ============================================
echo   RESTARTING BACKEND SERVER
echo ============================================
echo.

cd F:\projects\ruya_AI_hackathon\backend

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting backend server...
echo (Press Ctrl+C to stop)
echo.

python main.py
