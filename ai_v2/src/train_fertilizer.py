"""
Fertilizer recommendation model training module
Implements hybrid approach: lookup table + ML model as per plan.md step 6
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime

def create_fertilizer_lookup_table():
    """
    Create rule-based fertilizer lookup table based on crop and soil conditions
    This is a simplified version - in practice would be based on agricultural expertise
    """
    
    # Basic fertilizer recommendations by crop type
    fertilizer_rules = {
        'rice': {
            'base_fertilizer': 'NPK 20-10-10',
            'dosage_kg_per_ha': 150,
            'cost_per_kg': 25,
            'conditions': {
                'high_n': {'fertilizer': 'Urea', 'dosage_kg_per_ha': 100, 'cost_per_kg': 15},
                'low_p': {'fertilizer': 'DAP', 'dosage_kg_per_ha': 75, 'cost_per_kg': 30},
                'low_k': {'fertilizer': 'MOP', 'dosage_kg_per_ha': 50, 'cost_per_kg': 20}
            }
        },
        'wheat': {
            'base_fertilizer': 'NPK 18-12-8',
            'dosage_kg_per_ha': 120,
            'cost_per_kg': 28,
            'conditions': {
                'high_n': {'fertilizer': 'Urea', 'dosage_kg_per_ha': 80, 'cost_per_kg': 15},
                'low_p': {'fertilizer': 'SSP', 'dosage_kg_per_ha': 100, 'cost_per_kg': 22},
                'low_k': {'fertilizer': 'MOP', 'dosage_kg_per_ha': 40, 'cost_per_kg': 20}
            }
        },
        'maize': {
            'base_fertilizer': 'NPK 16-16-16',
            'dosage_kg_per_ha': 140,
            'cost_per_kg': 26,
            'conditions': {
                'high_n': {'fertilizer': 'Urea', 'dosage_kg_per_ha': 90, 'cost_per_kg': 15},
                'low_p': {'fertilizer': 'DAP', 'dosage_kg_per_ha': 80, 'cost_per_kg': 30},
                'low_k': {'fertilizer': 'MOP', 'dosage_kg_per_ha': 60, 'cost_per_kg': 20}
            }
        },
        'cotton': {
            'base_fertilizer': 'NPK 14-14-14',
            'dosage_kg_per_ha': 160,
            'cost_per_kg': 24,
            'conditions': {
                'high_n': {'fertilizer': 'Urea', 'dosage_kg_per_ha': 110, 'cost_per_kg': 15},
                'low_p': {'fertilizer': 'SSP', 'dosage_kg_per_ha': 120, 'cost_per_kg': 22},
                'low_k': {'fertilizer': 'MOP', 'dosage_kg_per_ha': 70, 'cost_per_kg': 20}
            }
        }
    }
    
    return fertilizer_rules

def analyze_soil_conditions(n, p, k, ph):
    """
    Analyze soil conditions to determine nutrient deficiencies
    """
    conditions = []
    
    # Nutrient thresholds (these would be calibrated with soil testing standards)
    if n > 80:
        conditions.append('high_n')
    elif n < 40:
        conditions.append('low_n')
    
    if p < 30:
        conditions.append('low_p')
    elif p > 70:
        conditions.append('high_p')
    
    if k < 35:
        conditions.append('low_k')
    elif k > 75:
        conditions.append('high_k')
    
    # pH-based recommendations
    if ph < 6.0:
        conditions.append('acidic_soil')
    elif ph > 7.5:
        conditions.append('alkaline_soil')
    
    return conditions

def lookup_fertilizer_recommendation(crop, n, p, k, ph):
    """
    Get fertilizer recommendation using lookup table
    """
    fertilizer_rules = create_fertilizer_lookup_table()
    
    # Default recommendation if crop not in lookup
    if crop not in fertilizer_rules:
        return {
            'fertilizer': 'NPK 15-15-15',
            'dosage_kg_per_ha': 130,
            'cost_per_kg': 25,
            'total_cost': 130 * 25,
            'method': 'default'
        }
    
    crop_rules = fertilizer_rules[crop]
    soil_conditions = analyze_soil_conditions(n, p, k, ph)
    
    # Start with base recommendation
    recommendation = {
        'fertilizer': crop_rules['base_fertilizer'],
        'dosage_kg_per_ha': crop_rules['dosage_kg_per_ha'],
        'cost_per_kg': crop_rules['cost_per_kg'],
        'method': 'lookup'
    }
    
    # Adjust based on soil conditions
    adjustments = []
    for condition in soil_conditions:
        if condition in crop_rules['conditions']:
            adj = crop_rules['conditions'][condition]
            adjustments.append({
                'condition': condition,
                'additional_fertilizer': adj['fertilizer'],
                'additional_dosage': adj['dosage_kg_per_ha'],
                'additional_cost': adj['dosage_kg_per_ha'] * adj['cost_per_kg']
            })
    
    # Calculate total cost
    base_cost = recommendation['dosage_kg_per_ha'] * recommendation['cost_per_kg']
    additional_cost = sum(adj['additional_cost'] for adj in adjustments)
    
    recommendation.update({
        'total_cost': base_cost + additional_cost,
        'adjustments': adjustments,
        'soil_conditions': soil_conditions
    })
    
    return recommendation

def create_training_data_for_ml():
    """
    Create synthetic training data for ML-based fertilizer recommendation
    This would normally come from agricultural databases
    """
    np.random.seed(42)
    n_samples = 1000
    
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'soybean']
    fertilizers = ['NPK 20-10-10', 'NPK 18-12-8', 'NPK 16-16-16', 'NPK 14-14-14', 'Urea', 'DAP', 'SSP', 'MOP']
    
    data = []
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        n = np.random.normal(60, 20)
        p = np.random.normal(50, 15)
        k = np.random.normal(55, 18)
        ph = np.random.normal(6.5, 1.0)
        
        # Simple rules to assign fertilizer (this would be expert knowledge)
        if crop in ['rice', 'wheat'] and n < 50:
            fertilizer = 'Urea'
        elif p < 40:
            fertilizer = 'DAP'
        elif k < 45:
            fertilizer = 'MOP'
        else:
            fertilizer = f'NPK {np.random.choice(["20-10-10", "18-12-8", "16-16-16", "14-14-14"])}'
        
        data.append({
            'crop': crop,
            'n': max(0, n),
            'p': max(0, p),
            'k': max(0, k),
            'ph': np.clip(ph, 4.0, 9.0),
            'fertilizer': fertilizer
        })
    
    return pd.DataFrame(data)

def train_ml_fertilizer_model():
    """
    Train ML model for fertilizer recommendation as backup to lookup table
    """
    # Create training data
    df = create_training_data_for_ml()
    
    # Prepare features
    feature_cols = ['n', 'p', 'k', 'ph']
    X = df[feature_cols]
    
    # Encode categorical variables
    from sklearn.preprocessing import LabelEncoder
    crop_encoder = LabelEncoder()
    fertilizer_encoder = LabelEncoder()
    
    df['crop_encoded'] = crop_encoder.fit_transform(df['crop'])
    y = fertilizer_encoder.fit_transform(df['fertilizer'])
    
    # Add crop as feature
    X = X.copy()
    X['crop_encoded'] = df['crop_encoded']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest (good for categorical features)
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"ML Fertilizer Model Accuracy: {accuracy:.4f}")
    
    return model, crop_encoder, fertilizer_encoder, feature_cols

def predict_fertilizer(crop, n, p, k, ph, use_ml=False, ml_model=None, encoders=None):
    """
    Predict fertilizer recommendation using hybrid approach
    """
    # Primary method: lookup table
    lookup_result = lookup_fertilizer_recommendation(crop, n, p, k, ph)
    
    if not use_ml or ml_model is None:
        return lookup_result
    
    # Secondary method: ML model
    try:
        model, crop_encoder, fertilizer_encoder = ml_model, encoders['crop'], encoders['fertilizer']
        
        # Prepare input
        crop_encoded = crop_encoder.transform([crop])[0] if crop in crop_encoder.classes_ else 0
        X_input = np.array([[n, p, k, ph, crop_encoded]])
        
        # Predict
        ml_pred = model.predict(X_input)[0]
        ml_fertilizer = fertilizer_encoder.inverse_transform([ml_pred])[0]
        
        # Combine results
        lookup_result['ml_recommendation'] = ml_fertilizer
        lookup_result['method'] = 'hybrid'
        
    except Exception as e:
        print(f"ML prediction failed: {e}")
        lookup_result['ml_error'] = str(e)
    
    return lookup_result

def save_fertilizer_artifacts(model=None, encoders=None, lookup_table=None, version='v1'):
    """
    Save fertilizer recommendation artifacts
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save ML model if available
    if model is not None:
        model_file = os.path.join(models_dir, f'fertilizer_model_{version}.pkl')
        joblib.dump(model, model_file)
        print(f"ML model saved: {model_file}")
    
    # Save encoders
    if encoders is not None:
        for name, encoder in encoders.items():
            encoder_file = os.path.join(models_dir, f'fertilizer_{name}_encoder_{version}.pkl')
            joblib.dump(encoder, encoder_file)
    
    # Save lookup table
    if lookup_table is None:
        lookup_table = create_fertilizer_lookup_table()
    
    lookup_file = os.path.join(models_dir, f'fertilizer_lookup_{version}.json')
    with open(lookup_file, 'w') as f:
        json.dump(lookup_table, f, indent=2)
    
    # Save evaluation
    eval_data = {
        'version': version,
        'timestamp': datetime.now().isoformat(),
        'method': 'hybrid_lookup_ml',
        'lookup_crops': list(lookup_table.keys()) if lookup_table else [],
        'has_ml_model': model is not None
    }
    
    eval_file = os.path.join(models_dir, f'fertilizer_eval_{version}.json')
    with open(eval_file, 'w') as f:
        json.dump(eval_data, f, indent=2)
    
    print(f"Fertilizer artifacts saved to {models_dir}")

