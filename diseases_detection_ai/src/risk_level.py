"""
Risk Level Assessment for Crop Disease Detection
Calculates risk levels based on prediction confidence and disease severity
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class RiskLevelCalculator:
    """Calculate risk levels for crop disease predictions"""
    
    def __init__(self, knowledge_base_path='knowledge_base/disease_info.json'):
        """
        Initialize risk calculator
        
        Args:
            knowledge_base_path: Path to disease knowledge base
        """
        self.knowledge_base_path = knowledge_base_path
        self.disease_info = self._load_disease_info()
        
        # Disease severity mapping (based on agricultural impact)
        self.disease_severity = {
            # Corn diseases
            'Corn___Cercospora_leaf_spot_Gray_leaf_spot': 'medium',
            'Corn___Common_rust': 'medium',
            'Corn___Northern_Leaf_Blight': 'high',
            'Corn___healthy': 'none',
            
            # Potato diseases
            'Potato___Early_Blight': 'medium',
            'Potato___Late_Blight': 'high',  # Most destructive
            'Potato___healthy': 'none',
            
            # Tomato diseases
            'Tomato___Bacterial_spot': 'medium',
            'Tomato___Early_blight': 'medium',
            'Tomato___Late_blight': 'high',  # Very destructive
            'Tomato___Leaf_Mold': 'low',
            'Tomato___Septoria_leaf_spot': 'medium',
            'Tomato___Spider_mites_Two_spotted_spider_mite': 'medium',
            'Tomato___Target_Spot': 'medium',
            'Tomato___Tomato_mosaic_virus': 'high',  # Viral, no cure
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'high',  # Viral, devastating
            'Tomato___healthy': 'none'
        }
        
        # Risk level thresholds
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.5,
            'low': 0.0
        }
    
    def _load_disease_info(self):
        """Load disease information from knowledge base"""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                data = json.load(f)
            return {f"{d['crop']}___{d['disease']}": d for d in data['diseases']}
        except FileNotFoundError:
            print(f"Warning: Knowledge base not found at {self.knowledge_base_path}")
            return {}
    
    def calculate_base_risk(self, predicted_class: str, confidence: float) -> str:
        """
        Calculate base risk level using confidence and disease severity
        
        Args:
            predicted_class: Predicted disease class
            confidence: Model confidence (0-1)
            
        Returns:
            risk_level: 'Low', 'Medium', or 'High'
        """
        # Handle healthy cases
        if 'healthy' in predicted_class.lower():
            return 'Low'
        
        # Get disease severity
        disease_severity = self.disease_severity.get(predicted_class, 'medium')
        
        # Calculate risk based on confidence and severity
        if confidence >= self.confidence_thresholds['high']:
            # High confidence predictions
            if disease_severity == 'high':
                return 'High'
            elif disease_severity == 'medium':
                return 'Medium'
            else:
                return 'Low'
        
        elif confidence >= self.confidence_thresholds['medium']:
            # Medium confidence predictions
            if disease_severity == 'high':
                return 'High'
            elif disease_severity == 'medium':
                return 'Medium'
            else:
                return 'Low'
        
        else:
            # Low confidence predictions
            if disease_severity == 'high':
                return 'Medium'
            else:
                return 'Low'
    
    def calculate_enhanced_risk(self, predicted_class: str, confidence: float,
                              weather_data: Optional[Dict] = None,
                              growth_stage: Optional[str] = None) -> Dict:
        """
        Calculate enhanced risk level with environmental factors
        
        Args:
            predicted_class: Predicted disease class
            confidence: Model confidence (0-1)
            weather_data: Optional weather information
            growth_stage: Optional crop growth stage
            
        Returns:
            risk_assessment: Detailed risk assessment
        """
        # Base risk calculation
        base_risk = self.calculate_base_risk(predicted_class, confidence)
        
        # Initialize risk factors
        risk_factors = []
        risk_multiplier = 1.0
        
        # Weather-based risk adjustment
        if weather_data:
            weather_risk, weather_factors = self._assess_weather_risk(
                predicted_class, weather_data
            )
            risk_factors.extend(weather_factors)
            risk_multiplier *= weather_risk
        
        # Growth stage risk adjustment
        if growth_stage:
            stage_risk, stage_factors = self._assess_growth_stage_risk(
                predicted_class, growth_stage
            )
            risk_factors.extend(stage_factors)
            risk_multiplier *= stage_risk
        
        # Calculate final risk level
        final_risk = self._adjust_risk_level(base_risk, risk_multiplier)
        
        return {
            'risk_level': final_risk,
            'base_risk': base_risk,
            'confidence': confidence,
            'disease_severity': self.disease_severity.get(predicted_class, 'unknown'),
            'risk_factors': risk_factors,
            'risk_multiplier': risk_multiplier,
            'assessment_timestamp': datetime.now().isoformat(),
            'recommendations': self._get_risk_recommendations(final_risk, predicted_class)
        }
    
    def _assess_weather_risk(self, predicted_class: str, weather_data: Dict) -> Tuple[float, List[str]]:
        """Assess weather-based risk factors"""
        risk_multiplier = 1.0
        factors = []
        
        humidity = weather_data.get('humidity', 50)
        temperature = weather_data.get('temperature', 25)
        rainfall = weather_data.get('rainfall', 0)
        
        # Disease-specific weather risk
        if 'Late_Blight' in predicted_class or 'Late_blight' in predicted_class:
            # Late blight thrives in cool, humid conditions
            if humidity > 80 and temperature < 20:
                risk_multiplier *= 1.5
                factors.append("High humidity and cool temperature favor late blight")
            if rainfall > 10:
                risk_multiplier *= 1.3
                factors.append("Recent rainfall increases late blight risk")
        
        elif 'rust' in predicted_class.lower():
            # Rust diseases favor cool, humid conditions
            if humidity > 70 and 15 < temperature < 25:
                risk_multiplier *= 1.4
                factors.append("Cool, humid conditions favor rust development")
        
        elif 'Early_Blight' in predicted_class or 'Early_blight' in predicted_class:
            # Early blight thrives in warm, humid conditions
            if humidity > 75 and temperature > 25:
                risk_multiplier *= 1.4
                factors.append("Warm, humid conditions favor early blight")
        
        elif 'Spider_mites' in predicted_class:
            # Spider mites thrive in hot, dry conditions
            if humidity < 40 and temperature > 30:
                risk_multiplier *= 1.6
                factors.append("Hot, dry conditions favor spider mite infestations")
        
        return risk_multiplier, factors
    
    def _assess_growth_stage_risk(self, predicted_class: str, growth_stage: str) -> Tuple[float, List[str]]:
        """Assess growth stage-based risk factors"""
        risk_multiplier = 1.0
        factors = []
        
        # Critical growth stages for different diseases
        if growth_stage.lower() in ['flowering', 'fruit_development']:
            if 'Late_Blight' in predicted_class or 'Late_blight' in predicted_class:
                risk_multiplier *= 1.3
                factors.append("Late blight is particularly damaging during flowering/fruiting")
            
            elif 'virus' in predicted_class.lower():
                risk_multiplier *= 1.4
                factors.append("Viral infections during flowering severely impact yield")
        
        elif growth_stage.lower() in ['seedling', 'early_vegetative']:
            risk_multiplier *= 1.2
            factors.append("Young plants are more vulnerable to disease damage")
        
        return risk_multiplier, factors
    
    def _adjust_risk_level(self, base_risk: str, multiplier: float) -> str:
        """Adjust risk level based on multiplier"""
        risk_levels = ['Low', 'Medium', 'High']
        current_index = risk_levels.index(base_risk)
        
        if multiplier >= 1.5:
            # Increase risk level
            new_index = min(current_index + 1, len(risk_levels) - 1)
        elif multiplier <= 0.7:
            # Decrease risk level
            new_index = max(current_index - 1, 0)
        else:
            new_index = current_index
        
        return risk_levels[new_index]
    
    def _get_risk_recommendations(self, risk_level: str, predicted_class: str) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = []
        
        if risk_level == 'High':
            recommendations.extend([
                "🚨 IMMEDIATE ACTION REQUIRED",
                "Apply appropriate treatment immediately",
                "Monitor field daily for disease spread",
                "Consider emergency harvest if disease is severe",
                "Consult agricultural extension services"
            ])
        
        elif risk_level == 'Medium':
            recommendations.extend([
                "⚠️ MONITOR CLOSELY",
                "Apply preventive treatments",
                "Increase monitoring frequency",
                "Prepare for potential treatment application",
                "Check weather forecasts for favorable disease conditions"
            ])
        
        else:  # Low risk
            recommendations.extend([
                "✅ CONTINUE MONITORING",
                "Maintain regular field inspections",
                "Follow standard preventive practices",
                "Keep treatment options ready"
            ])
        
        # Add disease-specific recommendations
        if 'healthy' not in predicted_class.lower():
            disease_info = self.disease_info.get(predicted_class, {})
            if 'solutions' in disease_info:
                recommendations.extend(disease_info['solutions'][:3])  # Top 3 solutions
        
        return recommendations
    
    def get_risk_summary(self, predictions: List[Dict]) -> Dict:
        """
        Generate risk summary for multiple predictions
        
        Args:
            predictions: List of prediction dictionaries
            
        Returns:
            summary: Risk summary across all predictions
        """
        if not predictions:
            return {'overall_risk': 'Low', 'total_predictions': 0}
        
        risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        total_confidence = 0
        diseases_detected = []
        
        for pred in predictions:
            risk_level = pred.get('risk_level', 'Low')
            risk_counts[risk_level] += 1
            total_confidence += pred.get('confidence', 0)
            
            if 'healthy' not in pred.get('predicted_class', '').lower():
                diseases_detected.append(pred.get('predicted_class', ''))
        
        # Determine overall risk
        if risk_counts['High'] > 0:
            overall_risk = 'High'
        elif risk_counts['Medium'] > 0:
            overall_risk = 'Medium'
        else:
            overall_risk = 'Low'
        
        return {
            'overall_risk': overall_risk,
            'risk_distribution': risk_counts,
            'total_predictions': len(predictions),
            'average_confidence': total_confidence / len(predictions),
            'diseases_detected': len(set(diseases_detected)),
            'unique_diseases': list(set(diseases_detected)),
            'assessment_timestamp': datetime.now().isoformat()
        }

def test_risk_calculator():
    """Test risk level calculator"""
    print("🎯 Testing Risk Level Calculator...")
    
    calculator = RiskLevelCalculator()
    
    # Test cases
    test_cases = [
        ('Potato___Late_Blight', 0.95),
        ('Tomato___healthy', 0.88),
        ('Corn___Northern_Leaf_Blight', 0.65),
        ('Tomato___Spider_mites_Two_spotted_spider_mite', 0.45)
    ]
    
    print("\n📊 Risk Assessment Results:")
    print("-" * 60)
    
    for disease, confidence in test_cases:
        # Basic risk assessment
        basic_risk = calculator.calculate_base_risk(disease, confidence)
        
        # Enhanced risk assessment with weather
        weather_data = {
            'humidity': 85,
            'temperature': 18,
            'rainfall': 15
        }
        
        enhanced_risk = calculator.calculate_enhanced_risk(
            disease, confidence, weather_data, 'flowering'
        )
        
        print(f"Disease: {disease}")
        print(f"Confidence: {confidence:.1%}")
        print(f"Basic Risk: {basic_risk}")
        print(f"Enhanced Risk: {enhanced_risk['risk_level']}")
        print(f"Risk Factors: {len(enhanced_risk['risk_factors'])}")
        print("-" * 60)
    
    print("✅ Risk Level Calculator tested successfully!")
    return True

if __name__ == "__main__":
    test_risk_calculator()
