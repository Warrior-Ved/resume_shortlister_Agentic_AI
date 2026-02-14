@echo off
echo ====================================
echo Resume Shortlister AI - Setup Script
echo ====================================
echo.

echo [1/5] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed!
    echo Please install Ollama from: https://ollama.ai
    pause
    exit /b 1
)
echo Ollama found!
echo.

echo [2/5] Pulling Ministral 3B model...
ollama pull ministral-3:3b
if %errorlevel% neq 0 (
    echo ERROR: Failed to pull model!
    pause
    exit /b 1
)
echo Model pulled successfully!
echo.

echo [3/5] Setting up Backend...
cd backend
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist resumes mkdir resumes

cd ..
echo Backend setup complete!
echo.

echo [4/5] Setting up Frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install

cd ..
echo Frontend setup complete!
echo.

echo [5/5] Setup Complete!
echo.
echo ====================================
echo Next Steps:
echo ====================================
echo 1. Make sure Ollama is running: ollama serve
echo 2. Start backend: cd backend ^&^& .venv\Scripts\activate ^&^& python main.py
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo 4. Open browser: http://localhost:3000
echo.
echo ====================================
pause
