"""
Test script for all API endpoints
"""
import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_classes_endpoint():
    """Test the classes endpoint"""
    print("\n🔍 Testing /classes endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/classes")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Number of classes: {len(data.get('classes', []))}")
        print(f"Classes: {data.get('classes', [])[:3]}...")  # Show first 3
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_info_endpoint():
    """Test the model info endpoint"""
    print("\n🔍 Testing /model_info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model_info")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Model info keys: {list(data.keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_endpoint():
    """Test the prediction endpoint"""
    print("\n🔍 Testing /predict endpoint...")
    
    # Check if test image exists
    image_path = "test_leaf_sample.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Prediction: {data.get('predicted_class', 'N/A')}")
            print(f"Confidence: {data.get('confidence', 'N/A')}")
            print(f"Risk Level: {data.get('risk_level', 'N/A')}")
            print(f"Has explanation: {'explanation' in data}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_predict_endpoint():
    """Test the batch prediction endpoint"""
    print("\n🔍 Testing /batch_predict endpoint...")
    
    # Check if test image exists
    image_path = "test_leaf_sample.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    try:
        # Test with single image (simulating batch with one image)
        with open(image_path, 'rb') as f:
            files = {'files': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/batch_predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of results: {len(data.get('results', []))}")
            if data.get('results'):
                first_result = data['results'][0]
                print(f"First result prediction: {first_result.get('predicted_class', 'N/A')}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Classes Endpoint", test_classes_endpoint),
        ("Model Info", test_model_info_endpoint),
        ("Predict Endpoint", test_predict_endpoint),
        ("Batch Predict", test_batch_predict_endpoint)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
        print()
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed!")
    else:
        print("⚠️  Some API tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()
