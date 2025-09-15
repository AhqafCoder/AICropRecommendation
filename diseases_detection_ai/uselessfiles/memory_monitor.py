"""
Memory usage monitoring and optimization script
Helps monitor and optimize RAM usage for the disease detection system
"""

import psutil
import torch
import gc
import os
import time
from pathlib import Path

class MemoryMonitor:
    """Monitor and optimize memory usage"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.get_memory_usage()
        self.peak_memory = self.initial_memory
        
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_memory_percent(self):
        """Get memory usage as percentage of total system memory"""
        return self.process.memory_percent()
    
    def get_system_memory_info(self):
        """Get system memory information"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": memory.total / 1024 / 1024 / 1024,
            "available_gb": memory.available / 1024 / 1024 / 1024,
            "used_percent": memory.percent,
            "free_gb": memory.free / 1024 / 1024 / 1024
        }
    
    def optimize_memory(self):
        """Force memory optimization"""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def check_memory_status(self):
        """Check if memory usage is within acceptable limits"""
        current = self.get_memory_usage()
        self.peak_memory = max(self.peak_memory, current)
        
        status = {
            "current_mb": current,
            "peak_mb": self.peak_memory,
            "increase_mb": current - self.initial_memory,
            "within_512mb": current < 512,
            "system_percent": self.get_memory_percent(),
            "status": "OK" if current < 512 else "HIGH"
        }
        
        return status
    
    def print_memory_report(self):
        """Print detailed memory report"""
        status = self.check_memory_status()
        system_info = self.get_system_memory_info()
        
        print("\n" + "="*50)
        print("MEMORY USAGE REPORT")
        print("="*50)
        print(f"Process Memory Usage:")
        print(f"  Current: {status['current_mb']:.1f} MB")
        print(f"  Peak: {status['peak_mb']:.1f} MB")
        print(f"  Increase: {status['increase_mb']:.1f} MB")
        print(f"  Status: {status['status']}")
        print(f"  Within 512MB limit: {'✅' if status['within_512mb'] else '❌'}")
        
        print(f"\nSystem Memory:")
        print(f"  Total: {system_info['total_gb']:.1f} GB")
        print(f"  Available: {system_info['available_gb']:.1f} GB")
        print(f"  Used: {system_info['used_percent']:.1f}%")
        
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.memory_allocated() / 1024 / 1024
            gpu_cached = torch.cuda.memory_reserved() / 1024 / 1024
            print(f"\nGPU Memory:")
            print(f"  Allocated: {gpu_memory:.1f} MB")
            print(f"  Cached: {gpu_cached:.1f} MB")
        
        print("="*50)
        
        return status

def test_model_memory_usage():
    """Test memory usage of different model configurations"""
    monitor = MemoryMonitor()
    
    print("Testing memory usage of disease detection models...")
    monitor.print_memory_report()
    
    try:
        # Test importing modules
        print("\n1. Testing module imports...")
        
        import sys
        sys.path.append('src')
        
        from src.model_lite import CropDiseaseResNet50Lite, TinyDiseaseClassifier
        monitor.optimize_memory()
        
        status = monitor.check_memory_status()
        print(f"After imports: {status['current_mb']:.1f} MB")
        
        # Test lite model
        print("\n2. Testing CropDiseaseResNet50Lite...")
        model_lite = CropDiseaseResNet50Lite(15, pretrained=False)
        
        status = monitor.check_memory_status()
        print(f"After lite model creation: {status['current_mb']:.1f} MB")
        print(f"Model size: {model_lite.get_model_size():.1f} MB")
        
        # Test with dummy input
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model_lite(dummy_input)
        
        status = monitor.check_memory_status()
        print(f"After inference: {status['current_mb']:.1f} MB")
        
        del model_lite, dummy_input, output
        monitor.optimize_memory()
        
        # Test tiny model
        print("\n3. Testing TinyDiseaseClassifier...")
        model_tiny = TinyDiseaseClassifier(15)
        
        status = monitor.check_memory_status()
        print(f"After tiny model creation: {status['current_mb']:.1f} MB")
        print(f"Model size: {model_tiny.get_model_size():.1f} MB")
        
        # Test with dummy input
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model_tiny(dummy_input)
        
        status = monitor.check_memory_status()
        print(f"After inference: {status['current_mb']:.1f} MB")
        
        del model_tiny, dummy_input, output
        monitor.optimize_memory()
        
    except Exception as e:
        print(f"Error during testing: {e}")
    
    print("\n4. Final memory report:")
    monitor.print_memory_report()
    
    return monitor

def benchmark_memory_usage():
    """Benchmark memory usage with continuous monitoring"""
    monitor = MemoryMonitor()
    
    print("Starting memory benchmark...")
    
    try:
        # Simulate API startup
        print("Simulating API startup...")
        
        import sys
        sys.path.append('src')
        
        from src.model_lite import CropDiseaseResNet50Lite
        from src.explain_lite import CropDiseaseExplainerLite
        
        # Load model
        model = CropDiseaseResNet50Lite(15, pretrained=False)
        model.eval()
        
        # Initialize explainer
        explainer = CropDiseaseExplainerLite(model, ["class1", "class2"], 'cpu')
        
        status = monitor.check_memory_status()
        print(f"After model loading: {status['current_mb']:.1f} MB")
        
        # Simulate multiple predictions
        print("Simulating predictions...")
        for i in range(5):
            dummy_input = torch.randn(1, 3, 224, 224)
            
            with torch.no_grad():
                output = model(dummy_input)
            
            # Cleanup after each prediction
            del dummy_input, output
            monitor.optimize_memory()
            
            status = monitor.check_memory_status()
            print(f"Prediction {i+1}: {status['current_mb']:.1f} MB")
        
        print("\nFinal benchmark results:")
        monitor.print_memory_report()
        
    except Exception as e:
        print(f"Benchmark error: {e}")
        monitor.print_memory_report()

def get_optimization_recommendations():
    """Get memory optimization recommendations"""
    monitor = MemoryMonitor()
    system_info = monitor.get_system_memory_info()
    
    recommendations = []
    
    if system_info["total_gb"] < 2:
        recommendations.append("🔴 Very low system memory. Use TinyDiseaseClassifier instead of ResNet50")
        recommendations.append("🔴 Disable explanations completely")
        recommendations.append("🔴 Set max_workers=1 for API")
    
    elif system_info["total_gb"] < 4:
        recommendations.append("🟡 Low system memory. Use CropDiseaseResNet50Lite")
        recommendations.append("🟡 Enable memory efficient mode")
        recommendations.append("🟡 Limit concurrent requests to 2")
    
    else:
        recommendations.append("🟢 Sufficient system memory for standard operation")
        recommendations.append("🟢 Can use full model with optimizations")
    
    if system_info["used_percent"] > 80:
        recommendations.append("⚠️ High system memory usage. Close other applications")
    
    print("\nMEMORY OPTIMIZATION RECOMMENDATIONS:")
    print("="*50)
    for rec in recommendations:
        print(rec)
    print("="*50)
    
    return recommendations

if __name__ == "__main__":
    print("Disease Detection Memory Monitor")
    print("="*50)
    
    # Run tests
    print("1. Testing model memory usage...")
    test_model_memory_usage()
    
    print("\n2. Running memory benchmark...")
    benchmark_memory_usage()
    
    print("\n3. Getting optimization recommendations...")
    get_optimization_recommendations()
    
    print("\nMemory monitoring complete!")