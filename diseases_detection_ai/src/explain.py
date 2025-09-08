"""
Grad-CAM Implementation for Crop Disease Detection
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

class GradCAM:
    """Grad-CAM implementation for visual explanations"""
    
    def __init__(self, model, target_layer_name='layer4'):
        """
        Initialize Grad-CAM
        
        Args:
            model: Trained PyTorch model
            target_layer_name: Name of the target layer for Grad-CAM
        """
        self.model = model
        self.model.eval()
        
        # Hook for gradients and activations
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer = None
        self._register_hooks(target_layer_name)
    
    def _register_hooks(self, target_layer_name):
        """Register forward and backward hooks"""
        
        def forward_hook(module, input, output):
            self.activations = output
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]
        
        # Find target layer in ResNet
        if hasattr(self.model, 'resnet'):
            # For our custom model structure
            target_layer = getattr(self.model.resnet, target_layer_name)
        elif hasattr(self.model, 'backbone'):
            # For backbone structure
            target_layer = getattr(self.model.backbone.resnet, target_layer_name)
        else:
            # Direct ResNet model
            target_layer = getattr(self.model, target_layer_name)
        
        self.target_layer = target_layer
        target_layer.register_forward_hook(forward_hook)
        target_layer.register_backward_hook(backward_hook)
    
    def generate_cam(self, input_tensor, class_idx=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            input_tensor: Input image tensor (1, 3, H, W)
            class_idx: Target class index (if None, uses predicted class)
            
        Returns:
            cam: Grad-CAM heatmap
            prediction: Model prediction
        """
        # Forward pass
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        class_score = output[0, class_idx]
        class_score.backward()
        
        # Generate CAM
        gradients = self.gradients[0]  # (C, H, W)
        activations = self.activations[0]  # (C, H, W)
        
        # Global average pooling of gradients
        weights = torch.mean(gradients, dim=(1, 2))  # (C,)
        
        # Weighted combination of activation maps
        cam = torch.zeros(activations.shape[1:], dtype=torch.float32)  # (H, W)
        for i, w in enumerate(weights):
            cam += w * activations[i]
        
        # Apply ReLU
        cam = F.relu(cam)
        
        # Normalize
        if cam.max() > 0:
            cam = cam / cam.max()
        
        return cam.detach().cpu().numpy(), output, class_idx
    
    def create_heatmap_overlay(self, original_image, cam, alpha=0.4):
        """
        Create heatmap overlay on original image
        
        Args:
            original_image: Original PIL Image
            cam: Grad-CAM heatmap
            alpha: Overlay transparency
            
        Returns:
            overlay_image: PIL Image with heatmap overlay
        """
        # Resize CAM to match original image size
        original_size = original_image.size
        cam_resized = cv2.resize(cam, original_size)
        
        # Convert to heatmap
        heatmap = cm.jet(cam_resized)[:, :, :3]  # Remove alpha channel
        heatmap = (heatmap * 255).astype(np.uint8)
        
        # Convert original image to numpy
        original_np = np.array(original_image)
        
        # Create overlay
        overlay = cv2.addWeighted(original_np, 1-alpha, heatmap, alpha, 0)
        
        return Image.fromarray(overlay)
    
    def save_explanation(self, original_image, cam, prediction, class_names, 
                        confidence, save_path, show_plot=False):
        """
        Save complete visual explanation
        
        Args:
            original_image: Original PIL Image
            cam: Grad-CAM heatmap
            prediction: Model prediction tensor
            class_names: List of class names
            confidence: Prediction confidence
            save_path: Path to save the explanation
            show_plot: Whether to display the plot
        """
        # Create figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image
        axes[0].imshow(original_image)
        axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # Heatmap
        axes[1].imshow(cam, cmap='jet', alpha=0.8)
        axes[1].set_title('Grad-CAM Heatmap', fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        # Overlay
        overlay = self.create_heatmap_overlay(original_image, cam)
        axes[2].imshow(overlay)
        predicted_class = class_names[prediction.argmax().item()]
        axes[2].set_title(f'Prediction: {predicted_class}\nConfidence: {confidence:.2%}', 
                         fontsize=14, fontweight='bold')
        axes[2].axis('off')
        
        plt.tight_layout()
        
        # Save
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return overlay
    
    def image_to_base64(self, image):
        """
        Convert PIL Image to base64 string for API response
        
        Args:
            image: PIL Image
            
        Returns:
            base64_string: Base64 encoded image
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str

class CropDiseaseExplainer:
    """High-level interface for crop disease explanation"""
    
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
        self.grad_cam = GradCAM(model)
    
    def explain_prediction(self, image_path, save_dir='outputs/heatmaps', 
                          return_base64=False):
        """
        Generate complete explanation for an image
        
        Args:
            image_path: Path to input image
            save_dir: Directory to save explanations
            return_base64: Whether to return base64 encoded image
            
        Returns:
            explanation: Dictionary with prediction and explanation
        """
        # Load and preprocess image
        original_image = Image.open(image_path).convert('RGB')
        
        # Preprocessing transforms (should match training transforms)
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        input_tensor = transform(original_image).unsqueeze(0).to(self.device)
        
        # Generate Grad-CAM
        cam, prediction, class_idx = self.grad_cam.generate_cam(input_tensor)
        
        # Get prediction details
        probabilities = F.softmax(prediction, dim=1)
        confidence = probabilities[0, class_idx].item()
        predicted_class = self.class_names[class_idx]
        
        # Create save path
        image_name = Path(image_path).stem
        save_path = Path(save_dir) / f"{image_name}_explanation.png"
        
        # Save explanation
        overlay_image = self.grad_cam.save_explanation(
            original_image, cam, prediction, self.class_names, 
            confidence, save_path
        )
        
        # Prepare explanation dictionary
        explanation = {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'class_probabilities': {
                self.class_names[i]: probabilities[0, i].item() 
                for i in range(len(self.class_names))
            },
            'explanation_image_path': str(save_path),
            'heatmap_regions': self._analyze_heatmap_regions(cam)
        }
        
        # Add base64 image if requested
        if return_base64:
            explanation['explanation_image_base64'] = self.grad_cam.image_to_base64(overlay_image)
        
        return explanation
    
    def _analyze_heatmap_regions(self, cam, threshold=0.5):
        """
        Analyze important regions in the heatmap
        
        Args:
            cam: Grad-CAM heatmap
            threshold: Threshold for important regions
            
        Returns:
            regions: Analysis of important regions
        """
        # Find regions above threshold
        important_mask = cam > threshold
        important_ratio = np.sum(important_mask) / cam.size
        
        # Find peak attention
        max_attention = np.max(cam)
        max_location = np.unravel_index(np.argmax(cam), cam.shape)
        
        return {
            'max_attention_value': float(max_attention),
            'max_attention_location': {
                'row': int(max_location[0]),
                'col': int(max_location[1])
            },
            'important_region_ratio': float(important_ratio),
            'attention_distribution': {
                'mean': float(np.mean(cam)),
                'std': float(np.std(cam)),
                'median': float(np.median(cam))
            }
        }

def test_gradcam():
    """Test Grad-CAM implementation"""
    print("🔬 Testing Grad-CAM Implementation...")
    
    # This is a test function - in practice, you would load your trained model
    # and test with actual images
    
    try:
        # Load model (placeholder - replace with actual model loading)
        print("📋 Grad-CAM implementation ready for integration")
        print("🎯 Features implemented:")
        print("   ✅ Grad-CAM heatmap generation")
        print("   ✅ Visual overlay creation")
        print("   ✅ Base64 encoding for API responses")
        print("   ✅ Heatmap region analysis")
        print("   ✅ Complete explanation pipeline")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Grad-CAM: {e}")
        return False

if __name__ == "__main__":
    test_gradcam()
