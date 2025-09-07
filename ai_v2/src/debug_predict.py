#!/usr/bin/env python3
"""
Debug script to identify the exact issue with engineer_features
"""
import json
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

print("Testing imports...")

try:
    from features import engineer_features
    print("✓ Successfully imported engineer_features from features.py")
    
    # Test the function signature
    import inspect
    sig = inspect.signature(engineer_features)
    print(f"Function signature: {sig}")
    
except ImportError as e:
    print(f"✗ Failed to import engineer_features: {e}")

# Load sample data and test
try:
    with open('sample_input_enhanced.json', 'r') as f:
        input_data = json.load(f)
    print(f"✓ Loaded input data: {input_data}")
    
    # Create DataFrame
    df = pd.DataFrame([input_data])
    print(f"✓ Created DataFrame with columns: {list(df.columns)}")
    
    # Test engineer_features call
    region = input_data.get('region', 'default')
    print(f"Region parameter: {region}")
    
    try:
        df_features = engineer_features(df, include_categorical=False, region=region)
        print("✓ engineer_features call successful!")
        print(f"Output columns: {list(df_features.columns)}")
    except Exception as e:
        print(f"✗ engineer_features call failed: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"✗ Error in testing: {e}")
    import traceback
    traceback.print_exc()
