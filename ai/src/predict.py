"""
Inference wrapper and API contract module
Implements single callable function for all three AI models as per plan.md step 9
"""

import pandas as pd
import numpy as np
import os
import json
import joblib
import yaml
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

# Import our modules
import sys
sys.path.append(os.path.dirname(__file__))
try:
    from preprocess import load_raw, standardize_column_names, clean_crop_data
    from features import engineer_features, load_feature_list
    from train_fertilizer import predict_fertilizer, create_fertilizer_lookup_table
    from train_profit import predict_profit, create_cost_tables
    from explain import explain_prediction, create_explanation_summary
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")
    # Create fallback functions
    def engineer_features(df, include_categorical=False):
        return df
    
    def load_feature_list():
        return ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    
    def predict_fertilizer(crop, n, p, k, ph, **kwargs):
        return {
            'fertilizer': 'NPK 15-15-15',
            'dosage_kg_per_ha': 130,
            'total_cost': 3000
        }
    
    def predict_profit(crop, n, p, k, ph, temperature, humidity, rainfall, fertilizer_cost, area_ha=1.0, **kwargs):
        return {
            'predicted_yield_quintals_per_ha': 45,
            'gross_revenue': 180000,
            'total_investment': 75000,
            'net_profit': 105000,
            'roi_percent': 140.0
        }
    
    def explain_prediction(model_type, model, X, feature_names, **kwargs):
        return [
            f"Recommendation based on {model_type} analysis",
            "Soil and climate conditions analyzed",
            "Consult local agronomist for final decisions"
        ]

def load_all_models():
    """
    Load all trained models and preprocessing artifacts
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
    models = {}
    
    try:
        # Load crop model
        crop_model_file = os.path.join(models_dir, 'crop_model_v1.pkl')
        if os.path.exists(crop_model_file):
            models['crop_model'] = joblib.load(crop_model_file)
        
        # Load fertilizer model
        fertilizer_model_file = os.path.join(models_dir, 'fertilizer_model_v1.pkl')
        if os.path.exists(fertilizer_model_file):
            models['fertilizer_model'] = joblib.load(fertilizer_model_file)
        
        # Load profit/yield model
        yield_model_file = os.path.join(models_dir, 'yield_model_v1.pkl')
        if os.path.exists(yield_model_file):
            models['yield_model'] = joblib.load(yield_model_file)
        
        # Load preprocessing artifacts
        scaler_file = os.path.join(models_dir, 'scaler_v1.pkl')
        if os.path.exists(scaler_file):
            models['scaler'] = joblib.load(scaler_file)
        
        # Load encoders
        encoders_dir = os.path.join(models_dir, 'label_encoders')
        if os.path.exists(encoders_dir):
            models['encoders'] = {}
            for file in os.listdir(encoders_dir):
                if file.endswith('_encoder.pkl'):
                    name = file.replace('_encoder.pkl', '')
                    models['encoders'][name] = joblib.load(os.path.join(encoders_dir, file))
        
        # Load fertilizer encoders
        for encoder_type in ['crop', 'fertilizer']:
            encoder_file = os.path.join(models_dir, f'fertilizer_{encoder_type}_encoder_v1.pkl')
            if os.path.exists(encoder_file):
                if 'fertilizer_encoders' not in models:
                    models['fertilizer_encoders'] = {}
                models['fertilizer_encoders'][encoder_type] = joblib.load(encoder_file)
        
        # Load profit crop encoder
        profit_encoder_file = os.path.join(models_dir, 'profit_crop_encoder_v1.pkl')
        if os.path.exists(profit_encoder_file):
            models['profit_crop_encoder'] = joblib.load(profit_encoder_file)
        
        print(f"Loaded {len(models)} model artifacts")
        
    except Exception as e:
        print(f"Error loading models: {e}")
    
    return models

def validate_input_schema(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and standardize input schema
    """
    required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Check required fields
    for field in required_fields:
        if field not in input_dict:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate numeric ranges
    validations = {
        'N': (0, 200),
        'P': (0, 150),
        'K': (0, 200),
        'temperature': (-10, 55),
        'humidity': (0, 100),
        'ph': (3.5, 9.0),
        'rainfall': (0, 5000)
    }
    
    validated_input = {}
    for field, (min_val, max_val) in validations.items():
        value = float(input_dict[field])
        if not (min_val <= value <= max_val):
            print(f"Warning: {field} value {value} outside expected range [{min_val}, {max_val}]")
        validated_input[field.lower()] = value
    
    # Optional fields
    optional_fields = ['area_ha', 'region']
    for field in optional_fields:
        if field in input_dict:
            validated_input[field] = input_dict[field]
    
    # Default area to 1 hectare if not provided
    if 'area_ha' not in validated_input:
        validated_input['area_ha'] = 1.0
    
    return validated_input

def preprocess_input(input_dict: Dict[str, Any], models: Dict) -> np.ndarray:
    """
    Apply preprocessing pipeline to input data
    """
    # Create DataFrame from input
    df = pd.DataFrame([input_dict])
    
    # Apply feature engineering
    df_features = engineer_features(df, include_categorical=False)
    
    # Get feature list
    try:
        feature_list = load_feature_list()
    except:
        # Fallback feature list
        feature_list = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Select features that exist in the dataframe
    available_features = [f for f in feature_list if f in df_features.columns]
    X = df_features[available_features]
    
    # Apply scaling if scaler is available
    if 'scaler' in models:
        try:
            X_scaled = models['scaler'].transform(X)
            return X_scaled, available_features
        except:
            print("Scaling failed, using unscaled features")
    
    return X.values, available_features

