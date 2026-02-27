@echo off
echo ========================================
echo Starting Web Application Servers
echo ========================================
echo.
echo Starting Frontend on http://localhost:8080
start cmd /k "cd /d %~dp0 && python -m http.server 8080 --directory frontend"
timeout /t 2 /nobreak >nul
echo.
echo Starting Backend API on http://localhost:8000
start cmd /k "cd /d %~dp0\backend && uvicorn app:app --reload --host 127.0.0.1 --port 8000"
timeout /t 2 /nobreak >nul
echo.
echo ========================================
echo Servers Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:8080/complete_analysis.html
echo Backend API: http://localhost:8000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080/complete_analysis.html
echo.
echo Press any key to stop servers...
pause >nul
