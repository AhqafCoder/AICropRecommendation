# 🌾 Crop AI - Intelligent Agricultural Recommendation System v2.0

A comprehensive **AI-powered crop recommendation system** that combines machine learning with agricultural domain expertise to provide farmers with optimal crop selection, fertilizer recommendations, and profitability estimates. Features an advanced **RandomForest classifier** trained on **22 crop varieties** with optimized hyperparameters for superior accuracy.

## 🎯 **Features**

### **Three AI Models**
- **🌱 Crop Recommender** - RandomForest classifier (100 estimators, max_depth=15) trained on 22 crop varieties with soil & weather features
- **🧪 Fertilizer Recommender** - Dynamic ML + lookup system for precise fertilizer suggestions  
- **💰 Profit Estimator** - LightGBM regressor predicting yield and profitability

### **Enhanced Features**
- **🌾 Previous Crop Impact** - Automatically adjusts soil NPK levels based on previous crop impact
- **🗓️ Season Detection** - Auto-detects agricultural season based on date/region with crop compatibility
- **🌍 Regional Support** - Different season definitions for North, South, East, West India
- **📊 Comprehensive Database** - 50+ crops with scientifically-based nutrient impacts
- **🔗 FastAPI Backend** - Modern REST API with automatic documentation and validation

### **Explainable AI**
- **SHAP Integration** - Advanced feature importance explanations for trained models
- **Rule-based Fallback** - Agricultural domain rules when models aren't trained
- **Human-friendly Insights** - Plain English explanations for all recommendations
- **Interactive Documentation** - Swagger UI for easy API testing

### **Production Ready**
- **FastAPI Backend v2.0.0** - Modern async REST API with automatic validation
- **Unified API** - Single function combining all three models
- **Input Validation** - Robust error handling and data validation
- **CORS Support** - Ready for web application integration
- **Interactive Docs** - Automatic API documentation at `/docs`
- **Enhanced Model Support** - Latest RandomForest crop classifier with 22 varieties

## 🌐 **API Endpoints**

### **FastAPI Endpoints (NEW)**
- **GET** `/` - API information
- **GET** `/health` - Health check and model status
- **POST** `/predict` - Complete prediction suite
- **POST** `/predict/crop` - Crop recommendation only
- **POST** `/predict/fertilizer` - Fertilizer recommendation only
- **POST** `/predict/economics` - Economic analysis only
- **POST** `/predict/explain` - Detailed SHAP-based explanations

### **Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 **Project Structure**
```
crop_ai/
├── data/
│   ├── raw/                    # Original datasets (Crop.csv, Fertilizer.csv)
│   └── processed/              # Cleaned & engineered datasets
├── src/
│   ├── api.py                 # 🆕 FastAPI REST endpoints with auto docs
│   ├── preprocess.py          # Data cleaning & preprocessing pipeline
│   ├── features.py            # Feature engineering (15+ derived features)
│   ├── train_fertilizer.py    # Fertilizer recommender training
│   ├── train_profit.py        # Profit estimator training (LightGBM)
│   ├── explain.py             # 🔧 SHAP explainability + rule-based fallback
│   ├── predict.py             # Unified inference API
│   ├── dynamic_recommendations.py # Dynamic fertilizer & profit calculations
│   ├── season_detection.py    # Season analysis & compatibility
│   └── nutrient_impact_lookup.py # Previous crop nutrient impact database
├── models/                    # Trained model artifacts & encoders
├── notebooks/                 # Jupyter notebooks for EDA
├── tests/                     # Unit tests
├── start_api_server.py        # 🆕 FastAPI server startup script
├── start_fastapi_server.ps1   # 🆕 PowerShell startup script
├── test_fastapi.py           # 🆕 FastAPI endpoint testing
├── requirements.txt           # Python dependencies (includes SHAP, LightGBM)
├── sample_input.json          # Example input format
├── FASTAPI_DOCUMENTATION.md   # 🆕 Complete FastAPI usage guide
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

### **2. Start FastAPI Server**
```bash
# Option 1: Python script
python start_api_server.py

# Option 2: PowerShell script (Windows)
.\start_fastapi_server.ps1

