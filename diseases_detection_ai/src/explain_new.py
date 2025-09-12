"""
Grad-CAM Implementation for Crop Disease Detection using pytorch-grad-cam
Generates visual explanations showing which parts of the leaf image the model focuses on
"""

import torch
import torch.nn.functional as F
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path
import base64
import io
import os

try:
    from pytorch_grad_cam import GradCAM
    from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
    from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image
    PYTORCH_GRAD_CAM_AVAILABLE = True
except ImportError:
    print("Warning: pytorch-grad-cam not available. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "grad-cam"])
    try:
        from pytorch_grad_cam import GradCAM
        from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
        from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image
        PYTORCH_GRAD_CAM_AVAILABLE = True
    except ImportError:
        PYTORCH_GRAD_CAM_AVAILABLE = False
        print("Warning: Could not import pytorch-grad-cam after installation")

class CropDiseaseExplainer:
    """High-level interface for crop disease explanation using pytorch-grad-cam"""
    
    def __init__(self, model, class_names, device='cpu'):
        """
        Initialize explainer
        
        Args:
            model: Trained model
            class_names: List of class names
            device: Device to run on
        """
        self.model = model.to(device)
        self.class_names = class_names
        self.device = device
        
        # Define target layer for Grad-CAM (last convolutional layer)
        if hasattr(model, 'resnet'):
            # For our CropDiseaseResNet50 model
            self.target_layers = [model.resnet.layer4[-1]]
        else:
            # Fallback for standard ResNet
            self.target_layers = [model.layer4[-1]]
        
        # Initialize Grad-CAM
        if PYTORCH_GRAD_CAM_AVAILABLE:
            self.grad_cam = GradCAM(model=self.model, target_layers=self.target_layers)
        else:
            self.grad_cam = None
            print("Warning: pytorch-grad-cam not available, Grad-CAM disabled")
    
    def explain_prediction(self, image_path, save_dir='outputs/heatmaps', 
                          return_base64=False, target_class=None):
        """
        Generate complete explanation for an image
        
        Args:
            image_path: Path to input image
            save_dir: Directory to save explanations
            return_base64: Whether to return base64 encoded image
            target_class: Specific class to target (if None, uses predicted class)
            
        Returns:
            explanation: Dictionary with prediction and explanation
        """
        if not PYTORCH_GRAD_CAM_AVAILABLE or self.grad_cam is None:
            return {'error': 'Grad-CAM not available'}
        
        # Load and preprocess image
        original_image = Image.open(image_path).convert('RGB')
        original_np = np.array(original_image) / 255.0  # Normalize to [0,1]
        
        # Preprocessing transforms (should match training transforms)
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        input_tensor = transform(original_image).unsqueeze(0).to(self.device)
        
        # Get prediction
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_idx = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_idx].item()
        
        # Use target class if specified, otherwise use predicted class
        target_idx = target_class if target_class is not None else predicted_idx
        targets = [ClassifierOutputTarget(target_idx)]
        
        # Generate Grad-CAM
        try:
            # Resize original image for overlay
            original_resized = cv2.resize(np.array(original_image), (224, 224))
            original_resized = original_resized / 255.0
            
            # Generate CAM
            grayscale_cam = self.grad_cam(input_tensor=input_tensor, targets=targets)
            grayscale_cam = grayscale_cam[0, :]  # Take first (and only) image
            
            # Create visualization
            cam_image = show_cam_on_image(original_resized, grayscale_cam, use_rgb=True)
            
            # Convert back to PIL Image
            cam_pil = Image.fromarray((cam_image * 255).astype(np.uint8))
            
            # Create save directory
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            
            # Save visualization
            filename = Path(image_path).stem
            save_path = Path(save_dir) / f"{filename}_gradcam.jpg"
            cam_pil.save(save_path)
            
            # Prepare return data
            result = {
                'predicted_class': self.class_names[predicted_idx],
                'predicted_idx': predicted_idx,
                'confidence': confidence,
                'target_class': self.class_names[target_idx],
                'target_idx': target_idx,
                'save_path': str(save_path),
                'cam_image': cam_pil
            }
            
            # Add base64 encoding if requested
            if return_base64:
                buffer = io.BytesIO()
                cam_pil.save(buffer, format='JPEG')
                buffer.seek(0)
                base64_str = base64.b64encode(buffer.getvalue()).decode()
                result['overlay_base64'] = base64_str
            
            return result
            
        except Exception as e:
            print(f"Error generating Grad-CAM: {e}")
            return {'error': str(e)}

def load_model_and_generate_gradcam(model_path, image_path, output_path=None, target_class=None):
    """
    Complete example function that loads a model and generates Grad-CAM visualization
    
    Args:
        model_path: Path to the saved model file
        image_path: Path to input image
        output_path: Path to save the output (optional)
        target_class: Target class index (optional, uses prediction if None)
    
    Returns:
        Dictionary with results
    """
    # Import model
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from model import CropDiseaseResNet50
    
    # Define class names
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
    
    # Step 1: Load the trained model
    print(f"Loading model from {model_path}...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=False)
    checkpoint = torch.load(model_path, map_location=device)
    
    # Handle checkpoint format
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
        if 'class_names' in checkpoint:
            class_names = checkpoint['class_names']
    else:
        state_dict = checkpoint
    
    model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()
    print(f"✅ Model loaded successfully!")
    
    # Step 2: Initialize Grad-CAM explainer
    print("Initializing Grad-CAM explainer...")
    explainer = CropDiseaseExplainer(model, class_names, device)
    
    # Step 3: Generate Grad-CAM visualization
    print(f"Generating Grad-CAM for {image_path}...")
    result = explainer.explain_prediction(
        image_path=image_path,
        save_dir='outputs/heatmaps',
        return_base64=True,
        target_class=target_class
    )
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return result
    
    # Step 4: Save output if path specified
    if output_path:
        result['cam_image'].save(output_path)
        print(f"✅ Saved Grad-CAM visualization to {output_path}")
    
    # Print results
    print(f"✅ Grad-CAM generated successfully!")
    print(f"   Predicted: {result['predicted_class']} ({result['confidence']:.1%})")
    print(f"   Target: {result['target_class']}")
    print(f"   Saved to: {result['save_path']}")
    
    return result

# Example usage
if __name__ == "__main__":
    # Example usage
    model_path = "../models/crop_disease_v3_model.pth"
    image_path = "../test_leaf_sample.jpg"
    output_path = "../outputs/gradcam_example.jpg"
    
    if os.path.exists(model_path) and os.path.exists(image_path):
        result = load_model_and_generate_gradcam(
            model_path=model_path,
            image_path=image_path,
            output_path=output_path
        )
    else:
        print("Model or image file not found!")
        print(f"Model path: {model_path}")
        print(f"Image path: {image_path}")
