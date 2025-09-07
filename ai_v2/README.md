# 🌾 Crop AI - Intelligent Agricultural Recommendation System

A comprehensive **AI-powered crop recommendation system** that combines machine learning with agricultural domain expertise to provide farmers with optimal crop selection, fertilizer recommendations, and profitability estimates.

## 🎯 **Features**

### **Three AI Models**
- **🌱 Crop Recommender** - LightGBM classifier recommending optimal crops based on soil & weather
- **🧪 Fertilizer Recommender** - Hybrid ML + lookup system for precise fertilizer suggestions  
- **💰 Profit Estimator** - LightGBM regressor predicting yield and profitability

### **Enhanced Features**
- **🌾 Previous Crop Impact** - Automatically adjusts soil NPK levels based on previous crop impact
- **🗓️ Season Detection** - Auto-detects agricultural season based on date/region with crop compatibility
- **🌍 Regional Support** - Different season definitions for North, South, East, West India
- **📊 Comprehensive Database** - 50+ crops with scientifically-based nutrient impacts

### **Explainable AI**
- **SHAP Integration** - Feature importance explanations for trained models
- **Rule-based Fallback** - Agricultural domain rules when models aren't trained
- **Human-friendly Insights** - Plain English explanations for all recommendations

### **Production Ready**
- **Unified API** - Single function combining all three models
- **Input Validation** - Robust error handling and data validation
- **CLI Interface** - Easy command-line usage with JSON I/O
- **FastAPI Backend** - REST endpoints with CORS support and complete error handling

## 📁 **Project Structure**
```
crop_ai/
├── data/
│   ├── raw/                    # Original datasets (Crop.csv, Fertilizer.csv)
│   └── processed/              # Cleaned & engineered datasets
├── src/
│   ├── preprocess.py          # Data cleaning & preprocessing pipeline
│   ├── features.py            # Feature engineering (15+ derived features)
│   ├── train_crop.py          # Crop classifier training (LightGBM)
│   ├── train_fertilizer.py    # Fertilizer recommender training
│   ├── train_profit.py        # Profit estimator training (yield prediction)
│   ├── explain.py             # SHAP explainability + rule-based fallback
│   └── predict.py             # Unified inference API
├── models/                    # Trained model artifacts & encoders
├── notebooks/                 # Jupyter notebooks for EDA
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── sample_input.json          # Example input format
└── README.md
```

## 🚀 **Quick Start**

### **1. Setup Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Run Predictions**
```bash
# Use sample data
python src/predict.py

# Use custom input file
python src/predict.py --input sample_input.json --output results.json
```

### **3. Input Format**

**Basic Input:**
```json
{
  "N": 60,
  "P": 35, 
  "K": 20,
  "temperature": 25,
  "humidity": 70,
  "ph": 6.5,
  "rainfall": 800,
  "area_ha": 2.0
}
```

**Enhanced Input (with previous crop & season):**
```json
{
  "N": 60, "P": 45, "K": 50,
  "temperature": 28, "humidity": 75, "ph": 6.8, "rainfall": 850,
  "area_ha": 2.5,
  "previous_crop": "wheat",
  "season": "kharif",
  "region": "north_india",
  "planting_date": "2024-07-15"
}
```

### **4. Output Format**

**Basic Output:**
```json
{
  "recommended_crop": "rice",
  "confidence": 0.87,
  "why": [
    "Moderate rainfall (800 mm) supports diverse crop options",
    "Optimal temperature (25.0°C) supports most crop varieties", 
    "Neutral soil (pH 6.5) supports most crop types"
  ],
  "expected_yield_t_per_acre": 4.5,
  "profit_breakdown": {
    "gross": 198000,
    "investment": 80500, 
    "net": 117500,
    "roi": 146.0
  },
  "fertilizer_recommendation": {
    "type": "NPK 20-10-10",
    "dosage_kg_per_ha": 150,
    "cost": 4750
  }
}
```

