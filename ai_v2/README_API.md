# CropAI Backend API

This is the AI-powered backend for the Crop Recommendation System.

## Features

- **Crop Recommendation**: AI-based crop suggestions based on soil and weather conditions
- **Fertilizer Recommendation**: Optimal fertilizer type and dosage recommendations
- **Profit Analysis**: Expected yield and profit calculations
- **Season Detection**: Automatic season detection based on planting date and region
- **Previous Crop Analysis**: Impact analysis of previously grown crops

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the development server:
```bash
python simple_app.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /predict
Get crop recommendations based on soil and environmental data.

**Request Body:**
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.5,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 200.0,
  "area_ha": 2.5,
  "previous_crop": "wheat",
  "region": "north_india"
}
```

**Response:**
```json
{
  "recommended_crop": "rice",
  "confidence": 0.85,
  "why": ["High rainfall suitable for rice cultivation", "..."],
  "expected_yield_t_per_acre": 3.2,
  "profit_breakdown": {
    "gross": 180000,
    "investment": 75000,
    "net": 105000,
    "roi": 140.0
  },
  "fertilizer_recommendation": {
    "type": "NPK 15-15-15",
    "dosage_kg_per_ha": 130,
    "cost": 3000
  }
}
```

## Model Information

The system uses multiple ML models:
- **Crop Model**: LightGBM classifier for crop recommendations
- **Fertilizer Model**: XGBoost for fertilizer optimization
- **Yield Model**: Random Forest for yield and profit prediction