# Option 3: Direct uvicorn command
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### **3. Access API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### **4. Test API Endpoints**
```bash
# Test health check
curl http://localhost:8000/health

# Test crop prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.87, "humidity": 82.0,
    "ph": 6.5, "rainfall": 202.93, "area_ha": 1.0
  }'

# Test detailed explanations (SHAP-based)
curl -X POST "http://localhost:8000/predict/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.87, "humidity": 82.0,
    "ph": 6.5, "rainfall": 202.93, "area_ha": 1.0
  }'
```

### **5. Run Python Tests**
```bash
# Test API endpoints
python test_fastapi.py

# Test SHAP and LightGBM integration
python test_shap_lightgbm.py

# Use CLI interface (legacy)
python src/predict.py --input sample_input.json --output results.json
```

### **6. FastAPI Request/Response Format**

**Request Schema (Pydantic Validation):**
```json
{
  "N": 90.0,           // Nitrogen (0-300)
  "P": 42.0,           // Phosphorus (0-150) 
  "K": 43.0,           // Potassium (0-300)
  "ph": 6.5,           // pH level (3-10)
  "temperature": 20.87, // Temperature °C (0-50)
  "humidity": 82.0,     // Humidity % (0-100)
  "rainfall": 202.93,   // Rainfall mm (0-3000)
  "area_ha": 1.0,       // Area hectares (0.1-1000)
  "location": "Farm A"  // Optional location name
}
```

**Response Schema:**
```json
{
  "status": "success",
  "message": "Prediction completed successfully",
  "data": {
    "input_parameters": { /* Validated input data */ },
    "predictions": {
      "crop": {
        "recommended_crop": "rice",
        "confidence": 0.85,
        "reasoning": ["SHAP-based explanations"]
      },
      "fertilizer": {
        "recommended_fertilizer": "NPK 20-10-10",
        "reasoning": ["Soil nutrient analysis"]
      },
      "economics": {
        "estimated_yield_per_ha": 3.2,
        "roi_percentage": 80.0,
        "currency": "INR"
      }
    },
    "metadata": {
      "prediction_timestamp": "2025-01-21T10:30:00",
      "model_version": "1.0",
      "explanation_method": "SHAP + Feature Importance"
    }
  }
}
```

### **7. Legacy CLI Input Format**

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

### **8. Legacy CLI Output Format**

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

### **Current Model Status (Updated September 11, 2025)**
- **Crop Model**: `crop_model_v1.pkl` (3.24 MB) - Latest RandomForest classifier
- **Label Encoder**: `crop_label_encoder_v1.pkl` - Handles 22 crop classes
- **Feature Scaler**: `scaler_v1.pkl` - Standardized preprocessing
- **Training Date**: September 11, 2025 at 10:30 PM

### **Train Individual Models**
```bash
# Train crop classifier (RandomForest) - Latest version
python src/train_crop.py

# Train fertilizer recommender (Dynamic system)
python src/train_fertilizer.py

# Train profit estimator (LightGBM)
python src/train_profit.py
```

### **Model Artifacts**
- `models/crop_model_v1.pkl` - **Latest RandomForest classifier (September 11, 2025)**
- `models/crop_label_encoder_v1.pkl` - Crop class encoder for 22 varieties
- `models/scaler_v1.pkl` - Feature preprocessing pipeline
- `models/feature_list.yaml` - Core feature definitions [N, P, K, temperature, humidity, pH, rainfall]
- `models/fertilizer_lookup_v1.json` - Fertilizer recommendation lookup
- `models/fertilizer_eval_v1.json` - Fertilizer evaluation metrics (September 3, 2025)

## 🧠 **AI Architecture**

```
FastAPI → Input Validation → Preprocessing → Feature Engineering → 3 AI Models → SHAP → Unified Response
  ↓           ↓                 ↓              ↓               ↓        ↓       ↓
REST API   Pydantic         Cleaning      15+ Features    Crop/Fert/   SHAP    JSON
Endpoints  Schema           Validation    NPK Balance     Profit      Analysis Response
/docs UI   Validation       Scaling       Stress Index    Models    Fallback  with Meta
```