**Enhanced Output (with previous crop & season analysis):**
```json
{
  "recommended_crop": "rice",
  "confidence": 0.85,
  "why": [
    "Previous wheat depleted nitrogen by 25 units",
    "Season analysis: rice is highly suitable for kharif season",
    "Soil nutrients adjusted based on previous crop: N-25, P-5, K-10",
    "High rainfall (850 mm) favors water-loving crops"
  ],
  "previous_crop_analysis": {
    "previous_crop": "wheat",
    "original_npk": [60, 45, 50],
    "adjusted_npk": [35, 40, 40],
    "nutrient_impact": [-25, -5, -10]
  },
  "season_analysis": {
    "detected_season": "kharif",
    "season_suitability": "highly_suitable",
    "season_explanation": "rice is highly suitable for kharif season cultivation"
  }
}
```

## 🔧 **Model Training**

### **Train Individual Models**
```bash
# Train crop classifier
python src/train_crop.py

# Train fertilizer recommender  
python src/train_fertilizer.py

# Train profit estimator
python src/train_profit.py
```

### **Model Artifacts**
- `models/crop_model_v1.pkl` - Trained crop classifier
- `models/profit_model_v1.pkl` - Trained yield predictor
- `models/scaler_v1.pkl` - Feature scaler
- `models/label_encoders/` - Categorical encoders

## 🧠 **AI Architecture**

```
Input → Preprocessing → Feature Engineering → 3 AI Models → SHAP → Unified API
  ↓           ↓              ↓               ↓        ↓       ↓
JSON     Cleaning      15+ Features    Crop/Fert/   Rule    JSON
Data   Validation      NPK Balance     Profit      Based   Output
       Scaling         Stress Index    Models    Fallback
```

## 📊 **Feature Engineering**

**Core Features:** N, P, K, pH, Temperature, Humidity, Rainfall, Area

**Enhanced Features:**
- Previous Crop Impact (NPK adjustments)
- Season Detection & Encoding
- Regional Adaptation
- Planting Date Analysis

**Derived Features (15+):**
- NPK Balance & Ratios
- Soil Fertility Index  
- Temperature/Humidity Stress
- Rainfall Categories
- Nutrient Deficiency Flags
- Growing Season Indicators
- Previous Crop Nutrient Impact
- Season Compatibility Scores

## 🎯 **Model Performance**

**Crop Classifier:**
- Algorithm: LightGBM with 5-fold CV
- Features: 22 engineered features
- Evaluation: Accuracy, Precision, Recall, F1

**Profit Estimator:**
- Algorithm: LightGBM Regressor
- Target: Yield prediction + cost calculation
- Metrics: RMSE, MAE, R²

**Fertilizer Recommender:**
- Hybrid: Rule-based + ML fallback
- NPK optimization based on soil analysis
- Cost-effective dosage recommendations

## 🔍 **Explainable AI**

**SHAP Integration:**
- Feature importance for each prediction
- Agricultural domain mapping
- Top-3 reasoning explanations

**Rule-based Fallback:**
- Works without trained models
- Agricultural best practices
- Domain-specific insights

## 📈 **Usage Examples**

### **1. Basic Usage with Previous Crop**
```python
from src.predict import predict_from_dict

input_data = {
    "N": 60, "P": 45, "K": 50,
    "temperature": 28, "humidity": 75, "ph": 6.8, "rainfall": 850,
    "area_ha": 2.5,
    "previous_crop": "wheat"  # This will adjust NPK levels
}

result = predict_from_dict(input_data)
print(f"Recommended: {result['recommended_crop']}")
print(f"NPK adjusted from {result['previous_crop_analysis']['original_npk']} to {result['previous_crop_analysis']['adjusted_npk']}")
```

### **2. Season Auto-Detection**
```python
# Season will be auto-detected based on current date
input_data = {
    "N": 40, "P": 35, "K": 45,
    "temperature": 18, "humidity": 60, "ph": 7.2, "rainfall": 150,
    "region": "north_india"  # Season detection varies by region
}

result = predict_from_dict(input_data)
print(f"Detected season: {result['season_analysis']['detected_season']}")
```

### **3. FastAPI Usage**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "N": 60, "P": 45, "K": 50,
    "temperature": 28, "humidity": 75, "ph": 6.8, "rainfall": 850,
    "area_ha": 2.5,
    "previous_crop": "wheat",
    "season": "kharif",
    "region": "north_india"
  }'
