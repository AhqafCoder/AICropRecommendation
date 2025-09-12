"""
Profit estimation model training module
Implements yield predictor + deterministic profit calculation as per plan.md step 7
Enhanced with LightGBM for better performance
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import lightgbm as lgb
import joblib
from datetime import datetime

def create_cost_tables():
    """
    Create cost tables for different crops and inputs
    Based on typical Indian agricultural costs (simplified)
    """
    
    # Cost per hectare by crop type (in INR)
    cultivation_costs = {
        'rice': {
            'seeds': 2500,
            'labor': 15000,
            'irrigation': 8000,
            'machinery': 5000,
            'pesticides': 3000,
            'other': 2000
        },
        'wheat': {
            'seeds': 3000,
            'labor': 12000,
            'irrigation': 6000,
            'machinery': 6000,
            'pesticides': 2500,
            'other': 1500
        },
        'maize': {
            'seeds': 4000,
            'labor': 10000,
            'irrigation': 7000,
            'machinery': 5500,
            'pesticides': 3500,
            'other': 2000
        },
        'cotton': {
            'seeds': 5000,
            'labor': 18000,
            'irrigation': 10000,
            'machinery': 7000,
            'pesticides': 8000,
            'other': 3000
        },
        'sugarcane': {
            'seeds': 15000,
            'labor': 25000,
            'irrigation': 12000,
            'machinery': 8000,
            'pesticides': 5000,
            'other': 5000
        }
    }
    
    # Market prices per quintal (100 kg) - modal prices
    market_prices = {
        'rice': 2200,
        'wheat': 2100,
        'maize': 1800,
        'cotton': 5500,  # per quintal of cotton
        'sugarcane': 350,  # per quintal
        'soybean': 4200,
        'groundnut': 5800
    }
    
    return cultivation_costs, market_prices

def create_yield_training_data():
    """
    Create synthetic yield training data
    In practice, this would come from agricultural databases
    """
    np.random.seed(42)
    n_samples = 2000
    
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'soybean']
    
    data = []
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        
        # Environmental factors
        n = np.random.normal(60, 20)
        p = np.random.normal(50, 15)
        k = np.random.normal(55, 18)
        ph = np.random.normal(6.5, 1.0)
        temperature = np.random.normal(25, 5)
        humidity = np.random.normal(70, 15)
        rainfall = np.random.normal(800, 300)
        
        # Fertilizer cost (proxy for input quality)
        fertilizer_cost = np.random.normal(3000, 1000)
        
        # Base yields by crop (quintals per hectare)
        base_yields = {
            'rice': 45, 'wheat': 35, 'maize': 55, 
            'cotton': 15, 'sugarcane': 650, 'soybean': 20
        }
        
        base_yield = base_yields.get(crop, 30)
        
        # Yield influenced by conditions
        yield_factor = 1.0
        
        # NPK influence
        if n < 40: yield_factor *= 0.8
        elif n > 80: yield_factor *= 1.1
        
        if p < 30: yield_factor *= 0.85
        elif p > 70: yield_factor *= 1.05
        
        if k < 35: yield_factor *= 0.9
        elif k > 75: yield_factor *= 1.05
        
        # Environmental influence
        if 20 <= temperature <= 30: yield_factor *= 1.1
        elif temperature < 15 or temperature > 40: yield_factor *= 0.7
        
        if 60 <= humidity <= 80: yield_factor *= 1.05
        elif humidity < 40 or humidity > 90: yield_factor *= 0.8
        
        if crop in ['rice', 'sugarcane'] and rainfall > 1000: yield_factor *= 1.2
        elif crop in ['wheat', 'maize'] and 400 <= rainfall <= 800: yield_factor *= 1.1
        elif rainfall < 200: yield_factor *= 0.6
        
        # pH influence
        if 6.0 <= ph <= 7.5: yield_factor *= 1.05
        elif ph < 5.0 or ph > 8.5: yield_factor *= 0.8
        
        # Input quality influence
        if fertilizer_cost > 4000: yield_factor *= 1.1
        elif fertilizer_cost < 2000: yield_factor *= 0.9
        
        # Add random variation
        yield_factor *= np.random.normal(1.0, 0.15)
        
        actual_yield = max(0, base_yield * yield_factor)
        
        data.append({
            'crop': crop,
            'n': max(0, n),
            'p': max(0, p),
            'k': max(0, k),
            'ph': np.clip(ph, 4.0, 9.0),
            'temperature': np.clip(temperature, 5, 45),
            'humidity': np.clip(humidity, 20, 100),
            'rainfall': max(0, rainfall),
            'fertilizer_cost': max(1000, fertilizer_cost),
            'yield_quintals_per_ha': actual_yield
        })
    
    return pd.DataFrame(data)

def train_yield_model():
    """
    Train yield prediction model using LightGBM regressor
    """
    # Create training data
    df = create_yield_training_data()
    
    # Prepare features
    feature_cols = ['n', 'p', 'k', 'ph', 'temperature', 'humidity', 'rainfall', 'fertilizer_cost']
    
    # Encode crop
    from sklearn.preprocessing import LabelEncoder
    crop_encoder = LabelEncoder()
    df['crop_encoded'] = crop_encoder.fit_transform(df['crop'])
    
    # Features and target
    X = df[feature_cols + ['crop_encoded']]
    y = df['yield_quintals_per_ha']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train LightGBM regressor for better performance
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0,
        'random_state': 42
    }
    
    model = lgb.train(
        params,
        train_data,
        valid_sets=[valid_data],
        num_boost_round=1000,
        callbacks=[lgb.early_stopping(100), lgb.log_evaluation(0)]
    )
    
    # Evaluate
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Yield Model Performance (LightGBM):")
    print(f"  MAE: {mae:.2f} quintals/ha")
    print(f"  RMSE: {rmse:.2f} quintals/ha")
    print(f"  R²: {r2:.4f}")
    print(f"  Best iteration: {model.best_iteration}")
    
    # Get feature importance
    feature_importance = model.feature_importance(importance_type='gain')
    feature_names = X.columns.tolist()
    
    metrics = {
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'best_iteration': int(model.best_iteration),
        'feature_importance': dict(zip(feature_names, feature_importance.tolist()))
    }
    
    return model, crop_encoder, feature_cols, metrics

def calculate_profit(crop, predicted_yield, fertilizer_cost, area_ha=1.0):
    """
    Calculate profit using deterministic approach
    """
    cultivation_costs, market_prices = create_cost_tables()
    
    # Get costs for the crop
    if crop in cultivation_costs:
        costs = cultivation_costs[crop].copy()
    else:
        # Default costs for unknown crops
        costs = {
            'seeds': 3000,
            'labor': 12000,
            'irrigation': 7000,
            'machinery': 6000,
            'pesticides': 3000,
            'other': 2000
        }
    
    # Add fertilizer cost
    costs['fertilizer'] = fertilizer_cost
    
    # Calculate total investment per hectare
    total_investment = sum(costs.values()) * area_ha
    
    # Get market price
    price_per_quintal = market_prices.get(crop, 2500)  # Default price
    
    # Calculate gross revenue
    gross_revenue = predicted_yield * price_per_quintal * area_ha
    
    # Calculate net profit
    net_profit = gross_revenue - total_investment
    
    # Calculate ROI
    roi_percent = (net_profit / total_investment) * 100 if total_investment > 0 else 0
    
    return {
        'predicted_yield_quintals_per_ha': predicted_yield,
        'area_ha': area_ha,
        'total_yield_quintals': predicted_yield * area_ha,
        'price_per_quintal': price_per_quintal,
        'gross_revenue': gross_revenue,
        'cost_breakdown': costs,
        'total_investment': total_investment,
        'net_profit': net_profit,
        'roi_percent': roi_percent,
        'profit_per_ha': net_profit / area_ha if area_ha > 0 else 0
    }

def predict_profit(crop, n, p, k, ph, temperature, humidity, rainfall, 
                  fertilizer_cost, area_ha=1.0, model=None, crop_encoder=None):
    """
    Predict profit for given conditions using LightGBM model
    """
    if model is None or crop_encoder is None:
        # Fallback to average yields if model not available
        avg_yields = {
            'rice': 45, 'wheat': 35, 'maize': 55, 
            'cotton': 15, 'sugarcane': 650, 'soybean': 20
        }
        predicted_yield = avg_yields.get(crop, 30)
    else:
        # Use trained LightGBM model
        try:
            crop_encoded = crop_encoder.transform([crop])[0] if crop in crop_encoder.classes_ else 0
            X_input = np.array([[n, p, k, ph, temperature, humidity, rainfall, fertilizer_cost, crop_encoded]])
            
            # For LightGBM models, use the predict method with best_iteration
            if hasattr(model, 'best_iteration'):
                predicted_yield = model.predict(X_input, num_iteration=model.best_iteration)[0]
            else:
                # Fallback for sklearn models
                predicted_yield = model.predict(X_input)[0]
                
            predicted_yield = max(0, predicted_yield)  # Ensure non-negative
        except Exception as e:
            print(f"Yield prediction failed: {e}")
            avg_yields = {'rice': 45, 'wheat': 35, 'maize': 55, 'cotton': 15, 'sugarcane': 650, 'soybean': 20}
            predicted_yield = avg_yields.get(crop, 30)
    
    # Calculate profit
    profit_analysis = calculate_profit(crop, predicted_yield, fertilizer_cost, area_ha)
    
    return profit_analysis

def save_profit_artifacts(model, crop_encoder, metrics, feature_cols, version='v1'):
    """
    Save profit estimation artifacts
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save yield model
    if model is not None:
        model_file = os.path.join(models_dir, f'yield_model_{version}.pkl')
        joblib.dump(model, model_file)
        print(f"Yield model saved: {model_file}")
    
    # Save crop encoder
    if crop_encoder is not None:
        encoder_file = os.path.join(models_dir, f'profit_crop_encoder_{version}.pkl')
        joblib.dump(crop_encoder, encoder_file)
    
    # Save cost configuration
    cultivation_costs, market_prices = create_cost_tables()
    cost_config = {
        'cultivation_costs': cultivation_costs,
        'market_prices': market_prices,
        'version': version,
        'currency': 'INR'
    }
    
    config_file = os.path.join(models_dir, f'profit_calc_config_{version}.json')
    with open(config_file, 'w') as f:
        json.dump(cost_config, f, indent=2)
    
    # Save evaluation
    eval_data = {
        'version': version,
        'timestamp': datetime.now().isoformat(),
        'model_type': 'LightGBM_Regressor',
        'metrics': metrics,
        'feature_count': len(feature_cols),
        'crops_supported': list(cultivation_costs.keys())
    }
    
    eval_file = os.path.join(models_dir, f'profit_eval_{version}.json')
    with open(eval_file, 'w') as f:
        json.dump(eval_data, f, indent=2)
    
    print(f"Profit artifacts saved to {models_dir}")

