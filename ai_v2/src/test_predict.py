#!/usr/bin/env python3
"""
Simple test script to verify predict.py functionality
"""
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from predict import predict_from_dict
    
    # Load the sample input
    with open('sample_input_enhanced.json', 'r') as f:
        input_data = json.load(f)
    
    print("Loaded input data:", input_data)
    
    # Make prediction
    result = predict_from_dict(input_data)
    
    # Save result
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("Prediction completed successfully!")
    print("Result saved to result.json")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
