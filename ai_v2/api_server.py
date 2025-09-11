"""
API Server for Crop Recommendation System
Provides REST API interface for the AI prediction system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple, Dict, Any
import sys
import os
from datetime import datetime
import traceback
import logging

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import prediction functions
try:
    from src.predict import predict_from_dict, load_all_models
    MODELS_LOADED = True
    print("✅ Successfully imported prediction modules")
except ImportError as e:
    MODELS_LOADED = False
    print(f"❌ Failed to import prediction modules: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crop AI Recommendation API",
    description="AI-powered crop recommendation system with enhanced features",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class PredictionRequest(BaseModel):
    # Basic soil nutrients
    N: float = Field(..., ge=0, le=300, description="Nitrogen content (kg/ha)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus content (kg/ha)")
    K: float = Field(..., ge=0, le=300, description="Potassium content (kg/ha)")
    
    # Climate conditions
    temperature: float = Field(..., ge=-10, le=60, description="Temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Humidity (%)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH level")
    rainfall: float = Field(..., ge=0, le=10000, description="Rainfall (mm)")
    
    # Farm details
    area_ha: float = Field(..., ge=0.01, le=10000, description="Farm area (hectares)")
    
    # Enhanced features
    region: str = Field(default="default", description="Geographical region")
    previous_crop: Optional[str] = Field(default="", description="Previous crop grown")
    season: Optional[str] = Field(default="", description="Growing season")
    planting_date: Optional[str] = Field(default="", description="Planting date (YYYY-MM-DD)")

class ProfitBreakdown(BaseModel):
    gross: float
    investment: float
    net: float
    roi: float

class PreviousCropAnalysis(BaseModel):
    previous_crop: str
    original_npk: Tuple[float, float, float]
    adjusted_npk: Tuple[float, float, float]
    nutrient_impact: str

class SeasonAnalysis(BaseModel):
    detected_season: str
    season_suitability: str
    season_explanation: str

class FertilizerRecommendation(BaseModel):
    type: str
    dosage_kg_per_ha: float
    cost: float

class PredictionResponse(BaseModel):
    recommended_crop: str
    confidence: float
    expected_yield_t_per_acre: float
    profit_breakdown: ProfitBreakdown
    yield_interval_p10_p90: Tuple[float, float]
    previous_crop_analysis: Optional[PreviousCropAnalysis] = None
    season_analysis: Optional[SeasonAnalysis] = None
    fertilizer_recommendation: Optional[FertilizerRecommendation] = None
    why: Optional[List[str]] = None
    model_version: str
    timestamp: str

# Initialize models on startup
@app.on_event("startup")
async def startup_event():
    """Load AI models on server startup"""
    if MODELS_LOADED:
        try:
            load_all_models()
            logger.info("✅ AI models loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load AI models: {e}")
    else:
        logger.warning("⚠️ AI modules not available")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": MODELS_LOADED,
        "timestamp": datetime.now().isoformat()
    }

# Main prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict_crop(request: PredictionRequest):
    """
    Generate crop recommendation based on input parameters
    """
    try:
        if not MODELS_LOADED:
            # Return a fallback prediction if models aren't loaded
            logger.warning("⚠️ Models not loaded, returning fallback prediction")
            return PredictionResponse(
                recommended_crop="rice",
                confidence=0.75,
                expected_yield_t_per_acre=2.5,
                profit_breakdown=ProfitBreakdown(
                    gross=150000,
                    investment=80000,
                    net=70000,
                    roi=87.5
                ),
                yield_interval_p10_p90=(2.0, 3.0),
                model_version="2.0.0-fallback",
                timestamp=datetime.now().isoformat()
            )
        
        # Convert request to dictionary format
        input_data = {
            "N": request.N,
            "P": request.P,
            "K": request.K,
            "temperature": request.temperature,
            "humidity": request.humidity,
            "ph": request.ph,
            "rainfall": request.rainfall,
            "area_ha": request.area_ha,
            "region": request.region,
            "previous_crop": request.previous_crop,
            "season": request.season,
            "planting_date": request.planting_date
        }
        
        logger.info(f"🔄 Processing prediction request: {input_data}")
        
        # Make prediction using the AI model
        result = predict_from_dict(input_data)
        
        # Check for errors in the result
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Convert result to response format
        response_data = {
            "recommended_crop": str(result.get("recommended_crop", "unknown")),
            "confidence": float(result.get("confidence", 0.0)),
            "expected_yield_t_per_acre": float(result.get("expected_yield_t_per_acre", 0.0)),
            "profit_breakdown": {
                "gross": float(result.get("profit_breakdown", {}).get("gross", 0)),
                "investment": float(result.get("profit_breakdown", {}).get("investment", 0)),
                "net": float(result.get("profit_breakdown", {}).get("net", 0)),
                "roi": float(result.get("profit_breakdown", {}).get("roi", 0.0))
            },
            "yield_interval_p10_p90": tuple(result.get("yield_interval_p10_p90", (0.0, 0.0))),
            "model_version": str(result.get("model_version", "2.0.0")),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add optional fields if present
        if result.get("previous_crop_analysis"):
            pca = result["previous_crop_analysis"]
            response_data["previous_crop_analysis"] = {
                "previous_crop": pca.get("previous_crop", ""),
                "original_npk": tuple(pca.get("original_npk", [0, 0, 0])),
                "adjusted_npk": tuple(pca.get("adjusted_npk", [0, 0, 0])),
                "nutrient_impact": str(pca.get("nutrient_impact", "No significant nutrient impact detected"))
            }
        
        if result.get("season_analysis"):
            sa = result["season_analysis"]
            response_data["season_analysis"] = {
                "detected_season": str(sa.get("detected_season", "")),
                "season_suitability": str(sa.get("season_suitability", "")),
                "season_explanation": str(sa.get("season_explanation", ""))
            }
        
        if result.get("fertilizer_recommendation"):
            fr = result["fertilizer_recommendation"]
            response_data["fertilizer_recommendation"] = {
                "type": str(fr.get("type", "")),
                "dosage_kg_per_ha": float(fr.get("dosage_kg_per_ha", 0.0)),
                "cost": float(fr.get("cost", 0.0))
            }
        
        if result.get("why"):
            response_data["why"] = [str(item) for item in result["why"]] if isinstance(result["why"], list) else [str(result["why"])]
        
        logger.info(f"✅ Prediction successful: {response_data['recommended_crop']}")
        
        return PredictionResponse(**response_data)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"❌ Prediction error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during prediction: {str(e)}"
        )

# Get model information
@app.get("/models/info")
async def get_model_info():
    """Get information about loaded models"""
    try:
        if not MODELS_LOADED:
            return {"error": "Models not loaded"}
        
        return {
            "models_available": True,
            "model_version": "2.0.0",
            "features": [
                "crop_recommendation",
                "yield_prediction", 
                "profit_estimation",
                "previous_crop_analysis",
                "season_detection",
                "fertilizer_recommendation"
            ],
            "supported_crops": [
                "rice", "wheat", "maize", "sugarcane", "cotton", "jute", "coconut",
                "papaya", "orange", "apple", "muskmelon", "watermelon", "grapes",
                "mango", "banana", "pomegranate", "lentil", "blackgram", "mungbean",
                "mothbeans", "pigeonpeas", "kidneybeans", "chickpea", "coffee"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

# Example data endpoint
@app.get("/examples")
async def get_examples():
    """Get example input data for testing"""
    return {
        "examples": {
            "rice_farm_kharif": {
                "N": 80, "P": 40, "K": 40, "temperature": 27, "humidity": 80,
                "ph": 6.0, "rainfall": 1200, "area_ha": 3.0, "season": "kharif",
                "region": "south", "previous_crop": ""
            },
            "wheat_farm_rabi": {
                "N": 120, "P": 60, "K": 40, "temperature": 20, "humidity": 65,
                "ph": 7.5, "rainfall": 300, "area_ha": 5.0, "season": "rabi",
                "region": "north", "previous_crop": ""
            },
            "cotton_farm": {
                "N": 90, "P": 50, "K": 50, "temperature": 30, "humidity": 70,
                "ph": 7.0, "rainfall": 600, "area_ha": 10.0, "season": "kharif",
                "region": "west", "previous_crop": "wheat"
            },
            "vegetable_farm": {
                "N": 100, "P": 80, "K": 60, "temperature": 25, "humidity": 75,
                "ph": 6.5, "rainfall": 500, "area_ha": 1.0, "season": "",
                "region": "default", "previous_crop": ""
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Crop AI API Server on port {port}")
    print(f"📝 API Documentation: http://localhost:{port}/docs")
    print(f"🔧 Models loaded: {MODELS_LOADED}")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        access_log=True
    )