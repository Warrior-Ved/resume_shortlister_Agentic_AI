@echo off
REM Example: Upload Python Developer Resumes
REM Customize this file for your specific needs

echo ============================================
echo   Python Developer Resume Upload
echo ============================================
echo.

cd backend
call .venv\Scripts\activate.bat

REM Customize these parameters for your job
python upload_and_process.py ^
    --pdf "python_developer_resumes.pdf" ^
    --job-title "Senior Python Developer" ^
    --description "Looking for experienced Python developer with backend expertise" ^
    --skills "Python,Django,FastAPI,PostgreSQL,Docker,AWS" ^
    --experience 5 ^
    --hiring-slots 2 ^
    --phase1-count 10 ^
    --phase2-count 5

echo.
echo ============================================
echo Process completed!
echo Check the output above for results.
echo ============================================
pause
