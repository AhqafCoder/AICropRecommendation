"""
Enhanced model explainability module for crop AI project
Provides detailed explanations using SHAP for model interpretability
"""

import pandas as pd
import numpy as np
import os
import joblib
import shap
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

def explain_prediction(model_type, model, X, feature_names, prediction_index=None, **kwargs):
    """
    Generate detailed explanations for model predictions using SHAP
    """
    try:
        if model_type == 'crop' and hasattr(model, 'predict'):
            return explain_crop_prediction_shap(model, X, feature_names, prediction_index)
        elif model_type == 'fertilizer':
            return explain_fertilizer_prediction(X, feature_names)
        elif model_type == 'profit':
            return explain_profit_prediction_enhanced(model, X, feature_names)
        else:
            return explain_fallback(model_type, X, feature_names)
    except Exception as e:
        print(f"SHAP explanation failed: {e}")
        return explain_fallback(model_type, X, feature_names)

def explain_crop_prediction_shap(model, X, feature_names, prediction_index=None):
    """
    Explain crop prediction using SHAP values for better interpretability
    """
    try:
        # Convert input to DataFrame for better handling
        if not isinstance(X, pd.DataFrame):
            X_df = pd.DataFrame(X, columns=feature_names)
        else:
            X_df = X.copy()
        
        # Create SHAP explainer
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_df)
        
        explanations = []
        
        # If prediction_index is provided, use that class
        if prediction_index is not None and len(shap_values) > prediction_index:
            class_shap_values = shap_values[prediction_index][0]
        else:
            # Use the predicted class
            prediction = model.predict(X_df)[0]
            predicted_class_idx = model.classes_.tolist().index(prediction) if hasattr(model, 'classes_') else 0
            class_shap_values = shap_values[predicted_class_idx][0] if len(shap_values) > predicted_class_idx else shap_values[0][0]
        
        # Get feature contributions
        feature_contributions = list(zip(feature_names, class_shap_values, X_df.iloc[0].values))
        feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
        
        # Generate explanations based on SHAP values
        for i, (feature, shap_val, actual_val) in enumerate(feature_contributions[:4]):
            if abs(shap_val) > 0.01:  # Only include meaningful contributions
                direction = "positively" if shap_val > 0 else "negatively"
                explanations.append(
                    f"{feature.title()} ({actual_val:.1f}) contributes {direction} "
                    f"(impact: {abs(shap_val):.3f}) to the recommendation"
                )
        
        if not explanations:
            explanations = explain_crop_prediction_fallback(model, X_df, feature_names)
        
        return explanations[:4]
        
    except Exception as e:
        print(f"SHAP crop explanation failed: {e}")
        return explain_crop_prediction_fallback(model, X, feature_names)

def explain_crop_prediction_fallback(model, X, feature_names):
    """
    Fallback explanation using feature importance when SHAP fails
    """
    try:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            input_values = X.iloc[0].values if isinstance(X, pd.DataFrame) else (X[0] if len(X.shape) > 1 else X)
            
            feature_impact = list(zip(feature_names, importances, input_values))
            feature_impact.sort(key=lambda x: x[1], reverse=True)
            
            explanations = []
            for i, (name, imp, val) in enumerate(feature_impact[:3]):
                if i == 0:
                    explanations.append(f"Primary factor: {name.title()} level ({val:.1f}) - high influence on crop selection")
                elif i == 1:
                    explanations.append(f"Secondary factor: {name.title()} ({val:.1f}) - moderate influence on suitability")
                else:
                    explanations.append(f"Supporting factor: {name.title()} ({val:.1f}) - contributes to final recommendation")
            
            return explanations
    except Exception as e:
        pass
    
    return [
        "Crop recommendation based on soil nutrient analysis",
        "Climate conditions evaluated for optimal growth",
        "Agricultural best practices applied to selection"
    ]

