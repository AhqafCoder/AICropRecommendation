"""
Season Detection and Encoding Module
Implements automatic season detection based on month and region
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, Optional
import calendar

# Season definitions for different regions in India
SEASON_DEFINITIONS = {
    'north_india': {
        'kharif': [6, 7, 8, 9, 10],      # June to October (Monsoon crops)
        'rabi': [11, 12, 1, 2, 3],       # November to March (Winter crops)
        'zaid': [4, 5]                   # April to May (Summer crops)
    },
    'south_india': {
        'kharif': [6, 7, 8, 9, 10, 11], # June to November (Southwest monsoon)
        'rabi': [12, 1, 2, 3, 4],       # December to April (Northeast monsoon)
        'zaid': [5]                      # May (Summer crops)
    },
    'west_india': {
        'kharif': [6, 7, 8, 9, 10],     # June to October
        'rabi': [11, 12, 1, 2, 3],      # November to March
        'zaid': [4, 5]                   # April to May
    },
    'east_india': {
        'kharif': [6, 7, 8, 9, 10, 11], # June to November
        'rabi': [12, 1, 2, 3],          # December to March
        'zaid': [4, 5]                   # April to May
    },
    'default': {
        'kharif': [6, 7, 8, 9, 10],     # June to October (Default)
        'rabi': [11, 12, 1, 2, 3],      # November to March
        'zaid': [4, 5]                   # April to May
    }
}

# Crop suitability by season
SEASON_CROP_SUITABILITY = {
    'kharif': {
        'highly_suitable': ['rice', 'maize', 'cotton', 'sugarcane', 'soybean', 'groundnut', 'sorghum', 'millet'],
        'suitable': ['sunflower', 'sesame', 'cowpea', 'green_gram', 'black_gram'],
        'not_suitable': ['wheat', 'barley', 'chickpea', 'lentil', 'mustard', 'pea']
    },
    'rabi': {
        'highly_suitable': ['wheat', 'barley', 'chickpea', 'lentil', 'mustard', 'pea', 'oats'],
        'suitable': ['potato', 'onion', 'garlic', 'coriander', 'cumin'],
        'not_suitable': ['rice', 'cotton', 'sugarcane', 'soybean', 'maize']
    },
    'zaid': {
        'highly_suitable': ['watermelon', 'muskmelon', 'cucumber', 'fodder_maize', 'fodder_sorghum'],
        'suitable': ['sunflower', 'sesame', 'green_gram', 'cowpea'],
        'not_suitable': ['wheat', 'rice', 'cotton', 'chickpea', 'mustard']
    }
}

def detect_season_from_month(month: int, region: str = 'default') -> str:
    """
    Detect agricultural season based on month and region
    
    Args:
        month: Month number (1-12)
        region: Region identifier (north_india, south_india, etc.)
    
    Returns:
        Season name ('kharif', 'rabi', 'zaid')
    """
    if region not in SEASON_DEFINITIONS:
        region = 'default'
    
    seasons = SEASON_DEFINITIONS[region]
    
    for season, months in seasons.items():
        if month in months:
            return season
    
    # Fallback to default if month not found
    return 'kharif'

def detect_season_from_date(date_input: Optional[str] = None, region: str = 'default') -> Tuple[str, int]:
    """
    Detect season from date string or current date
    
    Args:
        date_input: Date string in format 'YYYY-MM-DD' or None for current date
        region: Region identifier
    
    Returns:
        Tuple of (season_name, month_number)
    """
    if date_input:
        try:
            date_obj = datetime.strptime(date_input, '%Y-%m-%d')
            month = date_obj.month
        except ValueError:
            # Try alternative formats
            try:
                date_obj = datetime.strptime(date_input, '%d-%m-%Y')
                month = date_obj.month
            except ValueError:
                month = datetime.now().month
    else:
        month = datetime.now().month
    
    season = detect_season_from_month(month, region)
    return season, month

def encode_season(season: str) -> int:
    """
    Encode season as numerical value for ML models
    
    Args:
        season: Season name ('kharif', 'rabi', 'zaid')
    
    Returns:
        Encoded value (0=Kharif, 1=Rabi, 2=Zaid)
    """
    season_encoding = {
        'kharif': 0,
        'rabi': 1,
        'zaid': 2
    }
    
    return season_encoding.get(season.lower(), 0)

def decode_season(encoded_season: int) -> str:
    """
    Decode numerical season value back to season name
    
    Args:
        encoded_season: Encoded season value (0, 1, or 2)
    
    Returns:
        Season name
    """
    season_decoding = {
        0: 'kharif',
        1: 'rabi',
        2: 'zaid'
    }
    
    return season_decoding.get(encoded_season, 'kharif')

def get_season_characteristics(season: str) -> Dict:
    """
    Get characteristics and typical conditions for a season
    
    Args:
        season: Season name
    
    Returns:
        Dictionary with season characteristics
    """
    characteristics = {
        'kharif': {
            'description': 'Monsoon season crops (June-October)',
            'typical_rainfall': 'High (600-1200mm)',
            'temperature': 'Warm to hot (25-35°C)',
            'humidity': 'High (70-90%)',
            'main_crops': ['rice', 'maize', 'cotton', 'sugarcane', 'soybean'],
            'sowing_period': 'June-July',
            'harvesting_period': 'September-November'
        },
        'rabi': {
            'description': 'Winter season crops (November-March)',
            'typical_rainfall': 'Low (50-200mm)',
            'temperature': 'Cool to moderate (10-25°C)',
            'humidity': 'Moderate (50-70%)',
            'main_crops': ['wheat', 'barley', 'chickpea', 'mustard', 'pea'],
            'sowing_period': 'November-December',
            'harvesting_period': 'March-April'
        },
        'zaid': {
            'description': 'Summer season crops (April-May)',
            'typical_rainfall': 'Very low (0-50mm)',
            'temperature': 'Hot (30-45°C)',
            'humidity': 'Low (30-50%)',
            'main_crops': ['watermelon', 'muskmelon', 'fodder_crops'],
            'sowing_period': 'March-April',
            'harvesting_period': 'May-June'
        }
    }
    
    return characteristics.get(season.lower(), characteristics['kharif'])

def check_crop_season_compatibility(crop: str, season: str) -> Tuple[str, str]:
    """
    Check if a crop is suitable for the given season
    
    Args:
        crop: Crop name
        season: Season name
    
    Returns:
        Tuple of (suitability_level, explanation)
    """
    crop_lower = crop.lower().replace(' ', '_')
    season_lower = season.lower()
    
    if season_lower not in SEASON_CROP_SUITABILITY:
        return 'unknown', f"Season {season} not recognized"
    
    season_crops = SEASON_CROP_SUITABILITY[season_lower]
    
    for suitability, crops in season_crops.items():
        if crop_lower in crops:
            explanations = {
                'highly_suitable': f"{crop} is highly suitable for {season} season cultivation",
                'suitable': f"{crop} can be grown in {season} season with proper management",
                'not_suitable': f"{crop} is not recommended for {season} season due to climatic constraints"
            }
            return suitability, explanations[suitability]
    
    # If crop not found in any category, provide general guidance
    return 'moderate', f"{crop} suitability for {season} season needs to be evaluated based on local conditions"

def get_season_recommendations(season: str, region: str = 'default') -> Dict:
    """
    Get comprehensive recommendations for a given season
    
    Args:
        season: Season name
        region: Region identifier
    
    Returns:
        Dictionary with season-specific recommendations
    """
    characteristics = get_season_characteristics(season)
    
    recommendations = {
        'season': season,
        'region': region,
        'characteristics': characteristics,
        'recommended_crops': SEASON_CROP_SUITABILITY.get(season.lower(), {}).get('highly_suitable', []),
        'suitable_crops': SEASON_CROP_SUITABILITY.get(season.lower(), {}).get('suitable', []),
        'avoid_crops': SEASON_CROP_SUITABILITY.get(season.lower(), {}).get('not_suitable', []),
        'encoded_value': encode_season(season)
    }
    
    return recommendations

def add_season_features(df: pd.DataFrame, date_column: str = None, region: str = 'default') -> pd.DataFrame:
    """
    Add season-related features to a DataFrame
    
    Args:
        df: Input DataFrame
        date_column: Name of date column (if None, uses current date)
        region: Region for season detection
    
    Returns:
        DataFrame with added season features
    """
    df = df.copy()
    
    if date_column and date_column in df.columns:
        # Use provided date column
        df['season'] = df[date_column].apply(
            lambda x: detect_season_from_date(str(x), region)[0]
        )
        df['month'] = df[date_column].apply(
            lambda x: detect_season_from_date(str(x), region)[1]
        )
    else:
        # Use current date for all rows
        current_season, current_month = detect_season_from_date(None, region)
        df['season'] = current_season
        df['month'] = current_month
    
    # Add encoded season
    df['season_encoded'] = df['season'].apply(encode_season)
    
    # Add season characteristics as features
    df['is_kharif'] = (df['season'] == 'kharif').astype(int)
    df['is_rabi'] = (df['season'] == 'rabi').astype(int)
    df['is_zaid'] = (df['season'] == 'zaid').astype(int)
    
    return df

if __name__ == "__main__":
    # Test season detection functionality
    print("Testing Season Detection Module")
    print("=" * 40)
    
    # Test current season detection
    current_season, current_month = detect_season_from_date()
    print(f"Current month: {current_month} ({calendar.month_name[current_month]})")
    print(f"Current season: {current_season}")
    print(f"Encoded season: {encode_season(current_season)}")
    
    # Test different months
    test_months = [1, 4, 7, 10]
    print(f"\nSeason detection for different months:")
    for month in test_months:
        season = detect_season_from_month(month)
        encoded = encode_season(season)
        print(f"Month {month}: {season} (encoded: {encoded})")
    
    # Test crop-season compatibility
    print(f"\nCrop-Season Compatibility Tests:")
    test_crops = ['rice', 'wheat', 'cotton', 'watermelon']
    for crop in test_crops:
        for season in ['kharif', 'rabi', 'zaid']:
            suitability, explanation = check_crop_season_compatibility(crop, season)
            print(f"{crop} in {season}: {suitability}")
    
    # Test DataFrame feature addition
    print(f"\nTesting DataFrame feature addition:")
    sample_df = pd.DataFrame({
        'n': [60, 45, 80],
        'p': [40, 35, 55],
        'k': [50, 45, 65]
    })
    
    df_with_seasons = add_season_features(sample_df)
    print(df_with_seasons[['season', 'season_encoded', 'is_kharif', 'is_rabi', 'is_zaid']].head())
