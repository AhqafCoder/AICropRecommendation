# 🌾 Crop AI - Intelligent Agricultural Recommendation System

A comprehensive **AI-powered crop recommendation system** that combines machine learning with agricultural domain expertise to provide farmers with optimal crop selection, fertilizer recommendations, and profitability estimates.

## 🎯 **Features**

### **Three AI Models**
- **🌱 Crop Recommender** - LightGBM classifier recommending optimal crops based on soil & weather
- **🧪 Fertilizer Recommender** - Hybrid ML + lookup system for precise fertilizer suggestions  
- **💰 Profit Estimator** - LightGBM regressor predicting yield and profitability

### **Explainable AI**
- **SHAP Integration** - Feature importance explanations for trained models
- **Rule-based Fallback** - Agricultural domain rules when models aren't trained
- **Human-friendly Insights** - Plain English explanations for all recommendations

### **Production Ready**
- **Unified API** - Single function combining all three models
- **Input Validation** - Robust error handling and data validation
- **CLI Interface** - Easy command-line usage with JSON I/O

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

### **4. Output Format**
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

**Core Features:** N, P, K, pH, Temperature, Humidity, Rainfall

**Derived Features (15+):**
- NPK Balance & Ratios
- Soil Fertility Index  
- Temperature/Humidity Stress
- Rainfall Categories
- Nutrient Deficiency Flags
- Growing Season Indicators

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

### **High Rainfall Scenario**
```json
Input: {"rainfall": 1200, "temperature": 28, "humidity": 80}
Output: "High rainfall (1200 mm) favors water-loving crops like rice"
```

### **Low Nutrient Scenario**  
```json
Input: {"N": 20, "P": 15, "K": 10}
Output: "Low Nitrogen (20) may limit leafy crop growth"
```

### **Optimal Conditions**
```json
Input: {"ph": 6.8, "temperature": 24, "rainfall": 600}
Output: "Neutral soil (pH 6.8) supports most crop types"
```

## 🛠️ **Development**

### **Add New Features**
1. Update `src/features.py` with new feature engineering
2. Retrain models with `src/train_*.py`
3. Update explanation mapping in `src/explain.py`

### **Extend Models**
1. Add new model in `src/train_newmodel.py`
2. Integrate in `src/predict.py`
3. Add SHAP explanations in `src/explain.py`

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