def explain_fertilizer_prediction(X, feature_names):
    """
    Explain fertilizer recommendation based on soil conditions
    """
    try:
        input_values = X[0] if len(X.shape) > 1 else X
        explanations = []
        
        # Map common feature positions (assuming standard order)
        # N, P, K, pH are typically first 4 features
        if len(input_values) >= 4:
            n, p, k, ph = input_values[0], input_values[1], input_values[2], input_values[3]
            
            # NPK analysis
            if n < 40:
                explanations.append("Low nitrogen levels require nitrogen-rich fertilizer")
            elif n > 120:
                explanations.append("High nitrogen levels - reduced nitrogen fertilizer needed")
            
            if p < 25:
                explanations.append("Phosphorus deficiency detected - phosphate fertilizer recommended")
            elif p > 80:
                explanations.append("Adequate phosphorus levels - minimal phosphate needed")
            
            if k < 30:
                explanations.append("Potassium deficiency requires potash supplementation")
            elif k > 100:
                explanations.append("Sufficient potassium levels - reduced potash application")
        
        if not explanations:
            explanations = [
                "Fertilizer recommendation based on soil nutrient analysis",
                "Balanced NPK application suggested for optimal growth",
                "Application rates adjusted for soil conditions"
            ]
        
        return explanations[:4]
        
    except Exception as e:
        return [
            "Fertilizer recommendation calculated from soil test results",
            "Nutrient requirements balanced for crop needs",
            "Application timing and method important for effectiveness"
        ]

def explain_profit_prediction_enhanced(model, X, feature_names):
    """
    Enhanced profit/yield prediction explanation using SHAP if available
    """
    try:
        if hasattr(model, 'predict') and hasattr(model, '__class__'):
            # Try SHAP explanation for tree-based models
            X_df = pd.DataFrame(X, columns=feature_names) if not isinstance(X, pd.DataFrame) else X
            
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_df)
            
            feature_contributions = list(zip(feature_names, shap_values[0], X_df.iloc[0].values))
            feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
            
            explanations = []
            for feature, shap_val, actual_val in feature_contributions[:3]:
                if abs(shap_val) > 0.01:
                    direction = "increases" if shap_val > 0 else "decreases"
                    explanations.append(
                        f"{feature.title()} ({actual_val:.1f}) {direction} "
                        f"profit potential (impact: {abs(shap_val):.2f})"
                    )
            
            return explanations if explanations else explain_profit_prediction_fallback(X, feature_names)
            
    except Exception as e:
        print(f"SHAP profit explanation failed: {e}")
        return explain_profit_prediction_fallback(X, feature_names)

def explain_profit_prediction_fallback(X, feature_names):
    """
    Fallback profit prediction explanation
    """
    try:
        input_values = X.iloc[0].values if isinstance(X, pd.DataFrame) else (X[0] if len(X.shape) > 1 else X)
        explanations = []
        
        if len(input_values) >= 7:
            temp, humidity, rainfall = input_values[3], input_values[4], input_values[6]
            
            if 20 <= temp <= 30:
                explanations.append("Optimal temperature range supports good yields")
            elif temp < 15:
                explanations.append("Cool temperatures may reduce yield potential")
            elif temp > 35:
                explanations.append("High temperatures could stress crops and reduce yields")
                
            if 60 <= humidity <= 85:
                explanations.append("Favorable humidity levels for crop growth")
            elif humidity < 50:
                explanations.append("Low humidity may require irrigation management")
                
            if 150 <= rainfall <= 300:
                explanations.append("Adequate rainfall supports good productivity")
        
        if not explanations:
            explanations = [
                "Yield prediction based on environmental suitability",
                "Market prices and costs factored into profit calculation",
                "Weather conditions affect crop productivity"
            ]
        
        return explanations[:4]
        
    except Exception as e:
        return [
            "Profit estimate based on typical yields and market prices",
            "Environmental factors considered in productivity assessment",
            "Local market conditions may affect actual returns"
        ]

def explain_fallback(model_type, X, feature_names):
    """
    Generic fallback explanation when specific explanations fail
    """
    return [
        f"Prediction made using {model_type} model",
        "Based on provided soil and climate conditions",
        "Agricultural best practices applied to analysis",
        "Consult agricultural expert for validation"
    ]

def create_explanation_summary(crop_explanation, fertilizer_explanation, profit_explanation):
    """
    Create a comprehensive explanation summary
    """
    summary = {
        'crop_factors': crop_explanation,
        'fertilizer_rationale': fertilizer_explanation,
        'profit_drivers': profit_explanation,
        'overall_confidence': 'moderate',
        'recommendations': [
            "Verify soil test results before applying fertilizers",
            "Monitor weather conditions during growing season",
            "Consult local agricultural extension for specific guidance"
        ]
    }
    
    return summary
