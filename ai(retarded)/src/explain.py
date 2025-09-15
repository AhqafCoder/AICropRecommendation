"""
SHAP explainability module for crop AI project
Implements human-friendly explanations for all model predictions as per plan.md step 8
"""

import pandas as pd
import numpy as np
import os
import joblib
import shap
from typing import Dict, List, Tuple, Any

def load_model_artifacts():
    """
    Load trained models and preprocessing artifacts
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
    artifacts = {}
    
    # Load crop model
    crop_model_file = os.path.join(models_dir, 'crop_model_v1.pkl')
    if os.path.exists(crop_model_file):
        artifacts['crop_model'] = joblib.load(crop_model_file)
    
    # Load scaler
    scaler_file = os.path.join(models_dir, 'scaler_v1.pkl')
    if os.path.exists(scaler_file):
        artifacts['scaler'] = joblib.load(scaler_file)
    
    # Load label encoders
    encoders_dir = os.path.join(models_dir, 'label_encoders')
    if os.path.exists(encoders_dir):
        artifacts['encoders'] = {}
        for file in os.listdir(encoders_dir):
            if file.endswith('_encoder.pkl'):
                name = file.replace('_encoder.pkl', '')
                artifacts['encoders'][name] = joblib.load(os.path.join(encoders_dir, file))
    
    return artifacts

def create_shap_explainer(model, background_data=None):
    """
    Create SHAP explainer for tree-based models
    """
    try:
        # For LightGBM/XGBoost models
        explainer = shap.TreeExplainer(model)
        return explainer
    except Exception as e:
        print(f"TreeExplainer failed: {e}")
        # Fallback to KernelExplainer
        if background_data is not None:
            explainer = shap.KernelExplainer(model.predict, background_data)
            return explainer
        return None

def get_feature_contributions(explainer, X_sample, predicted_class=None):
    """
    Get SHAP values and feature contributions for a single sample
    """
    try:
        # Get SHAP values
        shap_values = explainer.shap_values(X_sample)
        
        # Handle multiclass case
        if isinstance(shap_values, list):
            if predicted_class is not None:
                shap_vals = shap_values[predicted_class]
            else:
                # Use the class with highest prediction
                shap_vals = shap_values[0]  # Default to first class
        else:
            shap_vals = shap_values
        
        # If single sample, extract the values
        if len(shap_vals.shape) > 1:
            shap_vals = shap_vals[0]
        
        return shap_vals
    
    except Exception as e:
        print(f"SHAP calculation failed: {e}")
        return None

def map_feature_to_explanation(feature_name: str, feature_value: float, shap_value: float) -> str:
    """
    Map numeric feature contribution to human-readable explanation
    """
    impact = "increases" if shap_value > 0 else "decreases"
    
    # Feature-specific explanations
    if feature_name == 'rainfall':
        if feature_value > 1000:
            return f"High rainfall ({feature_value:.0f} mm) {impact} suitability for water-loving crops"
        elif feature_value < 300:
            return f"Low rainfall ({feature_value:.0f} mm) {impact} crop viability; consider drought-resistant varieties"
        else:
            return f"Moderate rainfall ({feature_value:.0f} mm) {impact} crop recommendation"
    
    elif feature_name == 'temperature':
        if feature_value > 35:
            return f"High temperature ({feature_value:.1f}°C) {impact} heat-sensitive crop suitability"
        elif feature_value < 15:
            return f"Low temperature ({feature_value:.1f}°C) {impact} cold-sensitive crop growth"
        else:
            return f"Optimal temperature ({feature_value:.1f}°C) {impact} crop selection"
    
    elif feature_name == 'humidity':
        if feature_value > 85:
            return f"High humidity ({feature_value:.0f}%) {impact} disease-prone crop recommendations"
        elif feature_value < 40:
            return f"Low humidity ({feature_value:.0f}%) {impact} moisture-dependent crop viability"
        else:
            return f"Moderate humidity ({feature_value:.0f}%) {impact} crop suitability"
    
    elif feature_name == 'ph':
        if feature_value < 6.0:
            return f"Acidic soil (pH {feature_value:.1f}) {impact} acid-tolerant crop preference"
        elif feature_value > 7.5:
            return f"Alkaline soil (pH {feature_value:.1f}) {impact} alkali-tolerant crop selection"
        else:
            return f"Neutral soil (pH {feature_value:.1f}) {impact} most crop varieties"
    
    elif feature_name == 'n':
        if feature_value < 40:
            return f"Low Nitrogen ({feature_value:.0f}) {impact} leafy crop growth; consider urea application"
        elif feature_value > 80:
            return f"High Nitrogen ({feature_value:.0f}) {impact} nitrogen-loving crop recommendations"
        else:
            return f"Moderate Nitrogen ({feature_value:.0f}) {impact} balanced crop nutrition"
    
    elif feature_name == 'p':
        if feature_value < 30:
            return f"Low Phosphorus ({feature_value:.0f}) {impact} root development; consider DAP fertilizer"
        elif feature_value > 70:
            return f"High Phosphorus ({feature_value:.0f}) {impact} phosphorus-efficient crop selection"
        else:
            return f"Adequate Phosphorus ({feature_value:.0f}) {impact} crop root health"
    
    elif feature_name == 'k':
        if feature_value < 35:
            return f"Low Potassium ({feature_value:.0f}) {impact} fruit quality; consider MOP application"
        elif feature_value > 75:
            return f"High Potassium ({feature_value:.0f}) {impact} potassium-loving crop preference"
        else:
            return f"Balanced Potassium ({feature_value:.0f}) {impact} overall plant health"
    
    # Engineered features
    elif feature_name == 'npk_balance':
        if shap_value > 0:
            return f"Good NPK balance {impact} nutrient-efficient crop selection"
        else:
            return f"NPK imbalance {impact} crop performance; adjust fertilizer ratios"
    
    elif feature_name == 'soil_fertility_index':
        if feature_value > 0.8:
            return f"High soil fertility {impact} premium crop varieties"
        elif feature_value < 0.5:
            return f"Low soil fertility {impact} hardy crop selection"
        else:
            return f"Moderate soil fertility {impact} standard crop recommendations"
    
    elif 'stress' in feature_name:
        if feature_value > 0:
            return f"Environmental stress detected {impact} stress-resistant crop preference"
        else:
            return f"Favorable conditions {impact} diverse crop options"
    
    # Default explanation
    return f"{feature_name.replace('_', ' ').title()} ({feature_value:.1f}) {impact} crop recommendation"

def generate_rule_based_explanation(X_sample, feature_names, top_n=3):
    """
    Generate rule-based explanation when SHAP is unavailable
    """
    try:
        # Extract feature values
        if len(X_sample.shape) > 1:
            values = X_sample[0]
        else:
            values = X_sample
        
        # Create feature-value pairs
        feature_dict = dict(zip(feature_names, values))
        
        explanations = []
        
        # Analyze key features with agricultural rules
        if 'rainfall' in feature_dict:
            rainfall = feature_dict['rainfall']
            if rainfall > 1000:
                explanations.append(f"High rainfall ({rainfall:.0f} mm) favors water-loving crops like rice")
            elif rainfall < 300:
                explanations.append(f"Low rainfall ({rainfall:.0f} mm) suggests drought-resistant crops like millet")
            else:
                explanations.append(f"Moderate rainfall ({rainfall:.0f} mm) supports diverse crop options")
        
        if 'temperature' in feature_dict:
            temp = feature_dict['temperature']
            if temp > 35:
                explanations.append(f"High temperature ({temp:.1f}°C) limits heat-sensitive crops")
            elif temp < 15:
                explanations.append(f"Cool temperature ({temp:.1f}°C) favors temperate crops")
            else:
                explanations.append(f"Optimal temperature ({temp:.1f}°C) supports most crop varieties")
        
        if 'ph' in feature_dict:
            ph = feature_dict['ph']
            if ph < 6.0:
                explanations.append(f"Acidic soil (pH {ph:.1f}) suits acid-tolerant crops")
            elif ph > 7.5:
                explanations.append(f"Alkaline soil (pH {ph:.1f}) requires alkali-tolerant varieties")
            else:
                explanations.append(f"Neutral soil (pH {ph:.1f}) supports most crop types")
        
        # NPK analysis
        if all(nutrient in feature_dict for nutrient in ['n', 'p', 'k']):
            n, p, k = feature_dict['n'], feature_dict['p'], feature_dict['k']
            if n < 40:
                explanations.append(f"Low Nitrogen ({n:.0f}) may limit leafy crop growth")
            if p < 30:
                explanations.append(f"Low Phosphorus ({p:.0f}) affects root development")
            if k < 35:
                explanations.append(f"Low Potassium ({k:.0f}) impacts fruit quality")
        
        # Return top explanations
        return explanations[:top_n] if explanations else ["Analysis based on agricultural best practices"]
        
    except Exception as e:
        return [f"Rule-based analysis: {str(e)[:50]}..."]

def explain_crop_prediction(model, X_sample, feature_names, predicted_class=None, top_n=3):
    """
    Generate human-friendly explanation for crop prediction
    """
    try:
        # Check if model is None (not trained yet)
        if model is None:
            return generate_rule_based_explanation(X_sample, feature_names, top_n)
        
        # Create explainer
        explainer = create_shap_explainer(model)
        if explainer is None:
            return generate_rule_based_explanation(X_sample, feature_names, top_n)
        
        # Get SHAP values
        shap_vals = get_feature_contributions(explainer, X_sample, predicted_class)
        if shap_vals is None:
            return generate_rule_based_explanation(X_sample, feature_names, top_n)
        
        # Create feature contributions list
        contributions = []
        for i, (feature, shap_val) in enumerate(zip(feature_names, shap_vals)):
            feature_val = X_sample[0][i] if len(X_sample.shape) > 1 else X_sample[i]
            contributions.append({
                'feature': feature,
                'value': feature_val,
                'shap': abs(shap_val),
                'impact': shap_val
            })
        
        # Sort by absolute SHAP value and take top N
        contributions.sort(key=lambda x: x['shap'], reverse=True)
        top_contributions = contributions[:top_n]
        
        # Generate explanations
        explanations = []
        for contrib in top_contributions:
            explanation = map_feature_to_explanation(
                contrib['feature'], 
                contrib['value'], 
                contrib['impact']
            )
            explanations.append(explanation)
        
        # Add generic caution
        explanations.append("This recommendation is based on available data; consult local agronomist for final decisions")
        
        return explanations
    
    except Exception as e:
        print(f"Explanation generation failed: {e}")
        return [f"Explanation error: {str(e)}"]

def explain_prediction(model_type: str, model, X_sample, feature_names, **kwargs):
    """
    Universal explanation function for different model types
    """
    if model_type == 'crop':
        return explain_crop_prediction(model, X_sample, feature_names, **kwargs)
    
    elif model_type == 'fertilizer':
        # Simplified explanation for fertilizer (rule-based)
        return [
            "Fertilizer recommendation based on soil nutrient analysis",
            "NPK ratios optimized for selected crop type",
            "Dosage calculated per hectare based on deficiency levels"
        ]
    
    elif model_type == 'profit':
        # Simplified explanation for profit estimation
        return [
            "Profit estimation based on predicted yield and market prices",
            "Costs include seeds, labor, fertilizer, and operational expenses",
            "ROI calculated as net profit percentage of total investment"
        ]
    
    else:
        return ["Explanation not available for this model type"]

def create_explanation_summary(crop_explanation, fertilizer_info, profit_info):
    """
    Create comprehensive explanation combining all three models
    """
    summary = {
        'crop_reasoning': crop_explanation,
        'fertilizer_rationale': [
            f"Recommended: {fertilizer_info.get('fertilizer', 'N/A')}",
            f"Dosage: {fertilizer_info.get('dosage_kg_per_ha', 0)} kg/ha",
            f"Estimated cost: ₹{fertilizer_info.get('total_cost', 0):,.0f}"
        ],
        'profit_factors': [
            f"Expected yield: {profit_info.get('predicted_yield_quintals_per_ha', 0):.1f} quintals/ha",
            f"Market price: ₹{profit_info.get('price_per_quintal', 0):,.0f}/quintal",
            f"ROI: {profit_info.get('roi_percent', 0):.1f}%"
        ],
        'overall_recommendation': "Comprehensive analysis suggests this crop choice balances yield potential, input costs, and market profitability"
    }
    
    return summary

def save_explanation_plots(shap_values, feature_names, output_dir=None):
    """
    Save SHAP explanation plots (optional for debugging)
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'explain_plots')
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        import matplotlib.pyplot as plt
        
        # Create summary plot
        shap.summary_plot(shap_values, feature_names=feature_names, show=False)
        plt.savefig(os.path.join(output_dir, 'shap_summary.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"SHAP plots saved to {output_dir}")
        
    except Exception as e:
        print(f"Plot saving failed: {e}")

# Example usage function
def test_explanation_system():
    """
    Test the explanation system with sample data
    """
    print("Testing SHAP explanation system...")
    
    # Sample input
    sample_input = np.array([[60, 45, 50, 6.5, 25, 70, 800]])
    feature_names = ['n', 'p', 'k', 'ph', 'temperature', 'humidity', 'rainfall']
    
    # Mock model for testing
    class MockModel:
        def predict(self, X):
            return np.array([0.8, 0.1, 0.1])  # Mock probabilities
    
    mock_model = MockModel()
    
    # Generate explanation
    explanations = explain_crop_prediction(mock_model, sample_input, feature_names)
    
    print("Generated explanations:")
    for i, exp in enumerate(explanations, 1):
        print(f"{i}. {exp}")
    
    return explanations

if __name__ == "__main__":
    # Test the explanation system
    test_explanation_system()
