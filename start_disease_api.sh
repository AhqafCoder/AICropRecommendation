#!/bin/bash

# Start Disease Detection API Server
# This script starts the FastAPI disease detection server

echo "🌱 Starting Crop Disease Detection API Server..."
echo "📍 Location: diseases_detection_ai/api/"
echo "🔧 Using Python FastAPI with PyTorch"

# Navigate to disease detection directory
cd diseases_detection_ai

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Install requirements if needed
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Start the API server
echo "🌐 Starting FastAPI server on localhost:8001..."
echo "📊 API Documentation will be available at: http://localhost:8001/docs"
echo "🔍 Health Check: http://localhost:8001/health"
echo ""
echo "🔄 Starting server..."

# Run the API server
python api/main.py --host 0.0.0.0 --port 8001