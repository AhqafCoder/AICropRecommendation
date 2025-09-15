# FastAPI Crop AI Server Startup Script
# Usage: .\start_fastapi_server.ps1

Write-Host "🚀 Starting Crop AI FastAPI Server..." -ForegroundColor Green
Write-Host "📖 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🔧 Alternative Docs: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "🧪 Test endpoint: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Blue
    & .\venv\Scripts\Activate.ps1
}

# Start the FastAPI server
try {
    python start_api_server.py
} catch {
    Write-Host "❌ Failed to start server: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Python and required packages are installed." -ForegroundColor Yellow
}

Write-Host "Server stopped." -ForegroundColor Yellow
