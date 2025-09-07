"""
Test script for enhanced crop AI features
Tests previous crop impact, season detection, and enhanced predictions
"""

import json
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_nutrient_impact():
    """Test nutrient impact lookup functionality"""
    print("Testing Nutrient Impact Lookup")
    print("=" * 40)
    
    try:
        from nutrient_impact_lookup import (
            adjust_npk_for_previous_crop, 
            get_previous_crop_explanation,
            get_nutrient_impact_table
        )
        
        # Test cases
        test_cases = [
            ("wheat", 60, 45, 50),
            ("soybean", 40, 30, 35),
            ("cotton", 80, 60, 70),
            ("rice", 50, 40, 45)
        ]
        
        for crop, n, p, k in test_cases:
            adj_n, adj_p, adj_k = adjust_npk_for_previous_crop(n, p, k, crop)
            explanation = get_previous_crop_explanation(crop)
            print(f"\n{crop}: ({n}, {p}, {k}) -> ({adj_n:.1f}, {adj_p:.1f}, {adj_k:.1f})")
            print(f"Explanation: {explanation}")
        
        # Show lookup table
        df = get_nutrient_impact_table()
        print(f"\nTotal crops in database: {len(df)}")
        print("\nSample crops:")
        print(df.head(10)[['crop', 'n_delta', 'p_delta', 'k_delta', 'category']])
        
    except Exception as e:
        print(f"Error testing nutrient impact: {e}")

def test_season_detection():
    """Test season detection functionality"""
    print("\n\nTesting Season Detection")
    print("=" * 40)
    
    try:
        from season_detection import (
            detect_season_from_date,
            encode_season,
            check_crop_season_compatibility,
            get_season_recommendations
        )
        
        # Test current season
        current_season, current_month = detect_season_from_date()
        print(f"Current month: {current_month}")
        print(f"Current season: {current_season}")
        print(f"Encoded season: {encode_season(current_season)}")
        
        # Test different months
        test_months = [1, 4, 7, 10]
        print(f"\nSeason detection for different months:")
        for month in test_months:
            from season_detection import detect_season_from_month
            season = detect_season_from_month(month)
            encoded = encode_season(season)
            print(f"Month {month}: {season} (encoded: {encoded})")
        
        # Test crop-season compatibility
        print(f"\nCrop-Season Compatibility:")
        test_crops = ['rice', 'wheat', 'cotton']
        for crop in test_crops:
            for season in ['kharif', 'rabi']:
                suitability, explanation = check_crop_season_compatibility(crop, season)
                print(f"{crop} in {season}: {suitability}")
        
    except Exception as e:
        print(f"Error testing season detection: {e}")

def test_enhanced_prediction():
    """Test enhanced prediction with sample inputs"""
    print("\n\nTesting Enhanced Prediction")
    print("=" * 40)
    
    # Load sample input from file
    try:
        with open('sample_input_enhanced.json', 'r') as f:
            sample_input = json.load(f)
        print(f"Loaded sample input: {json.dumps(sample_input, indent=2)}")
    except Exception as e:
        print(f"Could not load sample input file: {e}")
        # Use hardcoded sample
        sample_input = {
            "N": 60, "P": 45, "K": 50,
            "temperature": 28, "humidity": 75, "ph": 6.8, "rainfall": 850,
            "area_ha": 2.5, "previous_crop": "wheat", "season": "kharif", "region": "north_india"
        }
    
    # Test with enhanced prediction
    try:
        # Try the enhanced prediction first
        from predict import predict_from_dict
        print("\nUsing enhanced prediction pipeline...")
        result = predict_from_dict(sample_input)
        
        print(f"\n✅ ENHANCED PREDICTION RESULT:")
        print("-" * 30)
        print(f"Recommended Crop: {result['recommended_crop']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Model Version: {result['model_version']}")
        
        if 'previous_crop_analysis' in result:
            pca = result['previous_crop_analysis']
            print(f"\nPrevious Crop Analysis:")
            print(f"  Previous Crop: {pca['previous_crop']}")
            print(f"  Original NPK: {pca['original_npk']}")
            print(f"  Adjusted NPK: {pca['adjusted_npk']}")
            print(f"  Nutrient Impact: {pca['nutrient_impact']}")
        
        if 'season_analysis' in result:
            sa = result['season_analysis']
            print(f"\nSeason Analysis:")
            print(f"  Detected Season: {sa['detected_season']}")
            print(f"  Season Suitability: {sa['season_suitability']}")
            print(f"  Explanation: {sa['season_explanation']}")
        
        print(f"\nExplanations:")
        for j, reason in enumerate(result.get('why', []), 1):
            print(f"  {j}. {reason}")
        
        # Save result
        with open('result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Result saved to result.json")
                
    except Exception as e:
        print(f"Enhanced prediction failed: {e}")
        print("\nFalling back to simple prediction...")
        
        try:
            # Fallback to simple app prediction
            sys.path.insert(0, '.')
            from simple_app import make_prediction
            result = make_prediction(sample_input)
            
            print(f"\n✅ FALLBACK PREDICTION RESULT:")
            print("-" * 30)
            print(f"Recommended Crop: {result['recommended_crop']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Model Version: {result['model_version']}")
            
            if 'previous_crop_analysis' in result:
                pca = result['previous_crop_analysis']
                print(f"Previous Crop: {pca['previous_crop']}")
                print(f"NPK: {pca['original_npk']} -> {pca['adjusted_npk']}")
            
            print(f"Explanations:")
            for j, reason in enumerate(result.get('why', []), 1):
                print(f"  {j}. {reason}")
            
            # Save result
            with open('result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Result saved to result.json")
            
        except Exception as e2:
            print(f"❌ Both enhanced and fallback predictions failed: {e2}")

def main():
    """Run all tests"""
    print("Enhanced Crop AI Features Test Suite")
    print("=" * 50)
    
    test_nutrient_impact()
    test_season_detection()
    test_enhanced_prediction()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")

if __name__ == "__main__":
    main()
