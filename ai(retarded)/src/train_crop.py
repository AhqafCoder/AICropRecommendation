"""
Crop recommendation model training module
Implements LightGBM classifier with cross-validation as per plan.md step 5
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import lightgbm as lgb
import joblib
import yaml
from datetime import datetime

# Import our modules
import sys
sys.path.append(os.path.dirname(__file__))
from preprocess import preprocess_crop_data
from features import engineer_features, get_feature_list, save_feature_list

def load_processed_data():
    """
    Load processed and feature-engineered data
    """
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    
    # Try to load feature-engineered data first
    features_file = os.path.join(processed_dir, 'crop_data_features.csv')
    if os.path.exists(features_file):
        df = pd.read_csv(features_file)
        print(f"Loaded feature-engineered data: {df.shape}")
        return df
    
    # Fallback to cleaned data
    cleaned_file = os.path.join(processed_dir, 'crop_data_cleaned.csv')
    if os.path.exists(cleaned_file):
        df = pd.read_csv(cleaned_file)
        print(f"Loaded cleaned data: {df.shape}")
        # Apply feature engineering
        df = engineer_features(df)
        return df
    
    # If no processed data, run preprocessing
    print("No processed data found. Running preprocessing...")
    df = preprocess_crop_data()
    df = engineer_features(df)
    return df

def prepare_training_data(df, target_col='label_encoded'):
    """
    Prepare features and target for training
    """
    # Get feature columns
    feature_cols = get_feature_list(df, exclude_target=True)
    
    # Prepare features and target
    X = df[feature_cols]
    y = df[target_col] if target_col in df.columns else df['label']
    
    print(f"Features: {len(feature_cols)}")
    print(f"Samples: {len(X)}")
    print(f"Classes: {len(np.unique(y))}")
    
    return X, y, feature_cols

def train_lightgbm_model(X, y, params=None):
    """
    Train LightGBM classifier with specified parameters
    """
    if params is None:
        params = {
            'objective': 'multiclass',
            'num_class': len(np.unique(y)),
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': 0,
            'random_state': 42
        }
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    # Train model with early stopping
    model = lgb.train(
        params,
        train_data,
        valid_sets=[train_data, valid_data],
        valid_names=['train', 'eval'],
        num_boost_round=500,
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100)
        ]
    )
    
    return model, X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test, class_names=None):
    """
    Evaluate model performance and generate metrics
    """
    # Predictions
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    y_pred_class = np.argmax(y_pred, axis=1)
    
    # Basic metrics
    accuracy = accuracy_score(y_test, y_pred_class)
    f1_macro = f1_score(y_test, y_pred_class, average='macro')
    
    # Top-3 accuracy
    top3_pred = np.argsort(y_pred, axis=1)[:, -3:]
    top3_accuracy = np.mean([y_test.iloc[i] in top3_pred[i] for i in range(len(y_test))])
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred_class)
    
    # Classification report
    report = classification_report(y_test, y_pred_class, output_dict=True)
    
    metrics = {
        'accuracy': float(accuracy),
        'f1_macro': float(f1_macro),
        'top3_accuracy': float(top3_accuracy),
        'confusion_matrix': cm.tolist(),
        'classification_report': report,
        'feature_importance': dict(zip(
            model.feature_name(),
            model.feature_importance().tolist()
        ))
    }
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-macro: {f1_macro:.4f}")
    print(f"Top-3 Accuracy: {top3_accuracy:.4f}")
    
    return metrics

def cross_validate_model(X, y, params=None, cv_folds=5):
    """
    Perform stratified k-fold cross-validation
    """
    if params is None:
        params = {
            'objective': 'multiclass',
            'num_class': len(np.unique(y)),
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1,
            'random_state': 42
        }
    
    # Create LightGBM classifier for sklearn compatibility
    lgb_clf = lgb.LGBMClassifier(**params, n_estimators=500, early_stopping_rounds=50)
    
    # Stratified K-Fold
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    
    # Cross-validation scores
    cv_scores = cross_val_score(lgb_clf, X, y, cv=skf, scoring='accuracy')
    
    cv_results = {
        'cv_scores': cv_scores.tolist(),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'cv_folds': cv_folds
    }
    
    print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return cv_results

def save_model_artifacts(model, metrics, cv_results, feature_cols, version='v1'):
    """
    Save model and evaluation artifacts
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_file = os.path.join(models_dir, f'crop_model_{version}.pkl')
    joblib.dump(model, model_file)
    
    # Save evaluation metrics
    eval_data = {
        'version': version,
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics,
        'cross_validation': cv_results,
        'feature_count': len(feature_cols),
        'model_type': 'LightGBM'
    }
    
    eval_file = os.path.join(models_dir, f'crop_eval_{version}.json')
    with open(eval_file, 'w') as f:
        json.dump(eval_data, f, indent=2)
    
    # Save feature list
    save_feature_list(feature_cols, version)
    
    print(f"Model artifacts saved:")
    print(f"  - Model: {model_file}")
    print(f"  - Evaluation: {eval_file}")
    
    return model_file, eval_file

def train_crop_model():
    """
    Main training pipeline for crop recommendation model
    """
    print("=" * 50)
    print("CROP RECOMMENDATION MODEL TRAINING")
    print("=" * 50)
    
    # Load data
    df = load_processed_data()
    
    # Prepare training data
    X, y, feature_cols = prepare_training_data(df)
    
    # Cross-validation
    print("\nPerforming cross-validation...")
    cv_results = cross_validate_model(X, y)
    
    # Train final model
    print("\nTraining final model...")
    model, X_train, X_test, y_train, y_test = train_lightgbm_model(X, y)
    
    # Evaluate model
    print("\nEvaluating model...")
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save artifacts
    print("\nSaving model artifacts...")
    model_file, eval_file = save_model_artifacts(model, metrics, cv_results, feature_cols)
    
    print("\n" + "=" * 50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    return model, metrics, cv_results

if __name__ == "__main__":
    # Run training pipeline
    model, metrics, cv_results = train_crop_model()
