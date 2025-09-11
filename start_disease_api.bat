@echo off
REM Start Disease Detection API Server
REM This script starts the FastAPI disease detection server on Windows

echo 🌱 Starting Crop Disease Detection API Server...
echo 📍 Location: diseases_detection_ai/api/
echo 🔧 Using Python FastAPI with PyTorch

REM Navigate to disease detection directory
cd diseases_detection_ai

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if needed
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Start the API server
echo 🌐 Starting FastAPI server on localhost:8001...
echo 📊 API Documentation will be available at: http://localhost:8001/docs
echo 🔍 Health Check: http://localhost:8001/health
echo.
echo 🔄 Starting server...

REM Run the API server
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload