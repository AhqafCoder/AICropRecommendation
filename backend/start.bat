@echo off
echo Starting CropAI Marketplace & Analytics Backend Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo.
echo ========================================
echo  CropAI Backend Server Starting...
echo ========================================
echo  API URL: http://localhost:8001
echo  Documentation: http://localhost:8001/docs
echo  Redoc: http://localhost:8001/redoc
echo ========================================
echo.

python app.py

pause
