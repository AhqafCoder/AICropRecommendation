# 🚀 PowerShell Deployment Script for Render
# Windows users can run this instead of the bash script

Write-Host "🌾 Preparing Crop AI for Render Deployment..." -ForegroundColor Green
Write-Host ""

# Check if required files exist
Write-Host "🔍 Checking deployment files..." -ForegroundColor Cyan

$requiredFiles = @("Dockerfile", "requirements.txt", "start_api_server.py", "src\api.py")

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing!" -ForegroundColor Red
        exit 1
    }
}

# Check if models directory exists
if (Test-Path "models") {
    Write-Host "✅ Models directory exists" -ForegroundColor Green
    Write-Host "📊 Model files:" -ForegroundColor Cyan
    Get-ChildItem models\ | Format-Table Name, Length, LastWriteTime
} else {
    Write-Host "⚠️  Models directory not found" -ForegroundColor Yellow
}

# Check Docker installation
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker is installed" -ForegroundColor Green
    
    # Build and test Docker image locally
    Write-Host "🐳 Building Docker image for testing..." -ForegroundColor Cyan
    docker build -t crop-ai-test .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker image built successfully" -ForegroundColor Green
        
        Write-Host "🧪 Testing Docker container..." -ForegroundColor Cyan
        docker run -d --name crop-ai-test -p 8001:8000 crop-ai-test
        
        # Wait for container to start
        Start-Sleep 10
        
        # Test health endpoint
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 5
            Write-Host "✅ Health check passed" -ForegroundColor Green
        } catch {
            Write-Host "❌ Health check failed" -ForegroundColor Red
            docker logs crop-ai-test
        }
        
        # Cleanup
        docker stop crop-ai-test
        docker rm crop-ai-test
        docker rmi crop-ai-test
        
    } else {
        Write-Host "❌ Docker build failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  Docker not found - skipping local test" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Ready for Render deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Push your code to GitHub:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Ready for Render deployment'" -ForegroundColor Gray
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Go to render.com and create a new Web Service" -ForegroundColor White
Write-Host "3. Connect your GitHub repository" -ForegroundColor White
Write-Host "4. Use these settings:" -ForegroundColor White
Write-Host "   - Runtime: Docker" -ForegroundColor Gray
Write-Host "   - Build Command: (automatic from Dockerfile)" -ForegroundColor Gray
Write-Host "   - Start Command: (automatic from Dockerfile)" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Your Crop AI will be live soon!" -ForegroundColor Green
