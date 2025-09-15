"""
FastAPI Crop AI Server Startup Script
"""
import uvicorn
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("🚀 Starting Crop AI FastAPI Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative Docs: http://localhost:8000/redoc")
    print("🧪 Test endpoint: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
