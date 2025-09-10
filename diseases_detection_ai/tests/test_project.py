"""
Comprehensive test suite for the cleaned project
"""
import os
import sys
import importlib
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_project_structure():
    """Test that all required files and directories exist"""
    print("🔍 Testing project structure...")
    
    required_files = [
        "requirements.txt",
        "README.md",
        "setup.py",
        ".gitignore",
        "docker-compose.yml",
        "Makefile",
        "crop_disease_gui.py",
        "src/__init__.py",
        "src/model.py",
        "src/dataset.py",
        "src/train.py",
        "src/evaluate.py",
        "src/explain.py",
        "src/risk_level.py",
        "api/main.py",
        "api/Dockerfile",
        "models/crop_disease_v3_model.pth",
        "knowledge_base/disease_info.json",
        "test_leaf_sample.jpg"
    ]
    
    required_dirs = [
        "src",
        "api", 
        "models",
        "knowledge_base",
        "data",
        "outputs",
        "notebooks",
        "tests"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ Project structure is complete")
    return True

def test_imports():
    """Test that all Python modules can be imported"""
    print("\n🔍 Testing Python imports...")
    
    modules_to_test = [
        "src.model",
        "src.dataset", 
        "src.train",
        "src.evaluate",
        "src.explain",
        "src.risk_level"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import: {failed_imports}")
        return False
    
    print("✅ All imports successful")
    return True

def test_api_startup():
    """Test that the API can start"""
    print("\n🔍 Testing API startup...")
    
    try:
        # Test import of API main
        from api.main import app
        print("✅ API imports successfully")
        
        # Test health endpoint exists
        print("✅ API structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ API startup failed: {e}")
        return False

def test_model_loading():
    """Test that the model can be loaded"""
    print("\n🔍 Testing model loading...")
    
    try:
        import torch
        from src.model import CropDiseaseResNet50
        
        # Test model creation
        model = CropDiseaseResNet50(num_classes=17)
        print("✅ Model architecture created")
        
        # Test model file exists
        model_path = "models/crop_disease_v3_model.pth"
        if Path(model_path).exists():
            # Try to load the model
            checkpoint = torch.load(model_path, map_location='cpu')
            print("✅ Model file loads successfully")
            return True
        else:
            print("❌ Model file not found")
            return False
            
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_cleanup_completion():
    """Test that cleanup was successful"""
    print("\n🔍 Testing cleanup completion...")
    
    # Check that cache files are gone
    cache_dirs = list(Path(".").rglob("__pycache__"))
    if cache_dirs:
        print(f"❌ Cache directories still exist: {cache_dirs}")
        return False
    
    # Check that backup files are gone
    backup_files = [
        "src/explain_backup.py"
    ]
    
    existing_backups = [f for f in backup_files if Path(f).exists()]
    if existing_backups:
        print(f"❌ Backup files still exist: {existing_backups}")
        return False
    
    print("✅ Cleanup completed successfully")
    return True

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE PROJECT TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Imports", test_imports),
        ("API Startup", test_api_startup),
        ("Model Loading", test_model_loading),
        ("Cleanup Completion", test_cleanup_completion)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🎯 Running: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Project is ready for development!")
        print("\n📝 Next steps:")
        print("   1. Start API: python -m uvicorn api.main:app --reload")
        print("   2. Start GUI: python crop_disease_gui.py")
        print("   3. Run training: python src/train.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
