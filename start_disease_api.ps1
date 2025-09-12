# PowerShell script to start the Disease Detection API
# Run this from the root directory of the project

Write-Host "🌱 Starting Crop Disease Detection API Server..." -ForegroundColor Green
Write-Host "📍 Location: diseases_detection_ai/api/" -ForegroundColor Cyan
Write-Host "🔧 Using Python FastAPI with PyTorch" -ForegroundColor Cyan

# Navigate to disease detection directory
Set-Location "diseases_detection_ai"

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "🐍 Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🚀 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements if needed
Write-Host "📥 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start the API server
Write-Host "" -ForegroundColor White
Write-Host "🌐 Starting FastAPI server on localhost:8001..." -ForegroundColor Green
Write-Host "📊 API Documentation will be available at: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "🔍 Health Check: http://localhost:8001/health" -ForegroundColor Cyan
Write-Host "🔄 Starting server..." -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

# Run the API server
python api/main.py