"""
Optimized startup script for disease detection API
Configured for minimal RAM usage (<512MB)
"""

import os
import sys
import psutil
import argparse
from pathlib import Path

def check_system_requirements():
    """Check if system meets minimum requirements"""
    print("Checking system requirements...")
    
    # Check available memory
    memory = psutil.virtual_memory()
    available_gb = memory.available / 1024 / 1024 / 1024
    total_gb = memory.total / 1024 / 1024 / 1024
    
    print(f"System Memory: {total_gb:.1f} GB total, {available_gb:.1f} GB available")
    
    if available_gb < 1:
        print("⚠️ WARNING: Low available memory (<1GB). Performance may be affected.")
        return False
    elif available_gb < 2:
        print("🟡 Limited memory available. Using optimized configuration.")
        return "limited"
    else:
        print("✅ Sufficient memory available.")
        return True

def get_optimal_config(memory_status):
    """Get optimal configuration based on available memory"""
    if memory_status == False:
        return {
            "model_type": "tiny",
            "workers": 1,
            "max_requests": 1,
            "explanations": False,
            "input_size": 112
        }
    elif memory_status == "limited":
        return {
            "model_type": "lite",
            "workers": 1,
            "max_requests": 2,
            "explanations": False,
            "input_size": 224
        }
    else:
        return {
            "model_type": "lite",
            "workers": 1,
            "max_requests": 4,
            "explanations": True,
            "input_size": 224
        }

def setup_environment(config):
    """Setup environment variables for optimization"""
    os.environ["MODEL_TYPE"] = config["model_type"]
    os.environ["MAX_REQUESTS"] = str(config["max_requests"])
    os.environ["ENABLE_EXPLANATIONS"] = str(config["explanations"])
    os.environ["INPUT_SIZE"] = str(config["input_size"])
    
    # PyTorch optimizations
    os.environ["PYTORCH_JIT"] = "0"  # Disable JIT compilation to save memory
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
    
    print(f"Configuration applied: {config}")

def start_api(config):
    """Start the API with optimized settings"""
    try:
        import uvicorn
        
        # Determine which main file to use
        if os.path.exists("api/main_optimized.py"):
            app_module = "api.main_optimized:app"
            print("Using optimized API version")
        else:
            app_module = "api.main:app"
            print("Using standard API version")
        
        print(f"Starting API with {config['workers']} worker(s)...")
        print(f"Maximum concurrent requests: {config['max_requests']}")
        print(f"Explanations enabled: {config['explanations']}")
        
        uvicorn.run(
            app_module,
            host="0.0.0.0",
            port=8001,
            workers=config["workers"],
            limit_concurrency=config["max_requests"],
            log_level="info",
            access_log=False,  # Disable access logs to save memory
            reload=False  # Disable reload for production
        )
        
    except ImportError:
        print("Error: uvicorn not installed. Install with: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting API: {e}")
        sys.exit(1)

def monitor_memory():
    """Monitor memory usage during startup"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    print(f"Initial memory usage: {initial_memory:.1f} MB")
    
    return initial_memory

def main():
    parser = argparse.ArgumentParser(description='Start optimized disease detection API')
    parser.add_argument('--force-config', choices=['tiny', 'lite', 'standard'], 
                       help='Force specific configuration')
    parser.add_argument('--port', type=int, default=8001, help='API port')
    parser.add_argument('--monitor', action='store_true', help='Enable memory monitoring')
    
    args = parser.parse_args()
    
    print("🌱 Disease Detection API - Optimized Startup")
    print("="*50)
    
    # Monitor initial memory
    initial_memory = monitor_memory()
    
    # Check system requirements
    memory_status = check_system_requirements()
    
    # Get optimal configuration
    if args.force_config:
        if args.force_config == "tiny":
            config = {
                "model_type": "tiny",
                "workers": 1,
                "max_requests": 1,
                "explanations": False,
                "input_size": 112
            }
        elif args.force_config == "lite":
            config = {
                "model_type": "lite",
                "workers": 1,
                "max_requests": 2,
                "explanations": False,
                "input_size": 224
            }
        else:  # standard
            config = {
                "model_type": "lite",
                "workers": 1,
                "max_requests": 4,
                "explanations": True,
                "input_size": 224
            }
        print(f"Using forced configuration: {args.force_config}")
    else:
        config = get_optimal_config(memory_status)
    
    # Setup environment
    setup_environment(config)
    
    # Start memory monitoring if requested
    if args.monitor:
        print("Memory monitoring enabled")
        os.environ["ENABLE_MEMORY_MONITORING"] = "1"
    
    print("\n🚀 Starting API...")
    print("="*50)
    
    try:
        # Start the API
        start_api(config)
    except KeyboardInterrupt:
        print("\n⏹️ API stopped by user")
    except Exception as e:
        print(f"\n❌ API failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()