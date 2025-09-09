"""
Retrain the crop disease detection model with the new dataset
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau, StepLR
import time
import copy
import json
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import seaborn as sns
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append('src')

from dataset import create_data_loaders, get_class_weights
from model import create_model, ModelCheckpoint, get_model_summary

class ModelTrainer:
    """Enhanced training class for crop disease detection model"""
    
    def __init__(self, model, train_loader, val_loader, class_names, device='cpu', model_save_path='models'):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.class_names = class_names
        self.device = device
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(exist_ok=True)
        
        # Training history
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'lr': []
        }
        
        # Best model tracking
        self.best_val_acc = 0.0
        self.best_model_weights = None
        
    def train_epoch(self, criterion, optimizer):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        for inputs, labels in self.train_loader:
            inputs = inputs.to(self.device, non_blocking=True)
            labels = labels.to(self.device, non_blocking=True)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_samples += inputs.size(0)
            
            # Clear cache periodically for GPU memory management
            if self.device.type == 'cuda' and total_samples % 500 == 0:
                torch.cuda.empty_cache()
        
        epoch_loss = running_loss / total_samples
        epoch_acc = running_corrects.double() / total_samples
        
        return epoch_loss, epoch_acc.item()
    
    def validate_epoch(self, criterion):
        """Validate for one epoch"""
        self.model.eval()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs = inputs.to(self.device, non_blocking=True)
                labels = labels.to(self.device, non_blocking=True)
                
                # Forward pass
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                # Statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                total_samples += inputs.size(0)
        
        epoch_loss = running_loss / total_samples
        epoch_acc = running_corrects.double() / total_samples
        
        return epoch_loss, epoch_acc.item()
    
    def train(self, num_epochs=50, learning_rate=0.001, weight_decay=1e-4, use_class_weights=True):
        """Main training loop"""
        print(f"Starting training on {self.device}")
        print(f"Training samples: {len(self.train_loader.dataset)}")
        print(f"Validation samples: {len(self.val_loader.dataset)}")
        print(f"Number of classes: {len(self.class_names)}")
        print(f"Epochs: {num_epochs}")
        print(f"Learning rate: {learning_rate}")
        print(f"Weight decay: {weight_decay}")
        print("-" * 60)
        
        # Setup criterion with class weights if specified
        if use_class_weights:
            try:
                class_weights = get_class_weights('data/processed')
                class_weights = class_weights.to(self.device)
                criterion = nn.CrossEntropyLoss(weight=class_weights)
                print("Using weighted CrossEntropyLoss")
            except Exception as e:
                print(f"Could not compute class weights: {e}")
                criterion = nn.CrossEntropyLoss()
        else:
            criterion = nn.CrossEntropyLoss()
        
        # Setup optimizer and scheduler
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=7)
        
        # Training loop
        start_time = time.time()
        
        for epoch in range(num_epochs):
            epoch_start_time = time.time()
            
            # Train
            train_loss, train_acc = self.train_epoch(criterion, optimizer)
            
            # Validate
            val_loss, val_acc = self.validate_epoch(criterion)
            
            # Step scheduler
            scheduler.step(val_acc)
            
            # Save history
            current_lr = optimizer.param_groups[0]['lr']
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['lr'].append(current_lr)
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.best_model_weights = copy.deepcopy(self.model.state_dict())
            
            # Print progress
            epoch_time = time.time() - epoch_start_time
            print(f'Epoch {epoch+1:2d}/{num_epochs} | '
                  f'Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | '
                  f'Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | '
                  f'LR: {current_lr:.6f} | Time: {epoch_time:.1f}s')
            
            # Print GPU memory usage if available
            if self.device.type == 'cuda':
                allocated = torch.cuda.memory_allocated(0) / 1024**3
                cached = torch.cuda.memory_reserved(0) / 1024**3
                print(f'GPU Memory - Allocated: {allocated:.1f}GB | Cached: {cached:.1f}GB')
            
            # Early stopping check
            if current_lr < 1e-6:
                print("Learning rate too small, stopping training")
                break
        
        total_time = time.time() - start_time
        print(f"\nTraining completed in {total_time:.1f}s")
        print(f"Best validation accuracy: {self.best_val_acc:.4f}")
        
        # Load best model weights
        self.model.load_state_dict(self.best_model_weights)
        
        return self.history
    
    def save_model(self, filename=None):
        """Save the trained model"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crop_disease_retrained_{timestamp}.pth"
        
        model_path = self.model_save_path / filename
        
        # Save model state dict along with metadata
        save_dict = {
            'model_state_dict': self.best_model_weights,
            'num_classes': len(self.class_names),
            'class_names': self.class_names,
            'best_val_acc': self.best_val_acc,
            'training_history': self.history,
            'model_architecture': 'ResNet50',
            'timestamp': datetime.now().isoformat()
        }
        
        torch.save(save_dict, model_path)
        print(f"Model saved to: {model_path}")
        
        return model_path
    
    def plot_training_curves(self, save_path='outputs'):
        """Plot and save training curves"""
        save_path = Path(save_path)
        save_path.mkdir(exist_ok=True)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs = range(1, len(self.history['train_loss']) + 1)
        
        # Loss curves
        ax1.plot(epochs, self.history['train_loss'], 'b-', label='Training Loss')
        ax1.plot(epochs, self.history['val_loss'], 'r-', label='Validation Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.set_xlabel('Epochs')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Accuracy curves
        ax2.plot(epochs, self.history['train_acc'], 'b-', label='Training Accuracy')
        ax2.plot(epochs, self.history['val_acc'], 'r-', label='Validation Accuracy')
        ax2.set_title('Training and Validation Accuracy')
        ax2.set_xlabel('Epochs')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        ax2.grid(True)
        
        # Learning rate
        ax3.plot(epochs, self.history['lr'], 'g-', label='Learning Rate')
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epochs')
        ax3.set_ylabel('Learning Rate')
        ax3.set_yscale('log')
        ax3.legend()
        ax3.grid(True)
        
        # Validation accuracy zoom
        ax4.plot(epochs, self.history['val_acc'], 'r-', label='Validation Accuracy')
        ax4.axhline(y=self.best_val_acc, color='g', linestyle='--', label=f'Best Val Acc: {self.best_val_acc:.4f}')
        ax4.set_title('Validation Accuracy (Best Model)')
        ax4.set_xlabel('Epochs')
        ax4.set_ylabel('Accuracy')
        ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = save_path / 'retrained_model_curves.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Training curves saved to: {plot_path}")
        
        return plot_path

def evaluate_model(model, test_loader, class_names, device):
    """Evaluate model on test set"""
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Calculate accuracy
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    
    # Generate classification report
    report = classification_report(all_labels, all_preds, target_names=class_names, output_dict=True)
    
    # Generate confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    return accuracy, report, cm, all_preds, all_labels

def plot_confusion_matrix(cm, class_names, save_path='outputs'):
    """Plot and save confusion matrix"""
    save_path = Path(save_path)
    save_path.mkdir(exist_ok=True)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - Retrained Model')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Save plot
    plot_path = save_path / 'confusion_matrix_retrained.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Confusion matrix saved to: {plot_path}")
    return plot_path

def main():
    """Main training function"""
    print("=" * 80)
    print("CROP DISEASE DETECTION - MODEL RETRAINING")
    print("=" * 80)
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        # Clear GPU cache
        torch.cuda.empty_cache()
    
    # Load dataset info
    dataset_info_path = 'data/processed/dataset_info.json'
    with open(dataset_info_path, 'r') as f:
        dataset_info = json.load(f)
    
    num_classes = dataset_info['num_classes']
    class_names = dataset_info['class_names']
    
    print(f"Number of classes: {num_classes}")
    print(f"Classes: {class_names}")
    
    # Create data loaders with GPU-optimized settings
    print("\nCreating data loaders...")
    batch_size = 16 if torch.cuda.is_available() else 8  # Smaller batch for RTX 3050
    num_workers = 4 if torch.cuda.is_available() else 2
    
    train_loader, val_loader, test_loader, loaded_class_names = create_data_loaders(
        data_dir='data/processed',
        batch_size=batch_size,
        num_workers=num_workers
    )
    
    # Use the class names from dataset_info.json to maintain consistency
    # but verify they match the loaded ones
    if loaded_class_names != class_names:
        print("Warning: Class names from dataset don't match expected order")
        print(f"Expected: {class_names}")
        print(f"Loaded: {loaded_class_names}")
        # Use the loaded class names to ensure consistency
        class_names = loaded_class_names
    
    print(f"Train batches: {len(train_loader)}")
    print(f"Val batches: {len(val_loader)}")
    print(f"Test batches: {len(test_loader)}")
    
    # Create model
    print("\nCreating model...")
    model = create_model(num_classes=num_classes, pretrained=True, device=device)
    get_model_summary(model)
    
    # Create trainer
    trainer = ModelTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        class_names=class_names,
        device=device
    )
    
    # Train model
    print("\nStarting training...")
    history = trainer.train(
        num_epochs=50,
        learning_rate=0.001,
        weight_decay=1e-4,
        use_class_weights=True
    )
    
    # Save model
    print("\nSaving model...")
    model_path = trainer.save_model('crop_disease_retrained_final.pth')
    
    # Plot training curves
    print("\nGenerating training curves...")
    trainer.plot_training_curves()
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_accuracy, test_report, test_cm, test_preds, test_labels = evaluate_model(
        model, test_loader, class_names, device
    )
    
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    
    # Plot confusion matrix
    plot_confusion_matrix(test_cm, class_names)
    
    # Save detailed results
    results = {
        'model_path': str(model_path),
        'test_accuracy': test_accuracy,
        'classification_report': test_report,
        'training_history': history,
        'dataset_info': dataset_info,
        'best_val_accuracy': trainer.best_val_acc,
        'total_parameters': sum(p.numel() for p in model.parameters()),
        'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad),
        'timestamp': datetime.now().isoformat()
    }
    
    # Save results
    results_path = Path('outputs') / 'retrained_model_results.json'
    results_path.parent.mkdir(exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("TRAINING SUMMARY")
    print("=" * 80)
    print(f"Dataset: {dataset_info['total_images']['total']} images, {num_classes} classes")
    print(f"Training images: {dataset_info['total_images']['train']}")
    print(f"Validation images: {dataset_info['total_images']['val']}")
    print(f"Test images: {dataset_info['total_images']['test']}")
    print(f"Best validation accuracy: {trainer.best_val_acc:.4f}")
    print(f"Final test accuracy: {test_accuracy:.4f}")
    print(f"Model saved to: {model_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
