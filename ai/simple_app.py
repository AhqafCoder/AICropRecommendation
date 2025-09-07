"""
Simplified FastAPI Backend for Crop AI System
Minimal working version with fallback predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import uvicorn
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Crop AI API",
    description="Intelligent Agricultural Recommendation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class CropPredictionRequest(BaseModel):
    N: float = Field(..., ge=0, le=200, description="Nitrogen content (0-200)")
    P: float = Field(..., ge=0, le=150, description="Phosphorus content (0-150)")
    K: float = Field(..., ge=0, le=200, description="Potassium content (0-200)")
    temperature: float = Field(..., ge=-10, le=55, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    ph: float = Field(..., ge=3.5, le=9.0, description="Soil pH")
    rainfall: float = Field(..., ge=0, le=5000, description="Rainfall in mm")
    area_ha: Optional[float] = Field(1.0, ge=0.1, le=1000, description="Area in hectares")

class FertilizerRecommendation(BaseModel):
    type: str
    dosage_kg_per_ha: float
    cost: int

class ProfitBreakdown(BaseModel):
    gross: int
    investment: int
    net: int
    roi: float

class CropPredictionResponse(BaseModel):
    recommended_crop: str
    confidence: float
    why: List[str]
    expected_yield_t_per_acre: float
    yield_interval_p10_p90: List[float]
    profit_breakdown: ProfitBreakdown
    fertilizer_recommendation: FertilizerRecommendation
    model_version: str
    timestamp: str
    area_analyzed_ha: float

# Fallback prediction function
def make_prediction(data: dict) -> dict:
    """Simple rule-based prediction system"""
    
    # Basic crop recommendation logic
    if data['rainfall'] > 1000:
        crop = "rice"
        confidence = 0.85
    elif data['rainfall'] < 300:
        crop = "millet" 
        confidence = 0.75
    elif data['temperature'] > 30:
        crop = "cotton"
        confidence = 0.80
    else:
        crop = "wheat"
        confidence = 0.70
    
    # Generate explanations
    explanations = []
    if data['rainfall'] > 1000:
        explanations.append(f"High rainfall ({data['rainfall']:.0f} mm) favors water-loving crops like rice")
    elif data['rainfall'] < 300:
        explanations.append(f"Low rainfall ({data['rainfall']:.0f} mm) suggests drought-resistant crops like millet")
    else:
        explanations.append(f"Moderate rainfall ({data['rainfall']:.0f} mm) supports diverse crop options")
    
    if data['temperature'] > 35:
        explanations.append(f"High temperature ({data['temperature']:.1f}°C) limits heat-sensitive crops")
    elif data['temperature'] < 15:
        explanations.append(f"Cool temperature ({data['temperature']:.1f}°C) favors temperate crops")
    else:
        explanations.append(f"Optimal temperature ({data['temperature']:.1f}°C) supports most crop varieties")
    
    if data['ph'] < 6.0:
        explanations.append(f"Acidic soil (pH {data['ph']:.1f}) suits acid-tolerant crops")
    elif data['ph'] > 7.5:
        explanations.append(f"Alkaline soil (pH {data['ph']:.1f}) requires alkali-tolerant varieties")
    else:
        explanations.append(f"Neutral soil (pH {data['ph']:.1f}) supports most crop types")
    
    # Basic yield estimation (tonnes per acre)
    base_yield = 2.5
    if crop == "rice":
        base_yield = 3.0
    elif crop == "wheat":
        base_yield = 2.8
    elif crop == "cotton":
        base_yield = 1.5
    elif crop == "millet":
        base_yield = 2.0
    
    # Adjust for conditions
    if data['rainfall'] > 800:
        base_yield *= 1.2
    elif data['rainfall'] < 400:
        base_yield *= 0.8
    
    # Fertilizer recommendation
    if data['N'] < 40:
        fertilizer_type = "NPK 20-10-10"
        dosage = 150
    elif data['P'] < 30:
        fertilizer_type = "NPK 10-20-10"
        dosage = 140
    elif data['K'] < 35:
        fertilizer_type = "NPK 10-10-20"
        dosage = 135
    else:
        fertilizer_type = "NPK 15-15-15"
        dosage = 130
    
    fertilizer_cost = dosage * 25  # ₹25 per kg
    
    # Profit calculation
    area_ha = data.get('area_ha', 1.0)
    yield_per_ha = base_yield * 2.47  # Convert acre to hectare
    
    # Market prices (₹ per quintal)
    crop_prices = {
        "rice": 2000,
        "wheat": 2200,
        "cotton": 5500,
        "millet": 1800
    }
    
    price_per_quintal = crop_prices.get(crop, 2000)
    total_yield_quintals = yield_per_ha * area_ha
    gross_revenue = int(total_yield_quintals * price_per_quintal)
    
    # Costs
    seed_cost = 2000 * area_ha
    labor_cost = 15000 * area_ha
    other_costs = 8000 * area_ha
    total_investment = int(seed_cost + labor_cost + fertilizer_cost + other_costs)
    
    net_profit = gross_revenue - total_investment
    roi = (net_profit / total_investment * 100) if total_investment > 0 else 0
    
    return {
        "recommended_crop": crop,
        "confidence": round(confidence, 3),
        "why": explanations[:3],
        "expected_yield_t_per_acre": round(base_yield, 2),
        "yield_interval_p10_p90": [
            round(base_yield * 0.8, 2),
            round(base_yield * 1.2, 2)
        ],
        "profit_breakdown": {
            "gross": gross_revenue,
            "investment": total_investment,
            "net": net_profit,
            "roi": round(roi, 1)
        },
        "fertilizer_recommendation": {
            "type": fertilizer_type,
            "dosage_kg_per_ha": dosage,
            "cost": fertilizer_cost
        },
        "model_version": "rule_based_v1",
        "timestamp": datetime.now().isoformat(),
        "area_analyzed_ha": area_ha
    }

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Crop AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": True,
        "version": "1.0.0"
    }

@app.post("/predict", response_model=CropPredictionResponse)
async def predict_crop(request: CropPredictionRequest):
    try:
        input_dict = request.model_dump()
        result = make_prediction(input_dict)
        return CropPredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(requests: List[CropPredictionRequest]):
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="Batch size cannot exceed 100 requests")
    
    results = []
    errors = []
    
    for i, request in enumerate(requests):
        try:
            input_dict = request.model_dump()
            result = make_prediction(input_dict)
            results.append({"index": i, "prediction": result})
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    
    return {
        "results": results,
        "errors": errors,
        "total_processed": len(requests),
        "successful": len(results),
        "failed": len(errors)
    }

if __name__ == "__main__":
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8000, reload=True)
