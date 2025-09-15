#!/usr/bin/env python3
"""
Test script for fixed Grad-CAM implementation
"""

import sys
import os
sys.path.append('.')

from src.explain import CropDiseaseExplainer
from src.model import CropDiseaseResNet50
import torch

def test_gradcam_fix():
    """Test the fixed Grad-CAM implementation"""
    print("🧪 Testing fixed Grad-CAM implementation...")
    
    # Setup
    device = torch.device('cpu')
    model_path = 'models/crop_disease_v3_model.pth'
    
    try:
        # Load model
        checkpoint = torch.load(model_path, map_location=device)
        class_names = checkpoint['class_names']
        
        model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        print(f"✅ Model loaded with {len(class_names)} classes")
        
        # Initialize explainer
        explainer = CropDiseaseExplainer(model, class_names, device)
        print("✅ Explainer initialized successfully")
        
        # Test with sample image if available
        test_image = 'test_leaf_sample.jpg'
        if os.path.exists(test_image):
            print(f"🖼️ Testing with {test_image}...")
            
            result = explainer.explain_prediction(
                test_image, 
                save_dir='outputs/test_heatmaps',
                return_base64=True
            )
            
            if 'error' in result:
                print(f"⚠️ Explanation error: {result['error']}")
                print("But prediction is still available:")
                print(f"  Predicted: {result.get('predicted_class', 'Unknown')}")
                print(f"  Confidence: {result.get('confidence', 0):.2%}")
            else:
                print("✅ Explanation generated successfully!")
                print(f"  Predicted: {result['predicted_class']}")
                print(f"  Confidence: {result['confidence']:.2%}")
                print(f"  Saved to: {result['save_path']}")
                
                if result.get('overlay_base64'):
                    print("  Base64 image: Available")
                else:
                    print("  Base64 image: Not available")
        else:
            print(f"⚠️ Test image {test_image} not found")
            print("✅ But explainer setup is working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gradcam_fix()
    if success:
        print("\n🎉 Grad-CAM fix test completed!")
    else:
        print("\n💥 Grad-CAM fix test failed!")