### **Model Details**
- **Crop Classifier**: RandomForestClassifier with 100 estimators, max_depth=15, min_samples_split=5
- **Training Features**: [N, P, K, temperature, humidity, pH, rainfall] + engineered features
- **Output Classes**: 22 supported crops (apple to watermelon)
- **Model Version**: crop_model_v1.pkl (trained September 11, 2025)
- **Performance**: Optimized hyperparameters with random_state=42 for reproducibility

## 📊 **Enhanced Dependencies**

**Core ML Libraries:**
- **LightGBM 4.6+** - High-performance gradient boosting (profit estimation)
- **SHAP 0.48+** - Advanced model interpretability and explanations
- **Scikit-learn 1.3+** - Traditional ML algorithms (crop classification)

**API Framework:**
- **FastAPI 0.104+** - Modern async web framework with auto-documentation
- **Pydantic 2.4+** - Data validation and serialization
- **Uvicorn** - ASGI server for FastAPI

**Data Processing:**
- **Pandas, NumPy** - Data manipulation and numerical computing
- **Joblib** - Model persistence and serialization

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

**Crop Classifier (RandomForest v1):**
- **Algorithm**: RandomForestClassifier with advanced hyperparameters
- **Model Parameters**: 
  - n_estimators: 100 (ensemble trees)
  - max_depth: 15 (prevents overfitting)
  - min_samples_split: 5, min_samples_leaf: 2
  - max_features: 'sqrt' (feature randomness)
  - random_state: 42 (reproducibility)
- **Features**: 7 core environmental + engineered features
- **Classes**: 22 supported crops (from apple to watermelon)
- **Training Date**: September 11, 2025
- **Model Size**: 3.24 MB (optimized for production)
- **Evaluation**: Cross-validated with robust performance metrics

**Profit Estimator:**
- Algorithm: LightGBM Regressor with early stopping
- Target: Yield prediction + cost calculation
- Metrics: RMSE, MAE, R² with feature importance

**Fertilizer Recommender:**
- Hybrid: Dynamic rule-based + ML fallback
- NPK optimization based on soil analysis
- Cost-effective dosage recommendations with regional pricing

## 🔍 **Explainable AI**

**SHAP Integration (Restored):**
- Advanced feature importance for crop predictions
- Tree-based SHAP explainer for RandomForest models
- Robust fallback to feature importance when SHAP fails
- Agricultural domain mapping for technical explanations

**Enhanced Explanations:**
- SHAP values converted to human-readable insights
- Feature contribution analysis (positive/negative impact)
- Confidence-based explanation filtering
- Method tracking (SHAP vs. fallback)

**Rule-based Fallback:**
- Works without trained models
- Agricultural best practices
- Domain-specific insights for fertilizer and profit predictions

## 📈 **Usage Examples**

### **4. Legacy Python Usage Examples**

**Basic Usage with Previous Crop:**
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

**Season Auto-Detection:**
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

### **3. FastAPI Usage Examples**

**Basic Prediction:**
```python
import requests

# Complete prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "N": 90, "P": 42, "K": 43,
        "temperature": 20.87, "humidity": 82.0,
        "ph": 6.5, "rainfall": 202.93, "area_ha": 1.0
    }
)
result = response.json()
print(f"Recommended crop: {result['data']['predictions']['crop']['recommended_crop']}")
```

**Detailed Explanations (SHAP-based):**
```python
# Get SHAP explanations
response = requests.post(
    "http://localhost:8000/predict/explain",
    json={
        "N": 90, "P": 42, "K": 43,
        "temperature": 20.87, "humidity": 82.0,
        "ph": 6.5, "rainfall": 202.93, "area_ha": 1.0
    }
)
explanations = response.json()
print(f"Model interpretability: {explanations['data']['model_interpretability']}")
```

**Individual Predictions:**
```python
# Just crop recommendation
crop_response = requests.post("http://localhost:8000/predict/crop", json=data)

# Just fertilizer recommendation  
fert_response = requests.post("http://localhost:8000/predict/fertilizer", json=data)

# Just economic analysis
econ_response = requests.post("http://localhost:8000/predict/economics", json=data)
```

### **5. Scenario Examples**

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

### **Supported Crop Predictions (22 Varieties)**
The current RandomForest model is trained to predict the following crop types:

