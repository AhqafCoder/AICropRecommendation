"""
Dataset preprocessing script for crop disease detection
Organizes raw dataset into train/val/test splits
"""

import os
import shutil
import random
from pathlib import Path
from collections import defaultdict
import json

class DatasetPreprocessor:
    """Preprocesses raw crop disease dataset into train/val/test splits"""
    
    def __init__(self, raw_data_path, output_path, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """
        Args:
            raw_data_path: Path to raw dataset
            output_path: Path where processed dataset will be saved
            train_ratio: Proportion of data for training
            val_ratio: Proportion of data for validation  
            test_ratio: Proportion of data for testing
        """
        self.raw_data_path = Path(raw_data_path)
        self.output_path = Path(output_path)
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        
        # Ensure ratios sum to 1
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.001, "Ratios must sum to 1"
        
        # Create output directories
        self.train_dir = self.output_path / "train"
        self.val_dir = self.output_path / "val"
        self.test_dir = self.output_path / "test"
        
    def get_class_directories(self):
        """Get all class directories from raw data"""
        class_dirs = []
        for item in self.raw_data_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                class_dirs.append(item)
        return sorted(class_dirs)
    
    def count_images_per_class(self):
        """Count number of images per class"""
        class_counts = {}
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        for class_dir in self.get_class_directories():
            count = 0
            for img_file in class_dir.iterdir():
                if img_file.suffix.lower() in image_extensions:
                    count += 1
            class_counts[class_dir.name] = count
            
        return class_counts
    
    def create_output_structure(self):
        """Create output directory structure"""
        # Remove existing output if it exists
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        
        # Create base directories
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.train_dir.mkdir(exist_ok=True)
        self.val_dir.mkdir(exist_ok=True)
        self.test_dir.mkdir(exist_ok=True)
        
        # Create class subdirectories
        for class_dir in self.get_class_directories():
            class_name = class_dir.name
            (self.train_dir / class_name).mkdir(exist_ok=True)
            (self.val_dir / class_name).mkdir(exist_ok=True)
            (self.test_dir / class_name).mkdir(exist_ok=True)
    
    def split_and_copy_data(self):
        """Split data into train/val/test and copy files"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        split_stats = defaultdict(lambda: defaultdict(int))
        
        for class_dir in self.get_class_directories():
            class_name = class_dir.name
            print(f"Processing class: {class_name}")
            
            # Get all image files
            image_files = []
            for img_file in class_dir.iterdir():
                if img_file.suffix.lower() in image_extensions:
                    image_files.append(img_file)
            
            # Shuffle files for random split
            random.shuffle(image_files)
            
            # Calculate split indices
            total_images = len(image_files)
            train_end = int(total_images * self.train_ratio)
            val_end = train_end + int(total_images * self.val_ratio)
            
            # Split files
            train_files = image_files[:train_end]
            val_files = image_files[train_end:val_end]
            test_files = image_files[val_end:]
            
            # Copy files to respective directories
            for files, target_dir, split_name in [
                (train_files, self.train_dir, 'train'),
                (val_files, self.val_dir, 'val'),
                (test_files, self.test_dir, 'test')
            ]:
                target_class_dir = target_dir / class_name
                for img_file in files:
                    shutil.copy2(img_file, target_class_dir / img_file.name)
                
                split_stats[split_name][class_name] = len(files)
                print(f"  {split_name}: {len(files)} images")
        
        return split_stats
    
    def generate_dataset_info(self, split_stats):
        """Generate dataset information JSON"""
        # Get class names
        class_names = sorted([d.name for d in self.get_class_directories()])
        
        # Create class to index mapping
        class_to_idx = {cls_name: idx for idx, cls_name in enumerate(class_names)}
        
        # Calculate totals
        total_stats = {}
        for split in ['train', 'val', 'test']:
            total_stats[split] = sum(split_stats[split].values())
        
        dataset_info = {
            'dataset_name': 'Crop Disease Detection - Retrained',
            'num_classes': len(class_names),
            'class_names': class_names,
            'class_to_idx': class_to_idx,
            'split_ratios': {
                'train': self.train_ratio,
                'val': self.val_ratio,
                'test': self.test_ratio
            },
            'split_stats': dict(split_stats),
            'total_images': {
                'train': total_stats['train'],
                'val': total_stats['val'],
                'test': total_stats['test'],
                'total': sum(total_stats.values())
            }
        }
        
        # Save dataset info
        info_file = self.output_path / 'dataset_info.json'
        with open(info_file, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        return dataset_info
    
    def preprocess(self, seed=42):
        """Main preprocessing function"""
        print("Starting dataset preprocessing...")
        print(f"Raw data path: {self.raw_data_path}")
        print(f"Output path: {self.output_path}")
        print(f"Split ratios - Train: {self.train_ratio}, Val: {self.val_ratio}, Test: {self.test_ratio}")
        
        # Set random seed for reproducibility
        random.seed(seed)
        
        # Count images per class
        class_counts = self.count_images_per_class()
        print("\nImages per class in raw dataset:")
        for class_name, count in class_counts.items():
            print(f"  {class_name}: {count}")
        
        total_images = sum(class_counts.values())
        print(f"\nTotal images: {total_images}")
        
        # Create output structure
        print("\nCreating output directory structure...")
        self.create_output_structure()
        
        # Split and copy data
        print("\nSplitting and copying data...")
        split_stats = self.split_and_copy_data()
        
        # Generate dataset info
        print("\nGenerating dataset information...")
        dataset_info = self.generate_dataset_info(split_stats)
        
        print("\nDataset preprocessing completed!")
        print(f"Train images: {dataset_info['total_images']['train']}")
        print(f"Val images: {dataset_info['total_images']['val']}")
        print(f"Test images: {dataset_info['total_images']['test']}")
        print(f"Total processed: {dataset_info['total_images']['total']}")
        
        return dataset_info

def main():
    """Main function to run preprocessing"""
    # Set paths
    raw_data_path = "data/raw"
    output_path = "data/processed"
    
    # Create preprocessor
    preprocessor = DatasetPreprocessor(
        raw_data_path=raw_data_path,
        output_path=output_path,
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15
    )
    
    # Run preprocessing
    dataset_info = preprocessor.preprocess()
    
    print(f"\nDataset info saved to: {output_path}/dataset_info.json")
    print(f"Classes found: {dataset_info['num_classes']}")
    print("Class names:")
    for i, class_name in enumerate(dataset_info['class_names']):
        print(f"  {i}: {class_name}")

if __name__ == "__main__":
    main()
