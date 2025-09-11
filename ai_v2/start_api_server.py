"""
🚀 Production FastAPI Server for Render Deployment
"""
import uvicorn
import sys
import os
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

def main():
    """Start the FastAPI server for production deployment"""
    
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("API_HOST", "0.0.0.0")
    environment = os.environ.get("ENVIRONMENT", "production")
    
    print(f"🌾 Starting Crop AI API Server...")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📱 Environment: {environment}")
    
    if environment == "production":
        print("🔧 Production Mode - API Documentation available at /docs")
        print("🧪 Health check available at /health")
    else:
        print("📖 API Documentation: http://localhost:8000/docs")
        print("🔧 Alternative Docs: http://localhost:8000/redoc")
        print("🧪 Test endpoint: http://localhost:8000/health")
        print("\nPress Ctrl+C to stop the server")
    
    # Configure based on environment
    reload_setting = environment != "production"
    workers = 1  # Single worker for free tier
    
    uvicorn.run(
        "src.api:app",
        host=host,
        port=port,
        reload=reload_setting,
        workers=workers if not reload_setting else None,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
