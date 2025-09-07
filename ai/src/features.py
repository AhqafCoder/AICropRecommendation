"""
Feature engineering module for crop AI project
Implements domain-driven derived features as per plan.md step 4
"""

import pandas as pd
import numpy as np
import os
import yaml

def add_npk_balance(df):
    """
    Add NPK balance feature: N - (P+K)/2
    Experimentally useful for crop recommendation
    """
    if all(col in df.columns for col in ['n', 'p', 'k']):
        df['npk_balance'] = df['n'] - (df['p'] + df['k']) / 2
    return df

def add_soil_fertility_index(df):
    """
    Add soil fertility index combining pH and organic carbon if available
    For now, use pH as proxy for soil fertility
    """
    if 'ph' in df.columns:
        # Optimal pH range for most crops is 6.0-7.0
        # Create fertility index based on distance from optimal pH
        optimal_ph = 6.5
        df['soil_fertility_index'] = 1 - abs(df['ph'] - optimal_ph) / 3.5
        df['soil_fertility_index'] = df['soil_fertility_index'].clip(0, 1)
    return df

def add_temperature_features(df):
    """
    Add temperature-related features if temperature data available
    """
    if 'temperature' in df.columns:
        # Temperature stress indicators
        df['temp_stress_cold'] = (df['temperature'] < 15).astype(int)
        df['temp_stress_hot'] = (df['temperature'] > 35).astype(int)
        
        # Temperature categories
        df['temp_category'] = pd.cut(df['temperature'], 
                                   bins=[-np.inf, 15, 25, 35, np.inf],
                                   labels=['cold', 'cool', 'warm', 'hot'])
    return df

def add_humidity_features(df):
    """
    Add humidity-related features
    """
    if 'humidity' in df.columns:
        # Humidity stress indicators
        df['humidity_stress_low'] = (df['humidity'] < 40).astype(int)
        df['humidity_stress_high'] = (df['humidity'] > 90).astype(int)
        
        # Humidity categories
        df['humidity_category'] = pd.cut(df['humidity'],
                                       bins=[0, 40, 60, 80, 100],
                                       labels=['low', 'moderate', 'high', 'very_high'])
    return df

def add_rainfall_features(df):
    """
    Add rainfall-related features
    """
    if 'rainfall' in df.columns:
        # Rainfall categories based on agricultural needs
        df['rainfall_category'] = pd.cut(df['rainfall'],
                                       bins=[0, 100, 300, 600, np.inf],
                                       labels=['low', 'moderate', 'high', 'very_high'])
        
        # Drought/flood indicators
        df['drought_risk'] = (df['rainfall'] < 100).astype(int)
        df['flood_risk'] = (df['rainfall'] > 1000).astype(int)
        
        # Log transformation for skewed rainfall data
        df['rainfall_log'] = np.log1p(df['rainfall'])
    return df

def add_nutrient_ratios(df):
    """
    Add nutrient ratio features
    """
    if all(col in df.columns for col in ['n', 'p', 'k']):
        # Prevent division by zero
        df['np_ratio'] = df['n'] / (df['p'] + 0.001)
        df['nk_ratio'] = df['n'] / (df['k'] + 0.001)
        df['pk_ratio'] = df['p'] / (df['k'] + 0.001)
        
        # Total nutrient content
        df['total_npk'] = df['n'] + df['p'] + df['k']
    return df

def add_environmental_stress_index(df):
    """
    Create composite environmental stress index
    """
    stress_factors = []
    
    if 'temp_stress_cold' in df.columns:
        stress_factors.append('temp_stress_cold')
    if 'temp_stress_hot' in df.columns:
        stress_factors.append('temp_stress_hot')
    if 'humidity_stress_low' in df.columns:
        stress_factors.append('humidity_stress_low')
    if 'humidity_stress_high' in df.columns:
        stress_factors.append('humidity_stress_high')
    if 'drought_risk' in df.columns:
        stress_factors.append('drought_risk')
    if 'flood_risk' in df.columns:
        stress_factors.append('flood_risk')
    
    if stress_factors:
        df['environmental_stress_index'] = df[stress_factors].sum(axis=1)
    
    return df

def add_seasonal_features(rainfall_df=None):
    """
    Add seasonal rainfall features if monthly rainfall data available
    Currently placeholder - would need monthly rainfall data
    """
    features = {}
    
    if rainfall_df is not None:
        # This would be implemented if we had monthly rainfall data
        # rainfall_mam = March-May (pre-monsoon)
        # rainfall_jjas = June-September (monsoon)
        pass
    
    return features

def engineer_features(df, include_categorical=True):
    """
    Main feature engineering pipeline
    Apply all feature engineering functions
    """
    df = df.copy()
    
    print("Starting feature engineering...")
    original_cols = len(df.columns)
    
    # Add NPK-related features
    df = add_npk_balance(df)
    df = add_nutrient_ratios(df)
    
    # Add soil features
    df = add_soil_fertility_index(df)
    
    # Add environmental features
    df = add_temperature_features(df)
    df = add_humidity_features(df)
    df = add_rainfall_features(df)
    
    # Add composite stress index
    df = add_environmental_stress_index(df)
    
    new_cols = len(df.columns)
    print(f"Added {new_cols - original_cols} new features")
    
    # Handle categorical features encoding if requested
    if include_categorical:
        categorical_cols = df.select_dtypes(include=['category', 'object']).columns
        for col in categorical_cols:
            if col not in ['label']:  # Don't encode target variable
                df[f'{col}_encoded'] = pd.Categorical(df[col]).codes
    
    return df

def get_feature_list(df, exclude_target=True):
    """
    Get list of all features for model training
    Exclude target variables and non-numeric columns
    """
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Exclude target-related columns
    if exclude_target:
        exclude_patterns = ['label', '_encoded']
        for pattern in exclude_patterns:
            numeric_cols = [col for col in numeric_cols if pattern not in col or col.endswith('_encoded')]
    
    return numeric_cols

def save_feature_list(feature_list, version='v1'):
    """
    Save feature list to YAML file for consistency across train/predict
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    feature_config = {
        'version': version,
        'features': feature_list,
        'feature_count': len(feature_list)
    }
    
    with open(os.path.join(models_dir, 'feature_list.yaml'), 'w') as f:
        yaml.dump(feature_config, f, default_flow_style=False)
    
    print(f"Feature list saved: {len(feature_list)} features")
    return feature_config

def load_feature_list():
    """
    Load feature list from YAML file
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    feature_file = os.path.join(models_dir, 'feature_list.yaml')
    
    if os.path.exists(feature_file):
        with open(feature_file, 'r') as f:
            config = yaml.safe_load(f)
        return config['features']
    else:
        raise FileNotFoundError("Feature list not found. Run feature engineering first.")

if __name__ == "__main__":
    # Test feature engineering on processed data
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    input_file = os.path.join(processed_dir, 'crop_data_cleaned.csv')
    
    if os.path.exists(input_file):
        df = pd.read_csv(input_file)
        print(f"Loaded processed data: {df.shape}")
        
        # Apply feature engineering
        df_features = engineer_features(df)
        print(f"After feature engineering: {df_features.shape}")
        
        # Get and save feature list
        feature_list = get_feature_list(df_features)
        save_feature_list(feature_list)
        
        # Save enhanced dataset
        output_file = os.path.join(processed_dir, 'crop_data_features.csv')
        df_features.to_csv(output_file, index=False)
        print(f"Enhanced dataset saved to: {output_file}")
        
    else:
        print("Processed data not found. Run preprocessing first.")
        print("Usage: python src/preprocess.py && python src/features.py")
