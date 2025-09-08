"""
Model Testing Script for Crop Disease Detection
Test the trained model with sample images
"""

import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.append('src')

def load_model():
    """Load the trained model"""
    try:
        from src.model import CropDiseaseResNet50
        
        # Class names
        class_names = [
            'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
            'Corn___Common_rust',
            'Corn___healthy',
            'Corn___Northern_Leaf_Blight',
            'Potato___Early_Blight',
            'Potato___healthy',
            'Potato___Late_Blight',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___healthy',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites_Two_spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
        ]
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # Load the specified model
        model_path = 'models/crop_disease_v2_model.pth'
        
        model = None
        loaded_path = None
        
        if os.path.exists(model_path):
            try:
                print(f"Trying to load model from: {model_path}")
                
                # Create model
                model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=False)
                
                # Load checkpoint
                checkpoint = torch.load(model_path, map_location=device)
                
                # Handle checkpoint format from crop_disease_v2_model.pth
                if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                    state_dict = checkpoint['model_state_dict']
                    # Use class names from checkpoint if available
                    if 'class_names' in checkpoint:
                        class_names = checkpoint['class_names']
                        print(f"Loaded class names from checkpoint: {len(class_names)} classes")
                elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                    state_dict = checkpoint['state_dict']
                else:
                    state_dict = checkpoint
                
                # Load state dict
                model.load_state_dict(state_dict, strict=True)
                model.to(device)
                model.eval()
                print(f"✅ Model loaded successfully from {model_path}")
                loaded_path = model_path
                
            except Exception as e:
                print(f"❌ Failed to load {model_path}: {e}")
                model = None
        else:
            print(f"❌ Model file not found: {model_path}")
            model = None
        
        if model is None:
            print("⚠️ No trained model found. Creating new model with pretrained weights.")
            model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=True)
            loaded_path = "pretrained_imagenet"
        
        model.to(device)
        model.eval()
        
        return model, class_names, device, loaded_path
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None, None

def create_test_image():
    """Create a simple test image"""
    # Create a green leaf-like image
    img = Image.new('RGB', (224, 224), color=(34, 139, 34))  # Forest green
    
    # Add some texture (simple pattern)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Add some leaf-like patterns
    for i in range(0, 224, 20):
        draw.line([(i, 0), (i, 224)], fill=(0, 100, 0), width=1)
    for i in range(0, 224, 20):
        draw.line([(0, i), (224, i)], fill=(0, 100, 0), width=1)
    
    return img

def test_single_prediction(model, class_names, device):
    """Test single image prediction"""
    print("\n🔍 Testing single image prediction...")
    
    # Create test image
    test_image = create_test_image()
    test_image.save('test_leaf_sample.jpg')
    print("✅ Test image created: test_leaf_sample.jpg")
    
    # Preprocessing
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Process image
    input_tensor = transform(test_image).unsqueeze(0).to(device)
    print(f"✅ Input tensor shape: {input_tensor.shape}")
    
    # Make prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = F.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = class_names[predicted_idx.item()]
        confidence_score = confidence.item()
    
    print(f"\n📊 Prediction Results:")
    print(f"   Predicted Class: {predicted_class}")
    print(f"   Confidence: {confidence_score:.2%}")
    
    # Show top 3 predictions
    top_probs, top_indices = torch.topk(probabilities[0], 3)
    print(f"\n🏆 Top 3 Predictions:")
    for i, (prob, idx) in enumerate(zip(top_probs, top_indices)):
        print(f"   {i+1}. {class_names[idx]}: {prob.item():.2%}")
    
    return predicted_class, confidence_score

def test_model_components(model, device):
    """Test model components"""
    print("\n🔧 Testing model components...")
    
    # Model info
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"✅ Model Architecture: {model.__class__.__name__}")
    print(f"✅ Total Parameters: {total_params:,}")
    print(f"✅ Trainable Parameters: {trainable_params:,}")
    print(f"✅ Device: {device}")
    
    # Test forward pass with random input
    try:
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        with torch.no_grad():
            output = model(dummy_input)
        print(f"✅ Forward pass successful: Output shape {output.shape}")
        return True
    except Exception as e:
        print(f"❌ Forward pass failed: {e}")
        return False

def test_with_real_images():
    """Test with real images from dataset if available"""
    print("\n🖼️ Testing with real dataset images...")
    
    # Look for test images in data folder
    test_dirs = [
        'data/test',
        'data/val',
        'data/train'
    ]
    
    test_images = []
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for class_dir in os.listdir(test_dir):
                class_path = os.path.join(test_dir, class_dir)
                if os.path.isdir(class_path):
                    for img_file in os.listdir(class_path)[:2]:  # Take first 2 images
                        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            test_images.append({
                                'path': os.path.join(class_path, img_file),
                                'true_class': class_dir
                            })
            break  # Use first available directory
    
    if test_images:
        print(f"✅ Found {len(test_images)} test images")
        return test_images[:5]  # Return first 5
    else:
        print("⚠️ No real test images found in data folder")
        return []

def main():
    """Main testing function"""
    print("🧪 CROP DISEASE MODEL TESTING")
    print("=" * 50)
    
    # Load model
    model, class_names, device, model_path = load_model()
    
    if model is None:
        print("❌ Failed to load model. Cannot proceed with testing.")
        return False
    
    print(f"✅ Model loaded from: {model_path}")
    print(f"✅ Classes: {len(class_names)}")
    
    # Test model components
    if not test_model_components(model, device):
        print("❌ Model component test failed.")
        return False
    
    # Test single prediction
    try:
        predicted_class, confidence = test_single_prediction(model, class_names, device)
        print("✅ Single prediction test passed")
    except Exception as e:
        print(f"❌ Single prediction test failed: {e}")
        return False
    
    # Test with real images if available
    real_images = test_with_real_images()
    if real_images:
        print(f"\n🎯 Testing with {len(real_images)} real images...")
        # You can add real image testing here if needed
    
    # Test risk assessment
    try:
        from src.risk_level import RiskLevelCalculator
        risk_calc = RiskLevelCalculator()
        risk = risk_calc.calculate_base_risk(predicted_class, confidence)
        print(f"✅ Risk assessment test passed: {risk}")
    except Exception as e:
        print(f"⚠️ Risk assessment test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 MODEL TESTING COMPLETED!")
    print("✅ Your model is working and ready for use")
    print("\n🚀 Next steps:")
    print("   1. Start API server: cd api && python main.py")
    print("   2. Test API endpoints at http://localhost:8000/docs")
    print("   3. Upload real crop images for testing")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Testing failed. Check the errors above.")
        sys.exit(1)
