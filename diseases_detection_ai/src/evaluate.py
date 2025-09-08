"""
Model evaluation script for crop disease detection
"""

import torch
import torch.nn as nn
import numpy as np
import json
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from .dataset import create_data_loaders
from .model import create_model, load_checkpoint

class ModelEvaluator:
    """Evaluate trained model performance"""
    
    def __init__(self, model, test_loader, class_names, device='cpu'):
        self.model = model
        self.test_loader = test_loader
        self.class_names = class_names
        self.device = device
        
    def evaluate(self):
        """Evaluate model on test dataset"""
        self.model.eval()
        
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(inputs)
                probs = torch.softmax(outputs, dim=1)
                _, preds = torch.max(outputs, 1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        return np.array(all_preds), np.array(all_labels), np.array(all_probs)
    
    def calculate_metrics(self, y_true, y_pred, y_probs):
        """Calculate comprehensive evaluation metrics"""
        
        # Basic metrics
        accuracy = accuracy_score(y_true, y_pred)
        
        # Per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            y_true, y_pred, average=None, labels=range(len(self.class_names))
        )
        
        # Macro and weighted averages
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
            y_true, y_pred, average='macro'
        )
        
        precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
            y_true, y_pred, average='weighted'
        )
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Classification report
        class_report = classification_report(
            y_true, y_pred, 
            target_names=self.class_names,
            output_dict=True
        )
        
        metrics = {
            'accuracy': float(accuracy),
            'precision_macro': float(precision_macro),
            'recall_macro': float(recall_macro),
            'f1_macro': float(f1_macro),
            'precision_weighted': float(precision_weighted),
            'recall_weighted': float(recall_weighted),
            'f1_weighted': float(f1_weighted),
            'per_class_metrics': {
                'precision': precision.tolist(),
                'recall': recall.tolist(),
                'f1_score': f1.tolist(),
                'support': support.tolist()
            },
            'confusion_matrix': cm.tolist(),
            'classification_report': class_report
        }
        
        return metrics
    
    def plot_confusion_matrix(self, cm, save_path='outputs/confusion_matrix.png'):
        """Plot and save confusion matrix"""
        plt.figure(figsize=(12, 10))
        
        # Normalize confusion matrix
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Create heatmap
        sns.heatmap(
            cm_normalized,
            annot=True,
            fmt='.2f',
            cmap='Blues',
            xticklabels=[name.replace('___', '\n') for name in self.class_names],
            yticklabels=[name.replace('___', '\n') for name in self.class_names],
            cbar_kws={'label': 'Normalized Frequency'}
        )
        
        plt.title('Confusion Matrix (Normalized)', fontsize=16, pad=20)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Save plot
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Confusion matrix saved to: {save_path}")
    
    def plot_per_class_metrics(self, metrics, save_path='outputs/per_class_metrics.png'):
        """Plot per-class performance metrics"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        class_names_short = [name.replace('___', '\n') for name in self.class_names]
        x_pos = np.arange(len(self.class_names))
        
        # Precision
        ax1.bar(x_pos, metrics['per_class_metrics']['precision'], color='skyblue', alpha=0.7)
        ax1.set_title('Precision per Class')
        ax1.set_ylabel('Precision')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(class_names_short, rotation=45, ha='right')
        ax1.set_ylim(0, 1)
        ax1.grid(True, alpha=0.3)
        
        # Recall
        ax2.bar(x_pos, metrics['per_class_metrics']['recall'], color='lightcoral', alpha=0.7)
        ax2.set_title('Recall per Class')
        ax2.set_ylabel('Recall')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(class_names_short, rotation=45, ha='right')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3)
        
        # F1-Score
        ax3.bar(x_pos, metrics['per_class_metrics']['f1_score'], color='lightgreen', alpha=0.7)
        ax3.set_title('F1-Score per Class')
        ax3.set_ylabel('F1-Score')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(class_names_short, rotation=45, ha='right')
        ax3.set_ylim(0, 1)
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Per-class metrics plot saved to: {save_path}")
    
    def save_results(self, metrics, save_path='outputs/results.json'):
        """Save evaluation results to JSON file"""
        
        # Add class names to results
        results = {
            'class_names': self.class_names,
            'num_classes': len(self.class_names),
            'test_samples': len(self.test_loader.dataset),
            'metrics': metrics,
            'model_info': {
                'architecture': 'ResNet50',
                'pretrained': True,
                'transfer_learning': True
            }
        }
        
        # Save to file
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {save_path}")
        
        return results
    
    def print_summary(self, metrics):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("MODEL EVALUATION SUMMARY")
        print("="*60)
        print(f"Test Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision (Macro): {metrics['precision_macro']:.4f}")
        print(f"Recall (Macro): {metrics['recall_macro']:.4f}")
        print(f"F1-Score (Macro): {metrics['f1_macro']:.4f}")
        print(f"F1-Score (Weighted): {metrics['f1_weighted']:.4f}")
        print("\nPer-Class Performance:")
        print("-" * 60)
        
        for i, class_name in enumerate(self.class_names):
            precision = metrics['per_class_metrics']['precision'][i]
            recall = metrics['per_class_metrics']['recall'][i]
            f1 = metrics['per_class_metrics']['f1_score'][i]
            support = metrics['per_class_metrics']['support'][i]
            
            print(f"{class_name:40} | P: {precision:.3f} | R: {recall:.3f} | F1: {f1:.3f} | N: {support:2d}")
        
        print("="*60)

def evaluate_model(checkpoint_path, data_dir='data', batch_size=32):
    """Main evaluation function"""
    
    # Device setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load data
    print("Loading test dataset...")
    _, _, test_loader, class_names = create_data_loaders(
        data_dir=data_dir,
        batch_size=batch_size,
        num_workers=0
    )
    
    print(f"Test dataset loaded: {len(test_loader.dataset)} samples")
    
    # Create and load model
    print("Loading trained model...")
    model = create_model(num_classes=len(class_names), device=device)
    
    try:
        model, _, epoch, _ = load_checkpoint(checkpoint_path, model, device=device)
        print(f"Model loaded successfully from epoch {epoch}")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        print("Using untrained model for testing...")
    
    # Create evaluator
    evaluator = ModelEvaluator(model, test_loader, class_names, device)
    
    # Run evaluation
    print("Evaluating model...")
    y_pred, y_true, y_probs = evaluator.evaluate()
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics(y_true, y_pred, y_probs)
    
    # Print summary
    evaluator.print_summary(metrics)
    
    # Generate plots
    evaluator.plot_confusion_matrix(metrics['confusion_matrix'])
    evaluator.plot_per_class_metrics(metrics)
    
    # Save results
    results = evaluator.save_results(metrics)
    
    return results

if __name__ == "__main__":
    # Evaluate the trained model
    results = evaluate_model(
        checkpoint_path='models/crop_disease_resnet50.pth',
        data_dir='data',
        batch_size=16
    )
