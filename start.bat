@echo off
echo ========================================
echo PrivyLoans - React + Flask Application
echo ========================================
echo.

echo Starting Flask API Backend...
start cmd /k "python api.py"

timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start cmd /k "npm run dev"

echo.
echo ========================================
echo Application is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to stop all servers...
pause > nul

taskkill /F /FI "WINDOWTITLE eq *api.py*"
taskkill /F /FI "WINDOWTITLE eq *npm run dev*"
