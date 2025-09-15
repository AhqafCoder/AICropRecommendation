"""
 Nutrient Impact Lookup Module
Handles previous crop impact on soil nutrients
"""

import pandas as pd
from typing import Tuple, Dict

# Previous crop nutrient impact lookup table
PREVIOUS_CROP_IMPACT = {
    'wheat': {'n_adjustment': -10, 'p_adjustment': -5, 'k_adjustment': -8},
    'rice': {'n_adjustment': -15, 'p_adjustment': -3, 'k_adjustment': -10},
    'corn': {'n_adjustment': -20, 'p_adjustment': -8, 'k_adjustment': -12},
    'soybean': {'n_adjustment': 15, 'p_adjustment': -5, 'k_adjustment': -5},  # Nitrogen fixing
    'cotton': {'n_adjustment': -25, 'p_adjustment': -10, 'k_adjustment': -15},
    'sugarcane': {'n_adjustment': -30, 'p_adjustment': -12, 'k_adjustment': -20},
    'potato': {'n_adjustment': -18, 'p_adjustment': -8, 'k_adjustment': -15},
    'tomato': {'n_adjustment': -12, 'p_adjustment': -6, 'k_adjustment': -10},
    'onion': {'n_adjustment': -8, 'p_adjustment': -4, 'k_adjustment': -6},
    'groundnut': {'n_adjustment': 10, 'p_adjustment': -3, 'k_adjustment': -4},  # Nitrogen fixing
    'chickpea': {'n_adjustment': 12, 'p_adjustment': -2, 'k_adjustment': -3},  # Nitrogen fixing
    'mustard': {'n_adjustment': -10, 'p_adjustment': -5, 'k_adjustment': -7},
    'barley': {'n_adjustment': -8, 'p_adjustment': -4, 'k_adjustment': -6},
    'millet': {'n_adjustment': -5, 'p_adjustment': -2, 'k_adjustment': -4},
    'default': {'n_adjustment': 0, 'p_adjustment': 0, 'k_adjustment': 0}
}

def adjust_npk_for_previous_crop(n: float, p: float, k: float, previous_crop: str) -> Tuple[float, float, float]:
    """
    Adjust NPK values based on previous crop impact
    
    Args:
        n, p, k: Current soil nutrient levels
        previous_crop: Name of the previous crop
    
    Returns:
        Tuple of adjusted (n, p, k) values
    """
    if not previous_crop or previous_crop.lower() == 'none':
        return n, p, k
    
    # Get impact values for the previous crop
    crop_key = previous_crop.lower()
    impact = PREVIOUS_CROP_IMPACT.get(crop_key, PREVIOUS_CROP_IMPACT['default'])
    
    # Apply adjustments
    adjusted_n = max(0, n + impact['n_adjustment'])
    adjusted_p = max(0, p + impact['p_adjustment'])
    adjusted_k = max(0, k + impact['k_adjustment'])
    
    return adjusted_n, adjusted_p, adjusted_k

def get_previous_crop_explanation(previous_crop: str) -> str:
    """
    Get explanation for previous crop impact
    
    Args:
        previous_crop: Name of the previous crop
    
    Returns:
        Explanation string
    """
    if not previous_crop or previous_crop.lower() == 'none':
        return "No previous crop impact considered"
    
    crop_key = previous_crop.lower()
    impact = PREVIOUS_CROP_IMPACT.get(crop_key, PREVIOUS_CROP_IMPACT['default'])
    
    if crop_key in ['soybean', 'groundnut', 'chickpea']:
        return f"Previous crop {previous_crop} was nitrogen-fixing, increasing soil nitrogen availability"
    elif impact['n_adjustment'] < -15:
        return f"Previous crop {previous_crop} was heavy nitrogen feeder, depleting soil nutrients significantly"
    elif impact['n_adjustment'] < 0:
        return f"Previous crop {previous_crop} moderately depleted soil nutrients"
    else:
        return f"Previous crop {previous_crop} had minimal impact on soil nutrients"

def get_nutrient_impact_summary(original_npk: Tuple[float, float, float], 
                               adjusted_npk: Tuple[float, float, float],
                               previous_crop: str) -> Dict:
    """
    Get summary of nutrient impact from previous crop
    
    Args:
        original_npk: Original N, P, K values
        adjusted_npk: Adjusted N, P, K values
        previous_crop: Name of previous crop
    
    Returns:
        Dictionary with impact summary
    """
    n_impact = adjusted_npk[0] - original_npk[0]
    p_impact = adjusted_npk[1] - original_npk[1]
    k_impact = adjusted_npk[2] - original_npk[2]
    
    return {
        'previous_crop': previous_crop,
        'original_npk': original_npk,
        'adjusted_npk': adjusted_npk,
        'nutrient_impact': (n_impact, p_impact, k_impact),
        'explanation': get_previous_crop_explanation(previous_crop)
    }
