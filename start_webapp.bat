@echo off
TITLE 5-Agent Indian Fund Deployment Advisory Web App
COLOR 0A
cls
echo ======================================================================
echo    5-AGENT INDIAN FUND DEPLOYMENT ADVISORY WEB APPLICATION
echo    Jasoos * Explorer * GrihaLaxmi * SafetyPriya * Buddhiman
echo ======================================================================
echo.
echo Starting web app on Port 8010...
echo Opening browser at http://127.0.0.1:8010
echo.

cd /d "%~dp0"
py -3.14 run.py --port 8010

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [Fallback] Trying standard python launcher...
    py run.py --port 8010
)

pause
