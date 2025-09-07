"""
Preprocessing module for crop AI project
Implements data cleaning, encoding, and scaling as per plan.md step 3
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import yaml

# Constants for outlier clipping (as per plan.md)
RAINFALL_CLIP = [0, 5000]  # mm
TEMPERATURE_CLIP = [-10, 55]  # °C
PH_CLIP = [3.5, 9.0]  # pH units

def load_raw():
    """
    Load raw CSV files from data/raw/ directory
    Returns: dict of dataframes
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
    
    datasets = {}
    
    # Load crop recommendation data
    crop_file = os.path.join(data_dir, 'Crop_recommendation.csv')
    if os.path.exists(crop_file):
        datasets['crop'] = pd.read_csv(crop_file)
        print(f"Loaded crop data: {datasets['crop'].shape}")
    
    # Load FAO crops and livestock data
    fao_file = os.path.join(data_dir, 'Crops and livestock products.csv')
    if os.path.exists(fao_file):
        datasets['fao'] = pd.read_csv(fao_file)
        print(f"Loaded FAO data: {datasets['fao'].shape}")
    
    # Load rainfall data
    rainfall_file = os.path.join(data_dir, 'Sub Divisional Monthly Rainfall from 1901 to 2017.csv')
    if os.path.exists(rainfall_file):
        datasets['rainfall'] = pd.read_csv(rainfall_file)
        print(f"Loaded rainfall data: {datasets['rainfall'].shape}")
    
    return datasets

def standardize_column_names(df):
    """
    Standardize column names: lowercase, underscores
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

def clean_crop_data(df):
    """
    Clean the main crop recommendation dataset
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Convert numeric columns
    numeric_cols = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Trim whitespace in categorical columns
    if 'label' in df.columns:
        df['label'] = df['label'].astype(str).str.strip().str.lower()
    
    # Apply outlier clipping
    if 'rainfall' in df.columns:
        df['rainfall'] = df['rainfall'].clip(RAINFALL_CLIP[0], RAINFALL_CLIP[1])
    
    if 'temperature' in df.columns:
        df['temperature'] = df['temperature'].clip(TEMPERATURE_CLIP[0], TEMPERATURE_CLIP[1])
    
    if 'ph' in df.columns:
        df['ph'] = df['ph'].clip(PH_CLIP[0], PH_CLIP[1])
    
    return df

def handle_missing_values(df, numeric_strategy='median'):
    """
    Handle missing values according to plan.md strategy
    """
    df = df.copy()
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Handle numeric missing values
    if len(numeric_cols) > 0:
        imputer = SimpleImputer(strategy=numeric_strategy)
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
        
        # Save imputer medians for inference
        medians = {col: imputer.statistics_[i] for i, col in enumerate(numeric_cols)}
        return df, medians
    
    # Handle categorical missing values
    for col in categorical_cols:
        df[col] = df[col].fillna('unknown')
    
    return df, {}

def create_encoders(df, target_col='label'):
    """
    Create and fit label encoders
    """
    encoders = {}
    
    # Encode target variable
    if target_col in df.columns:
        le_target = LabelEncoder()
        df[f'{target_col}_encoded'] = le_target.fit_transform(df[target_col])
        encoders[target_col] = le_target
    
    # Encode other categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != target_col and df[col].nunique() < 50:  # Only encode if reasonable number of categories
            le = LabelEncoder()
            df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    
    return df, encoders

def create_scaler(df, feature_cols=None):
    """
    Create and fit StandardScaler for numeric features
    """
    if feature_cols is None:
        feature_cols = df.select_dtypes(include=[np.number]).columns
    
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[feature_cols] = scaler.fit_transform(df[feature_cols])
    
    return df_scaled, scaler

def save_artifacts(encoders, scaler, medians, feature_list):
    """
    Save preprocessing artifacts for inference
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save encoders
    encoders_dir = os.path.join(models_dir, 'label_encoders')
    os.makedirs(encoders_dir, exist_ok=True)
    
    for name, encoder in encoders.items():
        joblib.dump(encoder, os.path.join(encoders_dir, f'{name}_encoder.pkl'))
    
    # Save scaler
    joblib.dump(scaler, os.path.join(models_dir, 'scaler_v1.pkl'))
    
    # Save numeric imputer medians
    with open(os.path.join(models_dir, 'num_imputer.json'), 'w') as f:
        json.dump(medians, f, indent=2)
    
    # Save feature list
    with open(os.path.join(models_dir, 'feature_list.yaml'), 'w') as f:
        yaml.dump({'features': feature_list}, f, default_flow_style=False)
    
    print(f"Artifacts saved to {models_dir}")

def preprocess_crop_data():
    """
    Main preprocessing pipeline for crop recommendation data
    """
    print("Starting crop data preprocessing...")
    
    # Load raw data
    datasets = load_raw()
    
    if 'crop' not in datasets:
        raise ValueError("Crop recommendation data not found!")
    
    df = datasets['crop']
    print(f"Original data shape: {df.shape}")
    
    # Clean data
    df_clean = clean_crop_data(df)
    print(f"After cleaning: {df_clean.shape}")
    
    # Handle missing values
    df_imputed, medians = handle_missing_values(df_clean)
    print(f"Missing values handled. Medians: {medians}")
    
    # Create encoders
    df_encoded, encoders = create_encoders(df_imputed)
    print(f"Encoders created for: {list(encoders.keys())}")
    
    # Define feature columns (exclude target and encoded versions)
    feature_cols = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Create scaler
    df_scaled, scaler = create_scaler(df_encoded, feature_cols)
    print("Scaler fitted")
    
    # Save artifacts
    save_artifacts(encoders, scaler, medians, feature_cols)
    
    # Save processed data
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    output_file = os.path.join(processed_dir, 'crop_data_cleaned.csv')
    df_scaled.to_csv(output_file, index=False)
    print(f"Processed data saved to: {output_file}")
    
    return df_scaled

if __name__ == "__main__":
    # Run preprocessing pipeline
    processed_data = preprocess_crop_data()
    print("Preprocessing completed successfully!")
