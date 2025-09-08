"""
Training script for crop disease detection model
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

from dataset import create_data_loaders, get_class_weights
from model import create_model, ModelCheckpoint, get_model_summary

class Trainer:
    """Training class for crop disease detection model"""
    
    def __init__(self, model, train_loader, val_loader, class_names, device='cpu'):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.class_names = class_names
        self.device = device
        
        # Training history
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'lr': []
        }
        
    def train_epoch(self, criterion, optimizer):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        for inputs, labels in self.train_loader:
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)
            
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
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
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
    
    def train(self, num_epochs=25, learning_rate=1e-4, weight_decay=1e-4, 
              use_class_weights=True, checkpoint_path='models/crop_disease_resnet50.pth',
              fine_tune_epoch=10):
        """
        Train the model
        
        Args:
            num_epochs: Number of training epochs
            learning_rate: Initial learning rate
            weight_decay: Weight decay for regularization
            use_class_weights: Use class weights for imbalanced data
            checkpoint_path: Path to save best model
            fine_tune_epoch: Epoch to start fine-tuning (unfreeze all layers)
        """
        
        print("Starting training...")
        print(f"Device: {self.device}")
        print(f"Number of classes: {len(self.class_names)}")
        print(f"Training samples: {len(self.train_loader.dataset)}")
        print(f"Validation samples: {len(self.val_loader.dataset)}")
        
        # Setup loss function
        if use_class_weights:
            class_weights = get_class_weights('data')
            class_weights = class_weights.to(self.device)
            criterion = nn.CrossEntropyLoss(weight=class_weights)
            print("Using weighted CrossEntropyLoss")
        else:
            criterion = nn.CrossEntropyLoss()
            print("Using standard CrossEntropyLoss")
        
        # Setup optimizer
        optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Setup learning rate scheduler
        scheduler = ReduceLROnPlateau(
            optimizer, mode='max', factor=0.5, patience=5
        )
        
        # Setup model checkpoint
        checkpoint = ModelCheckpoint(
            filepath=checkpoint_path,
            monitor='val_accuracy',
            mode='max'
        )
        
        # Training loop
        best_acc = 0.0
        start_time = time.time()
        
        for epoch in range(num_epochs):
            epoch_start = time.time()
            
            # Fine-tuning: unfreeze all layers after specified epoch
            if epoch == fine_tune_epoch:
                print(f"\nEpoch {epoch}: Starting fine-tuning (unfreezing all layers)")
                self.model.unfreeze_features()
                # Reduce learning rate for fine-tuning
                for param_group in optimizer.param_groups:
                    param_group['lr'] = learning_rate * 0.1
                print(f"Reduced learning rate to: {optimizer.param_groups[0]['lr']}")
            
            # Training phase
            train_loss, train_acc = self.train_epoch(criterion, optimizer)
            
            # Validation phase
            val_loss, val_acc = self.validate_epoch(criterion)
            
            # Update learning rate
            scheduler.step(val_acc)
            current_lr = optimizer.param_groups[0]['lr']
            
            # Save history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['lr'].append(current_lr)
            
            # Save checkpoint
            metrics = {
                'val_accuracy': val_acc,
                'val_loss': val_loss,
                'train_accuracy': train_acc,
                'train_loss': train_loss
            }
            checkpoint(self.model, optimizer, epoch, metrics)
            
            # Update best accuracy
            if val_acc > best_acc:
                best_acc = val_acc
            
            # Print progress
            epoch_time = time.time() - epoch_start
            print(f'Epoch {epoch+1:2d}/{num_epochs} | '
                  f'Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | '
                  f'Val Loss: {val_loss:.4f} Acc: {val_acc:.4f} | '
                  f'LR: {current_lr:.2e} | Time: {epoch_time:.1f}s')
        
        # Training completed
        total_time = time.time() - start_time
        print(f'\nTraining completed in {total_time//60:.0f}m {total_time%60:.0f}s')
        print(f'Best validation accuracy: {best_acc:.4f}')
        
        # Save training history
        self.save_training_history()
        
        return self.model, self.history
    
    def save_training_history(self, filepath='outputs/training_history.json'):
        """Save training history to file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)
        
        print(f"Training history saved to: {filepath}")
    
    def plot_training_curves(self, save_path='outputs/training_curves.png'):
        """Plot and save training curves"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        epochs = range(1, len(self.history['train_loss']) + 1)
        
        # Loss curves
        ax1.plot(epochs, self.history['train_loss'], 'b-', label='Training Loss')
        ax1.plot(epochs, self.history['val_loss'], 'r-', label='Validation Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Accuracy curves
        ax2.plot(epochs, self.history['train_acc'], 'b-', label='Training Accuracy')
        ax2.plot(epochs, self.history['val_acc'], 'r-', label='Validation Accuracy')
        ax2.set_title('Training and Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        ax2.grid(True)
        
        # Learning rate
        ax3.plot(epochs, self.history['lr'], 'g-', label='Learning Rate')
        ax3.set_title('Learning Rate Schedule')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Learning Rate')
        ax3.set_yscale('log')
        ax3.legend()
        ax3.grid(True)
        
        # Combined accuracy
        ax4.plot(epochs, self.history['train_acc'], 'b-', label='Training')
        ax4.plot(epochs, self.history['val_acc'], 'r-', label='Validation')
        ax4.set_title('Model Accuracy Comparison')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Accuracy')
        ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Training curves saved to: {save_path}")

def main():
    """Main training function"""
    
    # Configuration
    config = {
        'data_dir': 'data',
        'batch_size': 32,  # Increased for GPU training
        'num_epochs': 20,
        'learning_rate': 1e-4,
        'weight_decay': 1e-4,
        'fine_tune_epoch': 10,
        'checkpoint_path': 'models/crop_disease_resnet50.pth'
    }
    
    # Device setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Create data loaders
    print("Loading dataset...")
    train_loader, val_loader, test_loader, class_names = create_data_loaders(
        data_dir=config['data_dir'],
        batch_size=config['batch_size'],
        num_workers=0 if device.type == 'cpu' else 2  # Use more workers for GPU
    )
    
    print(f"Dataset loaded: {len(class_names)} classes")
    print(f"Classes: {class_names}")
    
    # Create model
    print("Creating model...")
    model = create_model(num_classes=len(class_names), device=device)
    get_model_summary(model)
    
    # Create trainer
    trainer = Trainer(model, train_loader, val_loader, class_names, device)
    
    # Start training
    trained_model, history = trainer.train(
        num_epochs=config['num_epochs'],
        learning_rate=config['learning_rate'],
        weight_decay=config['weight_decay'],
        checkpoint_path=config['checkpoint_path'],
        fine_tune_epoch=config['fine_tune_epoch']
    )
    
    # Plot training curves
    trainer.plot_training_curves()
    
    print("\nTraining completed successfully!")
    print(f"Best model saved at: {config['checkpoint_path']}")

if __name__ == "__main__":
    main()
