"""
Integration Test Script for Frontend-Backend Connection
Tests the complete flow from frontend to AI backend
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
FRONTEND_URL = "http://localhost:3000"
AI_BACKEND_URL = "http://localhost:8000"
NEXTJS_API_URL = "http://localhost:3000/api"

def test_ai_backend_direct():
    """Test direct connection to AI backend"""
    print("🔄 Testing direct AI backend connection...")
    
    try:
        # Health check
        response = requests.get(f"{AI_BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI Backend health check passed")
            health_data = response.json()
            print(f"   Models loaded: {health_data.get('models_loaded', 'Unknown')}")
        else:
            print(f"❌ AI Backend health check failed: {response.status_code}")
            return False
            
        # Test prediction
        test_data = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.5,
            "humidity": 82.0,
            "ph": 6.5,
            "rainfall": 200.0,
            "area_ha": 1.0,
            "region": "default",
            "previous_crop": "",
            "season": "kharif",
            "planting_date": ""
        }
        
        response = requests.post(
            f"{AI_BACKEND_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ AI Backend prediction successful")
            result = response.json()
            print(f"   Recommended crop: {result.get('recommended_crop', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.2%}")
            return True
        else:
            print(f"❌ AI Backend prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Backend connection failed: {e}")
        return False

def test_nextjs_api():
    """Test Next.js API route"""
    print("\n🔄 Testing Next.js API route...")
    
    try:
        test_data = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.5,
            "humidity": 82.0,
            "ph": 6.5,
            "rainfall": 200.0,
            "area_ha": 1.0,
            "region": "default",
            "previous_crop": "",
            "season": "kharif",
            "planting_date": ""
        }
        
        response = requests.post(
            f"{NEXTJS_API_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Next.js API route successful")
            result = response.json()
            print(f"   Recommended crop: {result.get('recommended_crop', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.2%}")
            return True
        else:
            print(f"❌ Next.js API route failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Next.js API connection failed: {e}")
        return False

def test_frontend_page():
    """Test frontend page accessibility"""
    print("\n🔄 Testing frontend page...")
    
    try:
        response = requests.get(f"{FRONTEND_URL}/recommend", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend page accessible")
            return True
        else:
            print(f"❌ Frontend page failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def run_performance_test():
    """Run a quick performance test"""
    print("\n🔄 Running performance test...")
    
    test_data = {
        "N": 80.0,
        "P": 40.0,
        "K": 40.0,
        "temperature": 27.0,
        "humidity": 80.0,
        "ph": 6.0,
        "rainfall": 1200.0,
        "area_ha": 3.0,
        "region": "south",
        "previous_crop": "",
        "season": "kharif",
        "planting_date": ""
    }
    
    times = []
    successful_requests = 0
    
    for i in range(5):
        try:
            start_time = time.time()
            response = requests.post(
                f"{NEXTJS_API_URL}/predict",
                json=test_data,
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                successful_requests += 1
                times.append(end_time - start_time)
                print(f"   Request {i+1}: {(end_time - start_time):.2f}s ✅")
            else:
                print(f"   Request {i+1}: Failed ({response.status_code}) ❌")
                
        except requests.exceptions.RequestException as e:
            print(f"   Request {i+1}: Exception ({e}) ❌")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"\n📊 Performance Results:")
        print(f"   Successful requests: {successful_requests}/5")
        print(f"   Average response time: {avg_time:.2f}s")
        print(f"   Min response time: {min(times):.2f}s")
        print(f"   Max response time: {max(times):.2f}s")
    else:
        print("❌ No successful requests for performance analysis")

def main():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test AI Backend
    if test_ai_backend_direct():
        tests_passed += 1
    
    # Test Next.js API
    if test_nextjs_api():
        tests_passed += 1
    
    # Test Frontend
    if test_frontend_page():
        tests_passed += 1
    
    # Performance test (optional)
    run_performance_test()
    
    print("\n" + "=" * 50)
    print(f"🎯 Integration Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Frontend and backend are properly connected.")
        print("\n🌐 Access the application at:")
        print(f"   Frontend: {FRONTEND_URL}/recommend")
        print(f"   API Docs: {AI_BACKEND_URL}/docs")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        
    return tests_passed == total_tests

if __name__ == "__main__":
    main()