def train_fertilizer_system():
    """
    Main training pipeline for fertilizer recommendation system
    """
    print("=" * 50)
    print("FERTILIZER RECOMMENDATION SYSTEM TRAINING")
    print("=" * 50)
    
    # Create lookup table
    print("\nCreating fertilizer lookup table...")
    lookup_table = create_fertilizer_lookup_table()
    print(f"Lookup table created for {len(lookup_table)} crops")
    
    # Train ML model as backup
    print("\nTraining ML backup model...")
    ml_model, crop_encoder, fertilizer_encoder, feature_cols = train_ml_fertilizer_model()
    
    encoders = {
        'crop': crop_encoder,
        'fertilizer': fertilizer_encoder
    }
    
    # Test the system
    print("\nTesting fertilizer recommendation system...")
    test_cases = [
        ('rice', 45, 35, 40, 6.2),
        ('wheat', 70, 55, 60, 7.1),
        ('maize', 55, 25, 45, 6.8)
    ]
    
    for crop, n, p, k, ph in test_cases:
        result = predict_fertilizer(crop, n, p, k, ph, use_ml=True, 
                                  ml_model=ml_model, encoders=encoders)
        print(f"\n{crop.upper()} recommendation:")
        print(f"  Fertilizer: {result['fertilizer']}")
        print(f"  Dosage: {result['dosage_kg_per_ha']} kg/ha")
        print(f"  Cost: ₹{result['total_cost']}")
    
    # Save artifacts
    print("\nSaving fertilizer artifacts...")
    save_fertilizer_artifacts(ml_model, encoders, lookup_table)
    
    print("\n" + "=" * 50)
    print("FERTILIZER SYSTEM TRAINING COMPLETED!")
    print("=" * 50)
    
    return ml_model, encoders, lookup_table

if __name__ == "__main__":
    # Run fertilizer system training
    model, encoders, lookup_table = train_fertilizer_system()