- **🍎 Fruits**: apple, banana, coconut, grapes, mango, muskmelon, orange, papaya, pomegranate, watermelon
- **🌾 Cereals & Grains**: maize, rice  
- **🫘 Legumes & Pulses**: blackgram, chickpea, kidneybeans, lentil, mothbeans, mungbean, pigeonpeas
- **💰 Cash Crops**: coffee, cotton, jute

### **Model Coverage**
- **Total Classes**: 22 distinct crop varieties
- **Prediction Range**: From traditional cereals to high-value fruits
- **Geographic Scope**: Optimized for diverse Indian agricultural conditions
- **Feature Requirements**: 7 core environmental parameters (N, P, K, temperature, humidity, pH, rainfall)

### **Supported Previous Crops for Nutrient Impact Analysis (50+ crops)**
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
# Test FastAPI endpoints
python test_fastapi.py

# Test SHAP and LightGBM integration
python test_shap_lightgbm.py

# Test enhanced features
python test_enhanced_features.py
```

Test individual modules:
```bash
python src/season_detection.py
```

## 📋 **Requirements**

- Python 3.8+
- **LightGBM 4.6+** (Restored for profit estimation)
- **SHAP 0.48+** (Restored for model explanations)
- **FastAPI 0.104+** (New REST API framework)
- Scikit-learn 1.3+
- Pandas, NumPy, Joblib
- Uvicorn (ASGI server)
- Pydantic (Data validation)

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
- All 3 models implemented and operational
- **SHAP explainability restored and working**
- **LightGBM integration restored for profit estimation**
- **FastAPI backend with interactive documentation**
- Comprehensive testing and validation

**Ready for:**
- Production deployment with FastAPI
- Model training with real data
- Integration with web applications (CORS enabled)
- Enhanced predictions with previous crop and season analysis
- Real-time API usage with automatic documentation

## 🚀 **Recent Updates**

### **✅ Latest Model Training (September 11, 2025)**
- **RandomForest Classifier v1** - Retrained with optimized hyperparameters
- **22 Crop Varieties** - Comprehensive support from fruits to cash crops
- **Enhanced Performance** - 100 estimators, max_depth=15, advanced parameter tuning
- **Production Ready** - 3.24 MB optimized model with robust cross-validation

### **✅ FastAPI Integration v2.0.0**
- Modern REST API with automatic documentation
- Pydantic validation for request/response
- Interactive Swagger UI at `/docs`
- CORS support for web applications
- Comprehensive error handling

### **✅ Dependencies Restored**
- **SHAP 0.48+** - Advanced model interpretability
- **LightGBM 4.6+** - High-performance gradient boosting
- Enhanced explanation capabilities
- Better profit estimation accuracy

### **✅ API Endpoints**
- `/predict` - Complete analysis
- `/predict/crop` - Crop recommendation only  
- `/predict/fertilizer` - Fertilizer recommendation only
- `/predict/economics` - Economic analysis only
- `/predict/explain` - Detailed SHAP explanations
- `/health` - System health check

## 🎯 **Key Benefits**

1. **Latest RandomForest Model**: Advanced classifier with 100 estimators supporting 22 crop varieties
2. **Modern API Framework**: FastAPI v2.0.0 with auto-documentation and validation
3. **Advanced Explanations**: SHAP-based model interpretability
4. **High Performance**: LightGBM for accurate profit estimation
5. **Optimized Training**: Recent model training (Sep 11, 2025) with cross-validated hyperparameters
6. **More Accurate Predictions**: Considers soil history and seasonal factors
7. **Regional Adaptation**: Season detection varies by geographic region
8. **Comprehensive Database**: 50+ crops with scientifically-based nutrient impacts
9. **Smart Defaults**: Auto-detection when information is not provided
10. **Production Ready**: Complete error handling, CORS support, and interactive documentation

## 📖 **Documentation**

- **`FASTAPI_DOCUMENTATION.md`** - Complete FastAPI usage guide
- **`/docs`** - Interactive Swagger UI (when server is running)
- **`/redoc`** - Alternative API documentation
- **`ROI_FERTILIZER_FIX_SUMMARY.md`** - Dynamic recommendations details
- **`MODEL_UPDATE_SUMMARY.md`** - Model integration details
