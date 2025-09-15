# 🚀 Crop AI Streamlit GUI Launcher
# PowerShell script to run the Streamlit GUI properly

Write-Host "🚀 Starting Crop AI Streamlit GUI..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 The app will open in your default browser" -ForegroundColor Cyan
Write-Host "🌐 URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Get the directory of this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to the script directory
Set-Location $scriptDir

# Activate virtual environment
& "$scriptDir\venv\Scripts\Activate.ps1"

# Run Streamlit
streamlit run ai_test_gui.py --server.port=8501 --server.address=localhost
