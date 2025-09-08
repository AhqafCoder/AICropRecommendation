"""
Cleanup script to remove unnecessary files from the project
"""

import os
import sys

def cleanup_project():
    """Remove unnecessary files from the project"""
    
    # Files to delete
    files_to_delete = [
        # Empty files
        'download_dataset.py',
        'fix_dataset.py', 
        'install_dependencies.py',
        'organize_dataset.py',
        'quick_fix.py',
        'run_training.py',
        'setup_project.py',
        'fix_installation.bat',
        
        # Old training scripts
        'custom_train.py',
        'train_custom.py',
        'train_v2_model.py',
        'train_v2_simple.py',
        
        # Testing/development scripts
        'test_api.py',
        'test_api_components.py',
        'evaluation_report.py',
        
        # Documentation (optional - can keep if needed)
        # 'EVALUATION_SUMMARY.md',
        # 'plan.txt'
    ]
    
    deleted_count = 0
    not_found_count = 0
    
    print("🧹 Cleaning up unnecessary files...")
    print("=" * 50)
    
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Deleted: {file_path}")
                deleted_count += 1
            else:
                print(f"⚠️ Not found: {file_path}")
                not_found_count += 1
        except Exception as e:
            print(f"❌ Error deleting {file_path}: {e}")
    
    print("=" * 50)
    print(f"🎯 Cleanup Summary:")
    print(f"   Files deleted: {deleted_count}")
    print(f"   Files not found: {not_found_count}")
    print(f"   Total processed: {len(files_to_delete)}")
    
    # Show remaining essential files
    print(f"\n✅ Essential files remaining:")
    essential_files = [
        'api/main.py',
        'api/requirements.txt', 
        'api/Dockerfile',
        'src/model.py',
        'src/dataset.py',
        'src/explain.py',
        'src/risk_level.py',
        'src/evaluate.py',
        'src/train.py',
        'knowledge_base/disease_info.json',
        'models/crop_disease_v2_model.pth',
        'requirements.txt'
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
    
    print(f"\n🎉 Project cleanup completed!")
    print(f"📁 Your project now contains only essential files for production.")

if __name__ == "__main__":
    cleanup_project()
