"""
Simple API test script
"""
import requests
import json

def test_endpoints():
    """Test basic API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 40)
    
    # Test health
    print("1. Testing /health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test classes
    print("2. Testing /classes...")
    try:
        response = requests.get(f"{base_url}/classes", timeout=10)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Classes: {len(data['classes'])} total")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test model info
    print("3. Testing /model_info...")
    try:
        response = requests.get(f"{base_url}/model_info", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Model: {data['model_name']}")
            print(f"   Device: {data['device']}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test prediction (if test image exists)
    print("4. Testing /predict...")
    try:
        import os
        if os.path.exists("test_leaf_sample.jpg"):
            with open("test_leaf_sample.jpg", "rb") as f:
                files = {"file": ("test.jpg", f, "image/jpeg")}
                response = requests.post(f"{base_url}/predict", files=files, timeout=30)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Prediction: {data.get('predicted_class', 'N/A')}")
                print(f"   Confidence: {data.get('confidence', 'N/A'):.2%}")
            else:
                print(f"   Error: {response.text}")
        else:
            print("   Test image not found")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_endpoints()
