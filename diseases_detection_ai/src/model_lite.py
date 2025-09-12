"""
Memory-optimized ResNet50 model architecture for crop disease detection
Designed to use minimal RAM while maintaining accuracy
"""

import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet50_Weights

class CropDiseaseResNet50Lite(nn.Module):
    """Memory-optimized ResNet50 model for crop disease classification"""
    
    def __init__(self, num_classes, pretrained=True, freeze_features=True):
        """
        Args:
            num_classes: Number of disease classes
            pretrained: Use ImageNet pretrained weights
            freeze_features: Freeze feature extraction layers
        """
        super(CropDiseaseResNet50Lite, self).__init__()
        
        # Load pretrained ResNet50 with memory optimization
        if pretrained:
            self.resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)  # Use V1 for smaller size
        else:
            self.resnet = models.resnet50(weights=None)
        
        # Freeze feature extraction layers to save memory
        if freeze_features:
            for param in self.resnet.parameters():
                param.requires_grad = False
        
        # Replace with smaller, more memory-efficient classifier
        num_features = self.resnet.fc.in_features
        
        # Simplified architecture to reduce memory usage
        self.resnet.fc = nn.Sequential(
            nn.Dropout(0.3),                    # Reduced dropout layers
            nn.Linear(num_features, 256),       # Smaller hidden layer (was 1024)
            nn.ReLU(inplace=True),              # In-place to save memory
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)         # Direct to output
        )
        
        # Store number of classes
        self.num_classes = num_classes
        self.memory_efficient = False
        
    def set_memory_efficient(self, enabled=True):
        """Enable/disable memory efficient mode"""
        self.memory_efficient = enabled
        
        if enabled:
            # Enable gradient checkpointing for memory efficiency
            if hasattr(self.resnet, 'layer1'):
                self._enable_checkpointing()
    
    def _enable_checkpointing(self):
        """Enable gradient checkpointing for memory efficiency"""
        try:
            from torch.utils.checkpoint import checkpoint
            
            def checkpoint_wrapper(module):
                def wrapper(*inputs):
                    return checkpoint(module, *inputs, use_reentrant=False)
                return wrapper
            
            # Apply checkpointing to memory-intensive layers
            if hasattr(self.resnet, 'layer3'):
                self.resnet.layer3 = checkpoint_wrapper(self.resnet.layer3)
            if hasattr(self.resnet, 'layer4'):
                self.resnet.layer4 = checkpoint_wrapper(self.resnet.layer4)
                
        except ImportError:
            print("Gradient checkpointing not available")
    
    def forward(self, x):
        """Forward pass with memory optimization"""
        if self.memory_efficient:
            # Use gradient checkpointing during training
            return torch.utils.checkpoint.checkpoint(self.resnet, x, use_reentrant=False)
        else:
            return self.resnet(x)
    
    def get_feature_extractor(self):
        """Get feature extractor for transfer learning"""
        return nn.Sequential(*list(self.resnet.children())[:-1])
    
    def get_classifier(self):
        """Get classifier layers"""
        return self.resnet.fc
    
    def freeze_features(self):
        """Freeze feature extraction layers"""
        for param in list(self.resnet.children())[:-1]:
            if hasattr(param, 'parameters'):
                for p in param.parameters():
                    p.requires_grad = False
    
    def unfreeze_features(self):
        """Unfreeze feature extraction layers"""
        for param in self.resnet.parameters():
            param.requires_grad = True
    
    def get_model_size(self):
        """Get model size in MB"""
        param_size = 0
        buffer_size = 0
        
        for param in self.parameters():
            param_size += param.nelement() * param.element_size()
        
        for buffer in self.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_mb = (param_size + buffer_size) / 1024 / 1024
        return size_mb
    
    def print_model_info(self):
        """Print model information"""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        size_mb = self.get_model_size()
        
        print(f"Model: CropDiseaseResNet50Lite")
        print(f"Total parameters: {total_params:,}")
        print(f"Trainable parameters: {trainable_params:,}")
        print(f"Model size: {size_mb:.2f} MB")
        print(f"Memory efficient mode: {self.memory_efficient}")

class TinyDiseaseClassifier(nn.Module):
    """Ultra-lightweight model for extremely memory-constrained environments"""
    
    def __init__(self, num_classes, input_size=224):
        super(TinyDiseaseClassifier, self).__init__()
        
        # Extremely simple CNN architecture
        self.features = nn.Sequential(
            # First block
            nn.Conv2d(3, 16, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            
            # Second block
            nn.Conv2d(16, 32, kernel_size=5, stride=2, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            
            # Third block
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )
        
        self.num_classes = num_classes
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
    
    def get_model_size(self):
        """Get model size in MB"""
        param_size = 0
        for param in self.parameters():
            param_size += param.nelement() * param.element_size()
        return param_size / 1024 / 1024

def create_memory_optimized_model(num_classes, model_type='lite', pretrained=True):
    """
    Create memory-optimized model based on available resources
    
    Args:
        num_classes: Number of classes
        model_type: 'lite' or 'tiny'
        pretrained: Use pretrained weights
    
    Returns:
        Optimized model
    """
    if model_type == 'tiny':
        model = TinyDiseaseClassifier(num_classes)
        print(f"Created TinyDiseaseClassifier: {model.get_model_size():.2f} MB")
    else:
        model = CropDiseaseResNet50Lite(num_classes, pretrained=pretrained)
        print(f"Created CropDiseaseResNet50Lite: {model.get_model_size():.2f} MB")
    
    return model

# Test function to check memory usage
def test_memory_usage():
    """Test memory usage of different model configurations"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    print("Testing memory usage of different models:")
    print(f"Initial memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    
    # Test lite model
    model_lite = CropDiseaseResNet50Lite(15, pretrained=False)
    print(f"After lite model: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    model_lite.print_model_info()
    
    del model_lite
    torch.cuda.empty_cache() if torch.cuda.is_available() else None
    
    # Test tiny model
    model_tiny = TinyDiseaseClassifier(15)
    print(f"After tiny model: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"Tiny model size: {model_tiny.get_model_size():.2f} MB")
    
    del model_tiny

if __name__ == "__main__":
    test_memory_usage()