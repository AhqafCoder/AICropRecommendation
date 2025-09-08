"""
Dataset loading and preprocessing for crop disease detection
"""

import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path

def get_transforms(split='train', input_size=224):
    """
    Get image transforms for different dataset splits
    
    Args:
        split: 'train', 'val', or 'test'
        input_size: Input image size (default: 224)
    
    Returns:
        transforms.Compose: Composed transforms
    """
    if split == 'train':
        # Training transforms with augmentation
        return transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomVerticalFlip(p=0.3),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        # Validation/test transforms (no augmentation)
        return transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])

def get_inference_transforms(input_size=224):
    """
    Get transforms for inference (prediction)
    
    Args:
        input_size: Input image size (default: 224)
    
    Returns:
        transforms.Compose: Composed transforms for inference
    """
    return transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])

class CropDiseaseDataset(Dataset):
    """Custom dataset for crop disease images"""
    
    def __init__(self, data_dir, transform=None, class_to_idx=None):
        """
        Args:
            data_dir: Path to dataset directory (train/val/test)
            transform: Optional transform to be applied on images
            class_to_idx: Dictionary mapping class names to indices
        """
        self.data_dir = Path(data_dir)
        self.transform = transform
        
        # Get all image files and their labels
        self.samples = []
        self.classes = []
        
        # Scan all class directories
        for class_dir in sorted(self.data_dir.iterdir()):
            if class_dir.is_dir() and not class_dir.name.startswith('.'):
                self.classes.append(class_dir.name)
        
        # Create class to index mapping if not provided
        if class_to_idx is None:
            self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}
        else:
            self.class_to_idx = class_to_idx
        
        # Collect all image samples
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        for class_name in self.classes:
            class_dir = self.data_dir / class_name
            class_idx = self.class_to_idx[class_name]
            
            for img_path in class_dir.iterdir():
                if img_path.suffix.lower() in image_extensions:
                    self.samples.append((str(img_path), class_idx))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        
        # Load image
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            # Create a dummy image if file doesn't exist or is corrupted
            print(f"Warning: Could not load {img_path}, creating dummy image")
            image = Image.new('RGB', (224, 224), color=(128, 128, 128))
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_names(self):
        """Return list of class names"""
        return self.classes
    
    def get_class_to_idx(self):
        """Return class to index mapping"""
        return self.class_to_idx

def get_data_transforms():
    """Get data transforms for training and validation"""
    
    # ImageNet normalization values
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    
    # Training transforms with data augmentation
    train_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        normalize
    ])
    
    # Validation/Test transforms (no augmentation)
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        normalize
    ])
    
    return train_transforms, val_transforms

def create_data_loaders(data_dir, batch_size=32, num_workers=4):
    """Create data loaders for training, validation, and testing"""
    
    train_transforms, val_transforms = get_data_transforms()
    
    # Create datasets
    train_dataset = CropDiseaseDataset(
        data_dir=os.path.join(data_dir, 'train'),
        transform=train_transforms
    )
    
    val_dataset = CropDiseaseDataset(
        data_dir=os.path.join(data_dir, 'val'),
        transform=val_transforms,
        class_to_idx=train_dataset.get_class_to_idx()
    )
    
    test_dataset = CropDiseaseDataset(
        data_dir=os.path.join(data_dir, 'test'),
        transform=val_transforms,
        class_to_idx=train_dataset.get_class_to_idx()
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader, train_dataset.get_class_names()

def get_class_weights(data_dir):
    """Calculate class weights for handling imbalanced datasets"""
    
    train_dataset = CropDiseaseDataset(data_dir=os.path.join(data_dir, 'train'))
    
    # Count samples per class
    class_counts = {}
    for _, label in train_dataset.samples:
        class_name = train_dataset.classes[label]
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    # Calculate weights (inverse frequency)
    total_samples = len(train_dataset.samples)
    num_classes = len(train_dataset.classes)
    
    class_weights = []
    for class_name in train_dataset.classes:
        count = class_counts.get(class_name, 1)
        weight = total_samples / (num_classes * count)
        class_weights.append(weight)
    
    return torch.FloatTensor(class_weights)

if __name__ == "__main__":
    # Test the dataset loading
    data_dir = "data"
    
    try:
        train_loader, val_loader, test_loader, class_names = create_data_loaders(data_dir, batch_size=4)
        
        print(f"Dataset loaded successfully!")
        print(f"Number of classes: {len(class_names)}")
        print(f"Classes: {class_names}")
        print(f"Train batches: {len(train_loader)}")
        print(f"Val batches: {len(val_loader)}")
        print(f"Test batches: {len(test_loader)}")
        
        # Test loading a batch
        for images, labels in train_loader:
            print(f"Batch shape: {images.shape}")
            print(f"Label shape: {labels.shape}")
            break
            
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Make sure the dataset is properly organized in data/train, data/val, data/test")
