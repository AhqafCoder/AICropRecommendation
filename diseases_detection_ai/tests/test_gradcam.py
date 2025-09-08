"""
Test script for Grad-CAM functionality
"""
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_gradcam():
    """Test the Grad-CAM implementation"""
    from src.explain import load_model_and_generate_gradcam
    
    # Define paths
    model_path = "models/crop_disease_v2_model.pth"
    image_path = "test_leaf_sample.jpg"
    output_path = "outputs/test_gradcam.jpg"
    
    # Check if files exist
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    print("🧪 Testing Grad-CAM implementation...")
    
    try:
        # Generate Grad-CAM
        result = load_model_and_generate_gradcam(
            model_path=model_path,
            image_path=image_path,
            output_path=output_path
        )
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Grad-CAM test successful!")
        print(f"   Predicted: {result['predicted_class']}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Output saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        return False

if __name__ == "__main__":
    test_gradcam()
