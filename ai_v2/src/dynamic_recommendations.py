"""
Enhanced Dynamic ROI and Fertilizer Recommendation System
Fixes static value issues by implementing dynamic calculations based on input parameters
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

class DynamicFertilizerRecommender:
    """Dynamic fertilizer recommendation system based on crop and soil conditions"""
    
    def __init__(self):
        self.fertilizer_database = {
            'rice': {
                'base': {'type': 'NPK 20-10-10', 'base_dosage': 150, 'cost_per_kg': 25},
                'n_range': (40, 120), 'p_range': (20, 60), 'k_range': (30, 80)
            },
            'wheat': {
                'base': {'type': 'NPK 18-12-8', 'base_dosage': 120, 'cost_per_kg': 28},
                'n_range': (50, 100), 'p_range': (25, 70), 'k_range': (25, 60)
            },
            'maize': {
                'base': {'type': 'NPK 16-16-16', 'base_dosage': 140, 'cost_per_kg': 26},
                'n_range': (60, 140), 'p_range': (30, 80), 'k_range': (40, 90)
            },
            'cotton': {
                'base': {'type': 'NPK 14-14-14', 'base_dosage': 160, 'cost_per_kg': 24},
                'n_range': (70, 160), 'p_range': (35, 90), 'k_range': (50, 120)
            },
            'coffee': {
                'base': {'type': 'NPK 12-8-16', 'base_dosage': 180, 'cost_per_kg': 30},
                'n_range': (80, 140), 'p_range': (15, 40), 'k_range': (60, 140)
            },
            'banana': {
                'base': {'type': 'NPK 15-10-20', 'base_dosage': 200, 'cost_per_kg': 32},
                'n_range': (100, 180), 'p_range': (20, 50), 'k_range': (80, 160)
            }
        }
        
        # Default for unknown crops
        self.default_fertilizer = {
            'base': {'type': 'NPK 15-15-15', 'base_dosage': 130, 'cost_per_kg': 27},
            'n_range': (50, 120), 'p_range': (25, 70), 'k_range': (35, 80)
        }
    
    def calculate_nutrient_adjustment(self, soil_value, optimal_range):
        """Calculate nutrient adjustment factor based on soil levels"""
        min_val, max_val = optimal_range
        optimal_mid = (min_val + max_val) / 2
        
        if soil_value < min_val:
            # Low nutrient - increase fertilizer
            deficiency = (min_val - soil_value) / min_val
            return 1.0 + (deficiency * 0.5)  # Up to 50% increase
        elif soil_value > max_val:
            # High nutrient - decrease fertilizer
            excess = (soil_value - max_val) / max_val
            return max(0.3, 1.0 - (excess * 0.4))  # Down to 30% of base
        else:
            # Within range - minor adjustments
            deviation = abs(soil_value - optimal_mid) / optimal_mid
            return 1.0 + (deviation * 0.1)  # ±10% adjustment
    
    def predict_fertilizer_dynamic(self, crop, n, p, k, ph, **kwargs):
        """Dynamic fertilizer prediction based on crop and soil conditions"""
        
        # Get crop-specific data or default
        crop_data = self.fertilizer_database.get(crop.lower(), self.default_fertilizer)
        base_fertilizer = crop_data['base']
        
        # Calculate nutrient adjustments
        n_factor = self.calculate_nutrient_adjustment(n, crop_data['n_range'])
        p_factor = self.calculate_nutrient_adjustment(p, crop_data['p_range'])
        k_factor = self.calculate_nutrient_adjustment(k, crop_data['k_range'])
        
        # Overall adjustment factor (weighted average)
        overall_factor = (n_factor * 0.4 + p_factor * 0.3 + k_factor * 0.3)
        
        # pH adjustment
        ph_factor = 1.0
        if ph < 6.0:  # Acidic soil
            ph_factor = 1.1  # Increase fertilizer for acidic conditions
        elif ph > 7.5:  # Alkaline soil
            ph_factor = 1.05  # Slight increase for alkaline conditions
        
        # Calculate final dosage
        base_dosage = base_fertilizer['base_dosage']
        adjusted_dosage = int(base_dosage * overall_factor * ph_factor)
        
        # Ensure reasonable bounds
        adjusted_dosage = max(50, min(300, adjusted_dosage))
        
        # Calculate cost
        total_cost = int(adjusted_dosage * base_fertilizer['cost_per_kg'])
        
        # Determine fertilizer type based on soil conditions
        fertilizer_type = base_fertilizer['type']
        if n < crop_data['n_range'][0]:
            fertilizer_type = fertilizer_type.replace('NPK', 'High-N NPK')
        elif p < crop_data['p_range'][0]:
            fertilizer_type = fertilizer_type.replace('NPK', 'High-P NPK')
        elif k < crop_data['k_range'][0]:
            fertilizer_type = fertilizer_type.replace('NPK', 'High-K NPK')
        
        return {
            'fertilizer': fertilizer_type,
            'dosage_kg_per_ha': adjusted_dosage,
            'total_cost': total_cost,
            'adjustment_factors': {
                'n_factor': round(n_factor, 2),
                'p_factor': round(p_factor, 2),
                'k_factor': round(k_factor, 2),
                'ph_factor': round(ph_factor, 2),
                'overall_factor': round(overall_factor, 2)
            },
            'method': 'dynamic_calculation'
        }

class DynamicProfitCalculator:
    """Dynamic profit calculation system based on environmental and market factors"""
    
    def __init__(self):
        # Crop yield models based on environmental factors
        self.crop_models = {
            'rice': {
                'base_yield': 45,
                'temp_optimal': (20, 30),
                'humidity_optimal': (70, 90),
                'rainfall_optimal': (150, 300),
                'market_price': 2200
            },
            'wheat': {
                'base_yield': 35,
                'temp_optimal': (15, 25),
                'humidity_optimal': (50, 70),
                'rainfall_optimal': (200, 400),
                'market_price': 2100
            },
            'maize': {
                'base_yield': 55,
                'temp_optimal': (20, 30),
                'humidity_optimal': (60, 80),
                'rainfall_optimal': (300, 600),
                'market_price': 1800
            },
            'cotton': {
                'base_yield': 15,
                'temp_optimal': (25, 35),
                'humidity_optimal': (60, 80),
                'rainfall_optimal': (400, 800),
                'market_price': 5500
            },
            'coffee': {
                'base_yield': 12,
                'temp_optimal': (18, 25),
                'humidity_optimal': (60, 80),
                'rainfall_optimal': (1200, 2000),
                'market_price': 8000
            },
            'banana': {
                'base_yield': 350,
                'temp_optimal': (26, 30),
                'humidity_optimal': (75, 85),
                'rainfall_optimal': (1000, 1500),
                'market_price': 1500
            }
        }
        
        # Default cultivation costs per hectare
        self.base_costs = {
            'seeds': 3000,
            'labor': 15000,
            'irrigation': 7000,
            'machinery': 6000,
            'pesticides': 4000,
            'other': 2500
        }
    
    def calculate_environmental_factor(self, value, optimal_range):
        """Calculate yield factor based on environmental conditions"""
        min_val, max_val = optimal_range
        
        if min_val <= value <= max_val:
            # Within optimal range
            return 1.0
        elif value < min_val:
            # Below optimal
            deviation = (min_val - value) / min_val
            return max(0.3, 1.0 - deviation)
        else:
            # Above optimal
            deviation = (value - max_val) / max_val
            return max(0.3, 1.0 - (deviation * 0.5))
    
    def predict_profit_dynamic(self, crop, n, p, k, ph, temperature, humidity, rainfall, 
                             fertilizer_cost, area_ha=1.0, **kwargs):
        """Dynamic profit prediction based on all input parameters"""
        
        # Get crop-specific data or use rice as default
        crop_data = self.crop_models.get(crop.lower(), self.crop_models['rice'])
        
        # Calculate environmental factors
        temp_factor = self.calculate_environmental_factor(temperature, crop_data['temp_optimal'])
        humidity_factor = self.calculate_environmental_factor(humidity, crop_data['humidity_optimal'])
        rainfall_factor = self.calculate_environmental_factor(rainfall, crop_data['rainfall_optimal'])
        
        # Calculate soil nutrition factor
        # Optimal NPK ranges (general agriculture guidelines)
        n_factor = self.calculate_environmental_factor(n, (40, 120))
        p_factor = self.calculate_environmental_factor(p, (20, 80))
        k_factor = self.calculate_environmental_factor(k, (30, 100))
        
        # pH factor
        ph_factor = self.calculate_environmental_factor(ph, (6.0, 7.5))
        
        # Overall yield factor (weighted combination)
        yield_factor = (
            temp_factor * 0.2 +
            humidity_factor * 0.15 +
            rainfall_factor * 0.25 +
            n_factor * 0.15 +
            p_factor * 0.1 +
            k_factor * 0.1 +
            ph_factor * 0.05
        )
        
        # Add some variability based on input combinations
        interaction_bonus = 0
        if temp_factor > 0.8 and humidity_factor > 0.8:
            interaction_bonus += 0.1
        if n_factor > 0.8 and p_factor > 0.8 and k_factor > 0.8:
            interaction_bonus += 0.15
        
        yield_factor = min(1.5, yield_factor + interaction_bonus)
        
        # Calculate predicted yield
        base_yield = crop_data['base_yield']
        predicted_yield = base_yield * yield_factor
        
        # Add some randomness based on inputs (for more realistic variation)
        seed_value = int((n + p + k + temperature + humidity + ph) * 100) % 1000
        np.random.seed(seed_value)
        randomness = np.random.normal(1.0, 0.1)
        predicted_yield *= randomness
        
        # Ensure positive yield
        predicted_yield = max(5, predicted_yield)
        
        # Calculate costs
        base_cultivation_cost = sum(self.base_costs.values())
        
        # Adjust costs based on conditions
        cost_factor = 1.0
        if rainfall < 200:  # Low rainfall increases irrigation costs
            cost_factor += 0.2
        if ph < 6.0 or ph > 8.0:  # Poor pH increases amendment costs
            cost_factor += 0.1
        
        total_cultivation_cost = base_cultivation_cost * cost_factor
        total_investment = (total_cultivation_cost + fertilizer_cost) * area_ha
        
        # Calculate revenue
        market_price = crop_data['market_price']
        # Add price variation based on yield quality
        if yield_factor > 1.2:
            market_price *= 1.05  # Premium for high-quality yield
        elif yield_factor < 0.7:
            market_price *= 0.95  # Discount for lower quality
        
        gross_revenue = predicted_yield * market_price * area_ha
        
        # Calculate profit metrics
        net_profit = gross_revenue - total_investment
        roi_percent = (net_profit / total_investment * 100) if total_investment > 0 else 0
        
        return {
            'predicted_yield_quintals_per_ha': round(predicted_yield, 2),
            'gross_revenue': int(gross_revenue),
            'total_investment': int(total_investment),
            'net_profit': int(net_profit),
            'roi_percent': round(roi_percent, 1),
            'yield_factors': {
                'temperature': round(temp_factor, 2),
                'humidity': round(humidity_factor, 2),
                'rainfall': round(rainfall_factor, 2),
                'nitrogen': round(n_factor, 2),
                'phosphorus': round(p_factor, 2),
                'potassium': round(k_factor, 2),
                'ph': round(ph_factor, 2),
                'overall': round(yield_factor, 2)
            },
            'method': 'dynamic_calculation',
            'market_price_per_quintal': int(market_price)
        }

# Initialize global instances
dynamic_fertilizer = DynamicFertilizerRecommender()
dynamic_profit = DynamicProfitCalculator()

def get_dynamic_fertilizer_prediction(crop, n, p, k, ph, **kwargs):
    """Wrapper function for dynamic fertilizer prediction"""
    return dynamic_fertilizer.predict_fertilizer_dynamic(crop, n, p, k, ph, **kwargs)

def get_dynamic_profit_prediction(crop, n, p, k, ph, temperature, humidity, rainfall, 
                                fertilizer_cost, area_ha=1.0, **kwargs):
    """Wrapper function for dynamic profit prediction"""
    return dynamic_profit.predict_profit_dynamic(crop, n, p, k, ph, temperature, humidity, 
                                                rainfall, fertilizer_cost, area_ha, **kwargs)
