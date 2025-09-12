"""
ResNet50 model architecture for crop disease detection
"""

import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet50_Weights

# Import the lite version
from .model_lite import CropDiseaseResNet50Lite, TinyDiseaseClassifier, create_memory_optimized_model

class CropDiseaseResNet50(nn.Module):
    """ResNet50 model for crop disease classification"""
    
    def __init__(self, num_classes, pretrained=True, freeze_features=True):
        """
        Args:
            num_classes: Number of disease classes
            pretrained: Use ImageNet pretrained weights
            freeze_features: Freeze feature extraction layers initially
        """
        super(CropDiseaseResNet50, self).__init__()
        
        # Load pretrained ResNet50
        if pretrained:
            self.resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        else:
            self.resnet = models.resnet50(weights=None)
        
        # Freeze feature extraction layers if specified
        if freeze_features:
            for param in self.resnet.parameters():
                param.requires_grad = False
        
        # Replace the final fully connected layer to match saved v2 model architecture
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Sequential(
            nn.Dropout(0.5),                    # 0
            nn.Linear(num_features, 1024),      # 1
            nn.BatchNorm1d(1024),               # 2
            nn.ReLU(inplace=True),              # 3
            nn.Dropout(0.3),                    # 4
            nn.Linear(1024, 512),               # 5
            nn.BatchNorm1d(512),                # 6
            nn.ReLU(inplace=True),              # 7
            nn.Dropout(0.2),                    # 8
            nn.Linear(512, num_classes)         # 9
        )
        
        # Store number of classes
        self.num_classes = num_classes
        
    def forward(self, x):
        """Forward pass"""
        return self.resnet(x)
    
    def unfreeze_features(self):
        """Unfreeze all layers for fine-tuning"""
        for param in self.resnet.parameters():
            param.requires_grad = True
    
    def freeze_features(self):
        """Freeze feature extraction layers"""
        for name, param in self.resnet.named_parameters():
            if 'fc' not in name:  # Don't freeze the classifier
                param.requires_grad = False
    
    def get_feature_extractor(self):
        """Get feature extractor (without final FC layer) for Grad-CAM"""
        return nn.Sequential(*list(self.resnet.children())[:-1])
    
    def get_classifier(self):
        """Get classifier layer for Grad-CAM"""
        return self.resnet.fc

def create_model(num_classes, pretrained=True, device='cpu'):
    """Create and initialize the model"""
    
    model = CropDiseaseResNet50(
        num_classes=num_classes,
        pretrained=pretrained,
        freeze_features=True
    )
    
    # Move to device
    model = model.to(device)
    
    return model

def get_model_summary(model, input_size=(3, 224, 224)):
    """Print model summary"""
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print("=" * 60)
    print("MODEL SUMMARY")
    print("=" * 60)
    print(f"Model: ResNet50 for Crop Disease Detection")
    print(f"Input size: {input_size}")
    print(f"Number of classes: {model.num_classes}")
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Non-trainable parameters: {total_params - trainable_params:,}")
    print("=" * 60)
    
    return {
        'total_params': total_params,
        'trainable_params': trainable_params,
        'non_trainable_params': total_params - trainable_params
    }

class ModelCheckpoint:
    """Save best model checkpoints during training"""
    
    def __init__(self, filepath, monitor='val_accuracy', mode='max', save_best_only=True):
        self.filepath = filepath
        self.monitor = monitor
        self.mode = mode
        self.save_best_only = save_best_only
        self.best_score = float('-inf') if mode == 'max' else float('inf')
        
    def __call__(self, model, optimizer, epoch, metrics):
        """Save checkpoint if current score is better"""
        
        current_score = metrics.get(self.monitor, 0)
        
        is_better = False
        if self.mode == 'max':
            is_better = current_score > self.best_score
        else:
            is_better = current_score < self.best_score
        
        if not self.save_best_only or is_better:
            if is_better:
                self.best_score = current_score
                
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'metrics': metrics,
                'best_score': self.best_score
            }
            
            torch.save(checkpoint, self.filepath)
            
            if is_better:
                print(f"Saved new best model with {self.monitor}: {current_score:.4f}")
            
            return True
        
        return False

def load_checkpoint(filepath, model, optimizer=None, device='cpu'):
    """Load model checkpoint"""
    
    checkpoint = torch.load(filepath, map_location=device)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    
    epoch = checkpoint.get('epoch', 0)
    metrics = checkpoint.get('metrics', {})
    best_score = checkpoint.get('best_score', 0)
    
    print(f"Loaded checkpoint from epoch {epoch}")
    print(f"Best score: {best_score:.4f}")
    
    return model, optimizer, epoch, metrics

if __name__ == "__main__":
    # Test model creation
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create model for 17 classes (as per our dataset)
    model = create_model(num_classes=17, device=device)
    
    # Print model summary
    get_model_summary(model)
    
    # Test forward pass
    dummy_input = torch.randn(1, 3, 224, 224).to(device)
    output = model(dummy_input)
    print(f"\nTest forward pass:")
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output probabilities sum: {torch.softmax(output, dim=1).sum():.4f}")
