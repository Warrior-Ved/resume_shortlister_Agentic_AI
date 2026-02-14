@echo off
REM Simple Resume Upload - Just Run This!
REM Edit simple_upload.py to change PDF path and job details

echo ============================================
echo   SIMPLE RESUME UPLOADER
echo ============================================
echo.
echo Make sure you edited simple_upload.py first!
echo Change PDF_PATH and other variables at the top.
echo.
pause

cd backend
call .venv\Scripts\activate.bat

python simple_upload.py

echo.
pause
