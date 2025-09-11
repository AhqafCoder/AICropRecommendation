#!/bin/bash
# 🚀 Deploy to Render Script

echo "🌾 Preparing Crop AI for Render Deployment..."

# Check if required files exist
echo "🔍 Checking deployment files..."

required_files=("Dockerfile" "requirements.txt" "start_api_server.py" "src/api.py")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing!"
        exit 1
    fi
done

# Check if models directory exists
if [ -d "models" ]; then
    echo "✅ Models directory exists"
    echo "📊 Model files:"
    ls -la models/
else
    echo "⚠️  Models directory not found"
fi

# Build and test Docker image locally
echo "🐳 Building Docker image for testing..."
docker build -t crop-ai-test .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
    
    echo "🧪 Testing Docker container..."
    docker run -d --name crop-ai-test -p 8001:8000 crop-ai-test
    
    # Wait for container to start
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
        docker logs crop-ai-test
    fi
    
    # Cleanup
    docker stop crop-ai-test
    docker rm crop-ai-test
    docker rmi crop-ai-test
    
else
    echo "❌ Docker build failed"
    exit 1
fi

echo "🎯 Ready for Render deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to render.com and create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Use these settings:"
echo "   - Runtime: Docker"
echo "   - Build Command: (automatic from Dockerfile)"
echo "   - Start Command: (automatic from Dockerfile)"
echo ""
echo "🚀 Your Crop AI will be live soon!"