```

### **4. Scenario Examples**

**High Rainfall Scenario:**
```json
Input: {"rainfall": 1200, "temperature": 28, "humidity": 80}
Output: "High rainfall (1200 mm) favors water-loving crops like rice"
```

**Low Nutrient Scenario:**  
```json
Input: {"N": 20, "P": 15, "K": 10}
Output: "Low Nitrogen (20) may limit leafy crop growth"
```

**Previous Crop Impact:**
```json
Input: {"previous_crop": "cotton", "N": 80, "P": 60, "K": 70}
Output: "Previous cotton depleted nutrients heavily: N-40, P-15, K-25"
```

## 🌱 **Crop Database**

### **Supported Previous Crops (50+ crops)**
- **Cereals**: wheat, rice, maize, barley, oats, millet, sorghum
- **Legumes**: soybean, chickpea, lentil, pea, groundnut, cowpea
- **Cash Crops**: cotton, sugarcane, tobacco, jute
- **Vegetables**: tomato, potato, onion, cabbage, cauliflower, brinjal
- **Fruits**: banana, mango, citrus, apple, grapes
- **Oil Seeds**: mustard, sunflower, sesame, safflower
- **Spices**: turmeric, ginger, garlic, coriander

### **Nutrient Impact Examples**
- **Wheat**: N -25, P -5, K -10 (moderate depletion)
- **Soybean**: N +10, P -8, K -12 (nitrogen fixation)
- **Cotton**: N -40, P -15, K -25 (heavy depletion)
- **Rice**: N -30, P -10, K -15 (high water crop depletion)

## 🗓️ **Season Definitions**

### **Kharif (Monsoon Season)**
- **Months**: June-October
- **Crops**: rice, maize, cotton, sugarcane, soybean
- **Characteristics**: High rainfall, warm temperatures

### **Rabi (Winter Season)**
- **Months**: November-March
- **Crops**: wheat, barley, chickpea, mustard, pea
- **Characteristics**: Low rainfall, cool temperatures

### **Zaid (Summer Season)**
- **Months**: April-May
- **Crops**: watermelon, muskmelon, fodder crops
- **Characteristics**: Very low rainfall, hot temperatures

## 🧪 **Testing**

Run the comprehensive test suite:
```bash
python test_enhanced_features.py
```

Test individual modules:
```bash
python src/season_detection.py
```

## 🔄 **Backward Compatibility**

The enhanced system is fully backward compatible:
- All existing API endpoints work without changes
- New fields are optional - system provides sensible defaults
- Existing input formats continue to work
- Enhanced features activate only when new fields are provided

## 🛠️ **Development**

### **Add New Features**
1. Update `src/features.py` with new feature engineering
2. Retrain models with `src/train_*.py`
3. Update explanation mapping in `src/explain.py`

### **Extend Models**
1. Add new model in `src/train_newmodel.py`
2. Integrate in `src/predict.py`
3. Add SHAP explanations in `src/explain.py`

### **Model Training with Enhanced Features**
For production use, retrain your ML models with the new features:
1. Add `previous_crop` and `season` columns to training data
2. Use the enhanced feature engineering pipeline
3. Include the new features in your model input vector:
   `[N_adjusted, P_adjusted, K_adjusted, temperature, humidity, ph, rainfall, season_encoded, area_log]`

## 📋 **Requirements**

- Python 3.8+
- LightGBM 4.6+
- Scikit-learn 1.3+
- SHAP 0.42+
- Pandas, NumPy, Joblib

## 🎉 **Status**

✅ **Complete AI System**
- All 3 models implemented
- SHAP explainability working
- Production-ready API
- Comprehensive testing

**Ready for:**
- Model training with real data
- Production deployment
- Integration with farm management systems
- Enhanced predictions with previous crop and season analysis

## 🎯 **Key Benefits**

1. **More Accurate Predictions**: Considers soil history and seasonal factors
2. **Explainable AI**: Clear explanations for why crops are recommended
3. **Regional Adaptation**: Season detection varies by geographic region
4. **Comprehensive Database**: 50+ crops with scientifically-based nutrient impacts
5. **Smart Defaults**: Auto-detection when information is not provided
6. **Production Ready**: FastAPI backend with complete error handling and CORS support
