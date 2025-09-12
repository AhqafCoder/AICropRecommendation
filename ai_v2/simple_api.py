"""
Simple API server test - without complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Tuple
from datetime import datetime
import json

app = FastAPI(
    title="Crop AI Recommendation API - Test Mode",
    description="Simple test version of the AI API",
    version="2.0.0-test"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    N: float
    P: float  
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    area_ha: float
    region: str = "default"
    previous_crop: str = ""
    season: str = ""
    planting_date: str = ""

class ProfitBreakdown(BaseModel):
    gross: float
    investment: float
    net: float
    roi: float

class PredictionResponse(BaseModel):
    recommended_crop: str
    confidence: float
    expected_yield_t_per_acre: float
    profit_breakdown: ProfitBreakdown
    yield_interval_p10_p90: Tuple[float, float]
    model_version: str
    timestamp: str
    why: Optional[List[str]] = None

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": True,
        "timestamp": datetime.now().isoformat(),
        "mode": "test"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_crop(request: PredictionRequest):
    """
    Test prediction endpoint with mock data
    """
    try:
        # Simple rule-based prediction for testing
        if request.rainfall > 1000 and request.temperature > 25:
            crop = "rice"
            yield_val = 3.2
            roi = 85.0
        elif request.temperature < 22 and request.rainfall < 500:
            crop = "wheat"
            yield_val = 2.8
            roi = 92.0
        elif request.temperature > 28:
            crop = "cotton"
            yield_val = 2.1
            roi = 78.5
        else:
            crop = "maize"
            yield_val = 3.5
            roi = 88.0
        
        # Calculate mock financial data
        gross = yield_val * request.area_ha * 45000  # ₹45,000 per ton
        investment = request.area_ha * 65000  # ₹65,000 per hectare
        net = gross - investment
        
        explanations = [
            f"Based on rainfall of {request.rainfall}mm, {crop} is optimal",
            f"Temperature of {request.temperature}°C favors {crop} cultivation",
            f"Soil pH of {request.ph} is suitable for {crop}",
            f"NPK levels ({request.N}-{request.P}-{request.K}) support good {crop} growth"
        ]
        
        return PredictionResponse(
            recommended_crop=crop,
            confidence=0.85,
            expected_yield_t_per_acre=yield_val,
            profit_breakdown=ProfitBreakdown(
                gross=gross,
                investment=investment,
                net=net,
                roi=roi
            ),
            yield_interval_p10_p90=(yield_val * 0.8, yield_val * 1.2),
            model_version="2.0.0-test",
            timestamp=datetime.now().isoformat(),
            why=explanations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/examples")
async def get_examples():
    return {
        "examples": {
            "rice_farm": {
                "N": 80, "P": 40, "K": 40, "temperature": 27, "humidity": 80,
                "ph": 6.0, "rainfall": 1200, "area_ha": 3.0, "season": "kharif"
            },
            "wheat_farm": {
                "N": 120, "P": 60, "K": 40, "temperature": 20, "humidity": 65,
                "ph": 7.5, "rainfall": 300, "area_ha": 5.0, "season": "rabi"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Test AI API Server on port 8000")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "simple_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )