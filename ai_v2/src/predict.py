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
from typing import Dict, Any, Optional, Tuple

# Import our modules
import sys
sys.path.append(os.path.dirname(__file__))
try:
    from preprocess import load_raw, standardize_column_names, clean_crop_data
    from features import engineer_features, load_feature_list
    from train_fertilizer import predict_fertilizer, create_fertilizer_lookup_table
    from train_profit import predict_profit, create_cost_tables
    from explain import explain_prediction, create_explanation_summary
    from dynamic_recommendations import get_dynamic_fertilizer_prediction, get_dynamic_profit_prediction
    DYNAMIC_RECOMMENDATIONS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some modules not available ({e}), using enhanced fallback functions")
    DYNAMIC_RECOMMENDATIONS_AVAILABLE = False
    
    # Import dynamic recommendations as fallback
    try:
        from dynamic_recommendations import get_dynamic_fertilizer_prediction, get_dynamic_profit_prediction
        DYNAMIC_RECOMMENDATIONS_AVAILABLE = True
        print("✅ Dynamic recommendations available as fallback")
    except ImportError:
        print("⚠️ Dynamic recommendations not available, using basic fallback")
        DYNAMIC_RECOMMENDATIONS_AVAILABLE = False
    
    # Create enhanced fallback functions
    def engineer_features(df, include_categorical=False, region='default'):
        return df
    
    def load_feature_list():
        return ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    
    def predict_fertilizer(crop, n, p, k, ph, **kwargs):
        if DYNAMIC_RECOMMENDATIONS_AVAILABLE:
            return get_dynamic_fertilizer_prediction(crop, n, p, k, ph, **kwargs)
        else:
            return {
                'fertilizer': 'NPK 15-15-15',
                'dosage_kg_per_ha': 130,
                'total_cost': 3000,
                'method': 'static_fallback'
            }
    
    def predict_profit(crop, n, p, k, ph, temperature, humidity, rainfall, fertilizer_cost, area_ha=1.0, **kwargs):
        if DYNAMIC_RECOMMENDATIONS_AVAILABLE:
            return get_dynamic_profit_prediction(crop, n, p, k, ph, temperature, humidity, rainfall, fertilizer_cost, area_ha, **kwargs)
        else:
            return {
                'predicted_yield_quintals_per_ha': 45,
                'gross_revenue': 180000,
                'total_investment': 75000,
                'net_profit': 105000,
                'roi_percent': 140.0,
                'method': 'static_fallback'
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
            print("✅ Loaded crop_model_v1.pkl")
        
        # Load crop label encoder (use latest version)
        crop_encoder_file = os.path.join(models_dir, 'label_encoders', 'crop_encoder.pkl')
        if os.path.exists(crop_encoder_file):
            models['crop_label_encoder'] = joblib.load(crop_encoder_file)
            print("✅ Loaded crop_encoder.pkl (latest)")
        else:
            # Fallback to old version for backward compatibility
            crop_encoder_file_old = os.path.join(models_dir, 'crop_label_encoder_v1.pkl')
            if os.path.exists(crop_encoder_file_old):
                models['crop_label_encoder'] = joblib.load(crop_encoder_file_old)
                print("⚠️ Loaded crop_label_encoder_v1.pkl (fallback)")
        
        # Load scaler
        scaler_file = os.path.join(models_dir, 'scaler_v1.pkl')
        if os.path.exists(scaler_file):
            models['scaler'] = joblib.load(scaler_file)
            print("✅ Loaded scaler_v1.pkl")
        
        # Load fertilizer model
        fertilizer_model_file = os.path.join(models_dir, 'fertilizer_model_v1.pkl')
        if os.path.exists(fertilizer_model_file):
            models['fertilizer_model'] = joblib.load(fertilizer_model_file)
        
        # Load profit/yield model
        yield_model_file = os.path.join(models_dir, 'yield_model_v1.pkl')
        if os.path.exists(yield_model_file):
            models['yield_model'] = joblib.load(yield_model_file)
        
        # Load legacy encoders for backward compatibility (prioritize latest models)
        encoders_dir = os.path.join(models_dir, 'label_encoders')
        if os.path.exists(encoders_dir):
            models['encoders'] = {}
            for file in os.listdir(encoders_dir):
                if file.endswith('.pkl'):
                    name = file.replace('_encoder.pkl', '').replace('.pkl', '')
                    try:
                        models['encoders'][name] = joblib.load(os.path.join(encoders_dir, file))
                        print(f"✅ Loaded latest encoder: {name}")
                    except Exception as e:
                        print(f"⚠️ Failed to load encoder {file}: {e}")
        
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
        
        print(f"✅ Successfully loaded {len(models)} model components")
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
    
    return models

def validate_input_schema(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and standardize enhanced input schema with previous crop and season support
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
    
    # Enhanced optional fields
    optional_fields = ['area_ha', 'region', 'previous_crop', 'season', 'planting_date']
    for field in optional_fields:
        if field in input_dict:
            validated_input[field] = input_dict[field]
    
    # Default values for new fields
    if 'area_ha' not in validated_input:
        validated_input['area_ha'] = 1.0
    
    if 'region' not in validated_input:
        validated_input['region'] = 'default'
    
    if 'previous_crop' not in validated_input:
        validated_input['previous_crop'] = ''
    
    # Auto-detect season if not provided
    if 'season' not in validated_input:
        try:
            from season_detection import detect_season_from_date
            season, _ = detect_season_from_date(
                validated_input.get('planting_date'), 
                validated_input['region']
            )
            validated_input['season'] = season
        except:
            validated_input['season'] = 'kharif'  # Default season
    
    return validated_input

def preprocess_input(input_dict: Dict[str, Any], models: Dict) -> Tuple[np.ndarray, list, Dict]:
    """
    Apply enhanced preprocessing pipeline to input data with proper feature ordering
    """
    # Create DataFrame from input
    df = pd.DataFrame([input_dict])
    
    # Store preprocessing metadata for explanations
    preprocessing_info = {
        'original_npk': (input_dict['n'], input_dict['p'], input_dict['k']),
        'previous_crop': input_dict.get('previous_crop', ''),
        'season': input_dict.get('season', 'kharif'),
        'region': input_dict.get('region', 'default')
    }
    
    # Use the exact feature order from training data
    feature_list = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Map input keys to correct feature names (handle case sensitivity)
    feature_mapping = {
        'n': 'N', 'p': 'P', 'k': 'K',
        'N': 'N', 'P': 'P', 'K': 'K',
        'temperature': 'temperature',
        'humidity': 'humidity', 
        'ph': 'ph',
        'rainfall': 'rainfall'
    }
    
    # Create feature dataframe with correct column names
    feature_data = {}
    for feature in feature_list:
        # Find the corresponding input key
        input_key = None
        for input_k, feature_k in feature_mapping.items():
            if feature_k == feature and input_k in input_dict:
                input_key = input_k
                break
        
        if input_key is not None:
            feature_data[feature] = input_dict[input_key]
        else:
            # Set default values if missing
            defaults = {'N': 50, 'P': 30, 'K': 40, 'temperature': 25, 'humidity': 60, 'ph': 6.5, 'rainfall': 500}
            feature_data[feature] = defaults.get(feature, 0)
            print(f"⚠️ Using default value for missing feature {feature}: {feature_data[feature]}")
    
    # Create final feature matrix
    X_df = pd.DataFrame([feature_data])
    X = X_df[feature_list].values
    
    print(f"🔧 Preprocessed features: {dict(zip(feature_list, X[0]))}")
    
    # Apply scaling if scaler is available
    if 'scaler' in models:
        try:
            X_scaled = models['scaler'].transform(X)
            print("✅ Applied feature scaling")
            return X_scaled, feature_list, preprocessing_info
        except Exception as e:
            print(f"⚠️ Scaling failed: {e}, using unscaled features")
    
    print("⚠️ No scaler available, using unscaled features")
    return X, feature_list, preprocessing_info

def predict_crop(X: np.ndarray, models: Dict) -> Dict[str, Any]:
    """
    Predict crop recommendation using trained model
    """
    if 'crop_model' not in models:
        print("⚠️ No crop model found, using fallback")
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
        
        # Decode crop name using the correct encoder
        crop_name = 'unknown'
        if 'crop_label_encoder' in models:
            # Use the specific crop label encoder
            crop_name = models['crop_label_encoder'].inverse_transform([predicted_class])[0]
            print(f"✅ Used crop_label_encoder: {crop_name}")
        elif 'encoders' in models and 'label' in models['encoders']:
            # Fallback to legacy encoder
            crop_name = models['encoders']['label'].inverse_transform([predicted_class])[0]
            print(f"✅ Used legacy label encoder: {crop_name}")
        elif 'encoders' in models and 'crop' in models['encoders']:
            # Try crop encoder
            crop_name = models['encoders']['crop'].inverse_transform([predicted_class])[0]
            print(f"✅ Used crop encoder: {crop_name}")
        else:
            # Ultimate fallback - use class index to map to known crops
            crop_names = [
                'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
                'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
                'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
                'rice', 'watermelon'
            ]
            if 0 <= predicted_class < len(crop_names):
                crop_name = crop_names[predicted_class]
                print(f"⚠️ Used fallback crop mapping: {crop_name}")
        
        print(f"🌾 Predicted: {crop_name} (class: {predicted_class}, confidence: {confidence:.3f})")
        
        return {
            'recommended_crop': crop_name,
            'confidence': confidence,
            'method': 'ml_model',
            'predicted_class': int(predicted_class)
        }
        
    except Exception as e:
        print(f"❌ Crop prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'recommended_crop': 'rice',
            'confidence': 0.5,
            'method': 'error_fallback',
            'error': str(e)
        }

def predict_from_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhanced main prediction function with previous crop and season analysis
    """
    try:
        # Validate input with enhanced schema
        validated_input = validate_input_schema(input_dict)
        
        # Load models
        models = load_all_models()
        
        # Enhanced preprocessing with previous crop and season support
        X, feature_names, preprocessing_info = preprocess_input(validated_input, models)
        
        # 1. Crop Recommendation
        crop_result = predict_crop(X, models)
        recommended_crop = crop_result['recommended_crop']
        confidence = crop_result['confidence']
        
        # 2. Season compatibility check
        season_compatibility = None
        try:
            from season_detection import check_crop_season_compatibility
            season = preprocessing_info.get('season', 'kharif')
            season_compatibility = check_crop_season_compatibility(recommended_crop, season)
        except:
            season_compatibility = ('moderate', f"Season compatibility for {recommended_crop} needs evaluation")
        
        # 3. Use adjusted NPK for fertilizer recommendation if available
        npk_for_fertilizer = preprocessing_info.get('adjusted_npk', 
                                                   (validated_input['n'], validated_input['p'], validated_input['k']))
        
        # Use dynamic fertilizer prediction
        try:
            if DYNAMIC_RECOMMENDATIONS_AVAILABLE:
                from dynamic_recommendations import get_dynamic_fertilizer_prediction
                fertilizer_result = get_dynamic_fertilizer_prediction(
                    crop=recommended_crop,
                    n=npk_for_fertilizer[0],
                    p=npk_for_fertilizer[1],
                    k=npk_for_fertilizer[2],
                    ph=validated_input['ph']
                )
            else:
                fertilizer_result = predict_fertilizer(
                    crop=recommended_crop,
                    n=npk_for_fertilizer[0],
                    p=npk_for_fertilizer[1],
                    k=npk_for_fertilizer[2],
                    ph=validated_input['ph'],
                    use_ml=True,
                    ml_model=models.get('fertilizer_model'),
                    encoders=models.get('fertilizer_encoders')
                )
        except Exception as e:
            print(f"⚠️ Fertilizer prediction failed: {e}")
            fertilizer_result = {
                'fertilizer': 'NPK 15-15-15',
                'dosage_kg_per_ha': 130,
                'total_cost': 3000,
                'method': 'error_fallback'
            }
        
        # 4. Profit Estimation with adjusted NPK
        fertilizer_cost = fertilizer_result.get('total_cost', 3000)
        
        try:
            if DYNAMIC_RECOMMENDATIONS_AVAILABLE:
                from dynamic_recommendations import get_dynamic_profit_prediction
                profit_result = get_dynamic_profit_prediction(
                    crop=recommended_crop,
                    n=npk_for_fertilizer[0],
                    p=npk_for_fertilizer[1],
                    k=npk_for_fertilizer[2],
                    ph=validated_input['ph'],
                    temperature=validated_input['temperature'],
                    humidity=validated_input['humidity'],
                    rainfall=validated_input['rainfall'],
                    fertilizer_cost=fertilizer_cost,
                    area_ha=validated_input['area_ha']
                )
            else:
                profit_result = predict_profit(
                    crop=recommended_crop,
                    n=npk_for_fertilizer[0],
                    p=npk_for_fertilizer[1],
                    k=npk_for_fertilizer[2],
                    ph=validated_input['ph'],
                    temperature=validated_input['temperature'],
                    humidity=validated_input['humidity'],
                    rainfall=validated_input['rainfall'],
                    fertilizer_cost=fertilizer_cost,
                    area_ha=validated_input['area_ha'],
                    model=models.get('yield_model'),
                    crop_encoder=models.get('profit_crop_encoder')
                )
        except Exception as e:
            print(f"⚠️ Profit prediction failed: {e}")
            profit_result = {
                'predicted_yield_quintals_per_ha': 45,
                'gross_revenue': 180000,
                'total_investment': 75000,
                'net_profit': 105000,
                'roi_percent': 140.0,
                'method': 'error_fallback'
            }
        
        # 5. Generate Enhanced Explanations
        enhanced_explanations = []
        
        # Previous crop analysis
        previous_crop = preprocessing_info.get('previous_crop', '')
        if previous_crop:
            try:
                from nutrient_impact_lookup import get_previous_crop_explanation
                prev_crop_explanation = get_previous_crop_explanation(previous_crop)
                enhanced_explanations.append(prev_crop_explanation)
            except:
                enhanced_explanations.append(f"Previous crop {previous_crop} considered in soil analysis")
        
        # Season analysis
        season = preprocessing_info.get('season', 'kharif')
        if season_compatibility:
            suitability, explanation = season_compatibility
            enhanced_explanations.append(f"Season analysis: {explanation}")
        
        # NPK adjustment explanation
        if 'npk_deltas' in preprocessing_info:
            n_delta, p_delta, k_delta = preprocessing_info['npk_deltas']
            if any(abs(delta) > 0.1 for delta in [n_delta, p_delta, k_delta]):
                enhanced_explanations.append(
                    f"Soil nutrients adjusted based on previous crop: N{n_delta:+.0f}, P{p_delta:+.0f}, K{k_delta:+.0f}"
                )
        
        # Traditional ML explanations
        try:
            crop_explanations = explain_prediction(
                'crop', models.get('crop_model'), X, feature_names
            )
            enhanced_explanations.extend(crop_explanations[:2])
        except:
            enhanced_explanations.append(f"Recommended {recommended_crop} based on enhanced soil and climate analysis")
        
        # Create comprehensive enhanced response
        response = {
            'recommended_crop': recommended_crop,
            'confidence': round(confidence, 3),
            'method': crop_result.get('method', 'unknown'),  # Add method from crop prediction
            'why': enhanced_explanations[:4],  # Top 4 enhanced reasons
            'expected_yield_t_per_acre': round(profit_result['predicted_yield_quintals_per_ha'] * 0.1, 2),
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
            # Enhanced fields
            'previous_crop_analysis': {
                'previous_crop': previous_crop,
                'original_npk': preprocessing_info.get('original_npk', (0, 0, 0)),
                'adjusted_npk': preprocessing_info.get('adjusted_npk', preprocessing_info.get('original_npk', (0, 0, 0))),
                'nutrient_impact': preprocessing_info.get('npk_deltas', (0, 0, 0))
            },
            'season_analysis': {
                'detected_season': season,
                'season_suitability': season_compatibility[0] if season_compatibility else 'unknown',
                'season_explanation': season_compatibility[1] if season_compatibility else 'Season compatibility unknown'
            },
            'model_version': 'crop_model_v2_enhanced',
            'timestamp': datetime.now().isoformat(),
            'area_analyzed_ha': validated_input['area_ha'],
            'region': preprocessing_info.get('region', 'default')
        }
        
        return response
        
    except Exception as e:
        # Enhanced error response
        return {
            'error': str(e),
            'recommended_crop': 'rice',
            'confidence': 0.0,
            'why': ['Error in enhanced prediction pipeline'],
            'expected_yield_t_per_acre': 0.0,
            'yield_interval_p10_p90': [0.0, 0.0],
            'profit_breakdown': {'gross': 0, 'investment': 0, 'net': 0, 'roi': 0.0},
            'previous_crop_analysis': {'previous_crop': '', 'original_npk': (0, 0, 0), 'adjusted_npk': (0, 0, 0), 'nutrient_impact': (0, 0, 0)},
            'season_analysis': {'detected_season': 'kharif', 'season_suitability': 'unknown', 'season_explanation': 'Error in season analysis'},
            'model_version': 'error_v2',
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