def train_profit_system():
    """
    Main training pipeline for profit estimation system
    """
    print("=" * 50)
    print("PROFIT ESTIMATION SYSTEM TRAINING")
    print("=" * 50)
    
    # Train yield model
    print("\nTraining yield prediction model...")
    model, crop_encoder, feature_cols, metrics = train_yield_model()
    
    # Test the system
    print("\nTesting profit estimation system...")
    test_cases = [
        ('rice', 60, 45, 50, 6.5, 28, 75, 1200, 3500, 1.0),
        ('wheat', 55, 40, 45, 7.0, 22, 65, 600, 3000, 2.0),
        ('maize', 70, 35, 55, 6.8, 26, 70, 800, 3200, 1.5)
    ]
    
    for crop, n, p, k, ph, temp, hum, rain, fert_cost, area in test_cases:
        result = predict_profit(crop, n, p, k, ph, temp, hum, rain, fert_cost, area, model, crop_encoder)
        print(f"\n{crop.upper()} profit analysis ({area} ha):")
        print(f"  Expected yield: {result['predicted_yield_quintals_per_ha']:.1f} quintals/ha")
        print(f"  Gross revenue: ₹{result['gross_revenue']:,.0f}")
        print(f"  Total investment: ₹{result['total_investment']:,.0f}")
        print(f"  Net profit: ₹{result['net_profit']:,.0f}")
        print(f"  ROI: {result['roi_percent']:.1f}%")
    
    # Save artifacts
    print("\nSaving profit estimation artifacts...")
    save_profit_artifacts(model, crop_encoder, metrics, feature_cols)
    
    print("\n" + "=" * 50)
    print("PROFIT SYSTEM TRAINING COMPLETED!")
    print("=" * 50)
    
    return model, crop_encoder, metrics

if __name__ == "__main__":
    # Run profit system training
    model, crop_encoder, metrics = train_profit_system()
