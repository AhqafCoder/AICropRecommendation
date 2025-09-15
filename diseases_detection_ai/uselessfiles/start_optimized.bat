@echo off
echo Starting Memory-Optimized Disease Detection API
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "api\main_optimized.py" (
    echo Error: Please run this script from the diseases_detection_ai directory
    pause
    exit /b 1
)

REM Install optimized requirements if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing optimized requirements...
pip install -r requirements_optimized.txt

echo Starting optimized API...
python start_optimized.py

pause