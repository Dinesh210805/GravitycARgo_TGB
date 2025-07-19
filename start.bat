@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ================================================
echo OPTIGENIX - ONE-CLICK STARTER
echo ================================================
echo.
echo This will automatically start:
echo   • Main Flask application
echo   • Socket Mode integration  
echo   • Auto-notifications
echo   • Health monitoring
echo.
echo Press Ctrl+C to stop all services
echo.
python auto_start.py
pause
