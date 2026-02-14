@echo off
echo ====================================
echo Resume Shortlister AI - Starting...
echo ====================================
echo.

echo Starting Ollama service (if not already running)...
start "" ollama serve

echo Waiting for Ollama to initialize...
timeout /t 3 /nobreak >nul

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && .venv\Scripts\activate && python main.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Development Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo All services started!
echo ====================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /FI "WindowTitle eq Backend Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F >nul 2>&1

echo Services stopped.