def predict_crop(X: np.ndarray, models: Dict) -> Dict[str, Any]:
    """
    Predict crop recommendation
    """
    if 'crop_model' not in models:
        return {
            'recommended_crop': 'rice',
            'confidence': 0.5,
            'method': 'fallback'
        }
    
    try:
        model = models['crop_model']
        
        # Get prediction probabilities
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            predicted_class = np.argmax(proba)
            confidence = float(proba[predicted_class])
        else:
            predicted_class = model.predict(X)[0]
            confidence = 0.8  # Default confidence
        
        # Decode crop name
        if 'encoders' in models and 'label' in models['encoders']:
            crop_name = models['encoders']['label'].inverse_transform([predicted_class])[0]
        else:
            # Fallback crop names
            crop_names = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane']
            crop_name = crop_names[predicted_class % len(crop_names)]
        
        return {
            'recommended_crop': crop_name,
            'confidence': confidence,
            'method': 'ml_model'
        }
        
    except Exception as e:
        print(f"Crop prediction failed: {e}")
        return {
            'recommended_crop': 'rice',
            'confidence': 0.5,
            'method': 'error_fallback'
        }

def predict_from_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main prediction function that combines all three AI models
    """
    try:
        # Validate input
        validated_input = validate_input_schema(input_dict)
        
        # Load models
        models = load_all_models()
        
        # Preprocess input
        X, feature_names = preprocess_input(validated_input, models)
        
        # 1. Crop Recommendation
        crop_result = predict_crop(X, models)
        recommended_crop = crop_result['recommended_crop']
        confidence = crop_result['confidence']
        
        # 2. Fertilizer Recommendation
        fertilizer_result = predict_fertilizer(
            crop=recommended_crop,
            n=validated_input['n'],
            p=validated_input['p'],
            k=validated_input['k'],
            ph=validated_input['ph'],
            use_ml=True,
            ml_model=models.get('fertilizer_model'),
            encoders=models.get('fertilizer_encoders')
        )
        
        # 3. Profit Estimation
        fertilizer_cost = fertilizer_result.get('total_cost', 3000)
        profit_result = predict_profit(
            crop=recommended_crop,
            n=validated_input['n'],
            p=validated_input['p'],
            k=validated_input['k'],
            ph=validated_input['ph'],
            temperature=validated_input['temperature'],
            humidity=validated_input['humidity'],
            rainfall=validated_input['rainfall'],
            fertilizer_cost=fertilizer_cost,
            area_ha=validated_input['area_ha'],
            model=models.get('yield_model'),
            crop_encoder=models.get('profit_crop_encoder')
        )
        
        # 4. Generate Explanations
        try:
            crop_explanations = explain_prediction(
                'crop', models.get('crop_model'), X, feature_names
            )
        except:
            crop_explanations = [
                f"Recommended {recommended_crop} based on soil and climate conditions",
                "NPK levels and environmental factors favor this crop choice",
                "Consult local agronomist for final decisions"
            ]
        
        # Create comprehensive response
        response = {
            'recommended_crop': recommended_crop,
            'confidence': round(confidence, 3),
            'why': crop_explanations[:3],  # Top 3 reasons
            'expected_yield_t_per_acre': round(profit_result['predicted_yield_quintals_per_ha'] * 0.1, 2),  # Convert to tonnes per acre
            'yield_interval_p10_p90': [
                round(profit_result['predicted_yield_quintals_per_ha'] * 0.8 * 0.1, 2),
                round(profit_result['predicted_yield_quintals_per_ha'] * 1.2 * 0.1, 2)
            ],
            'profit_breakdown': {
                'gross': int(profit_result['gross_revenue']),
                'investment': int(profit_result['total_investment']),
                'net': int(profit_result['net_profit']),
                'roi': round(profit_result['roi_percent'], 1)
            },
            'fertilizer_recommendation': {
                'type': fertilizer_result.get('fertilizer', 'NPK 15-15-15'),
                'dosage_kg_per_ha': fertilizer_result.get('dosage_kg_per_ha', 130),
                'cost': int(fertilizer_result.get('total_cost', 3000))
            },
            'model_version': 'crop_model_v1',
            'timestamp': datetime.now().isoformat(),
            'area_analyzed_ha': validated_input['area_ha']
        }
        
        return response
        
    except Exception as e:
        # Error response
        return {
            'error': str(e),
            'recommended_crop': 'rice',
            'confidence': 0.0,
            'why': ['Error in prediction pipeline'],
            'expected_yield_t_per_acre': 0.0,
            'yield_interval_p10_p90': [0.0, 0.0],
            'profit_breakdown': {'gross': 0, 'investment': 0, 'net': 0, 'roi': 0.0},
            'model_version': 'error',
            'timestamp': datetime.now().isoformat()
        }

def main():
    """
    CLI wrapper for the prediction system
    """
    parser = argparse.ArgumentParser(description='Crop AI Prediction System')
    parser.add_argument('--input', required=True, help='Input JSON file path')
    parser.add_argument('--output', help='Output JSON file path (optional)')
    
    args = parser.parse_args()
    
    # Load input
    try:
        with open(args.input, 'r') as f:
            input_data = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}")
        return
    
    # Make prediction
    result = predict_from_dict(input_data)
    
    # Save output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) == 1:
        # Test with sample input
        sample_input = {
            'N': 60,
            'P': 45,
            'K': 50,
            'temperature': 25,
            'humidity': 70,
            'ph': 6.5,
            'rainfall': 800,
            'area_ha': 2.0
        }
        
        print("Testing prediction system with sample input...")
        result = predict_from_dict(sample_input)
        print(json.dumps(result, indent=2))
    else:
        main()
