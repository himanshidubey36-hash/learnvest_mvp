@echo off
echo.
echo  =============================================
echo   LearnVest - Gamified Financial Literacy App
echo   Learn Money. Play Smart. Build Wealth.
echo  =============================================
echo.

echo [1/3] Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [2/3] Installing dependencies...
pip install flask --quiet

echo [3/3] Launching LearnVest...
echo.
echo  App running at: http://localhost:5000
echo  Press Ctrl+C to stop the server.
echo.
start "" http://localhost:5000
python app.py
pause
