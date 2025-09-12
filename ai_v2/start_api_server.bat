@echo off
echo Starting Crop AI API Server...
echo.

REM Change to ai_v2 directory
cd /d "C:\Users\AHQAF ALI\Desktop\GUTHUB\hackbhoomi2025\ai_v2"

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install API requirements if needed
echo Installing/updating API requirements...
pip install -r requirements_api.txt

REM Start the API server
echo.
echo Starting FastAPI server...
echo API Documentation will be available at: http://localhost:8000/docs
echo Health check: http://localhost:8000/health
echo.
python api_server.py

pause