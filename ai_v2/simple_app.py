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
    # Enhanced fields
    previous_crop: Optional[str] = Field("", description="Previous crop grown on the field")
    season: Optional[str] = Field(None, description="Growing season (kharif/rabi/zaid) - auto-detected if not provided")
    region: Optional[str] = Field("default", description="Geographic region for season detection")
    planting_date: Optional[str] = Field(None, description="Planned planting date (YYYY-MM-DD format)")

class FertilizerRecommendation(BaseModel):
    type: str
    dosage_kg_per_ha: float
    cost: int

class ProfitBreakdown(BaseModel):
    gross: int
    investment: int
    net: int
    roi: float

class PreviousCropAnalysis(BaseModel):
    previous_crop: str
    original_npk: List[float]
    adjusted_npk: List[float]
    nutrient_impact: List[float]

class SeasonAnalysis(BaseModel):
    detected_season: str
    season_suitability: str
    season_explanation: str

class CropPredictionResponse(BaseModel):
    recommended_crop: str
    confidence: float
    why: List[str]
    expected_yield_t_per_acre: float
    yield_interval_p10_p90: List[float]
    profit_breakdown: ProfitBreakdown
    fertilizer_recommendation: FertilizerRecommendation
    # Enhanced fields
    previous_crop_analysis: PreviousCropAnalysis
    season_analysis: SeasonAnalysis
    model_version: str
    timestamp: str
    area_analyzed_ha: float
    region: str

# Enhanced prediction function with previous crop and season support
def make_prediction(data: dict) -> dict:
    """Enhanced rule-based prediction system with previous crop and season analysis"""
    
    # Import enhanced prediction if available
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from predict import predict_from_dict
        return predict_from_dict(data)
    except Exception as e:
        print(f"Enhanced prediction failed, using fallback: {e}")
        # Fallback to simple rule-based system
        pass
    
    # Enhanced fallback with previous crop and season consideration
    previous_crop = data.get('previous_crop', '')
    season = data.get('season', 'kharif')  # Default to kharif if not provided
    
    # Ensure season is never None
    if season is None or season == '':
        season = 'kharif'
    
    # Basic crop recommendation logic with season awareness
    if season == 'kharif':
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
            crop = "maize"
            confidence = 0.70
    elif season == 'rabi':
        if data['temperature'] < 20:
            crop = "wheat"
            confidence = 0.85
        elif data['ph'] > 7.0:
            crop = "barley"
            confidence = 0.75
        else:
            crop = "chickpea"
            confidence = 0.80
    else:  # zaid
        crop = "watermelon"
        confidence = 0.70
    
    # Generate enhanced explanations with previous crop and season analysis
    explanations = []
    
    # Season-specific explanations
    explanations.append(f"Season analysis: {crop} is suitable for {season} season cultivation")
    
    # Previous crop impact
    if previous_crop:
        explanations.append(f"Previous crop {previous_crop} considered in soil nutrient analysis")
        # Simple NPK adjustment logic for fallback
        if previous_crop.lower() in ['wheat', 'rice', 'maize']:
            explanations.append(f"Previous cereal crop {previous_crop} may have depleted soil nitrogen")
        elif previous_crop.lower() in ['soybean', 'chickpea', 'lentil']:
            explanations.append(f"Previous legume crop {previous_crop} likely improved soil nitrogen")
    
    # Environmental factors
    if data['rainfall'] > 1000:
        explanations.append(f"High rainfall ({data['rainfall']:.0f} mm) favors water-loving crops")
    elif data['rainfall'] < 300:
        explanations.append(f"Low rainfall ({data['rainfall']:.0f} mm) suggests drought-resistant crops")
    
    if data['temperature'] > 35:
        explanations.append(f"High temperature ({data['temperature']:.1f}°C) limits heat-sensitive crops")
    elif data['temperature'] < 15:
        explanations.append(f"Cool temperature ({data['temperature']:.1f}°C) favors temperate crops")
    
    if data['ph'] < 6.0:
        explanations.append(f"Acidic soil (pH {data['ph']:.1f}) suits acid-tolerant crops")
    elif data['ph'] > 7.5:
        explanations.append(f"Alkaline soil (pH {data['ph']:.1f}) requires alkali-tolerant varieties")
    
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
    
    # Enhanced response with previous crop and season analysis
    return {
        "recommended_crop": crop,
        "confidence": round(confidence, 3),
        "why": explanations[:4],  # Top 4 enhanced reasons
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
        # Enhanced fields for fallback
        "previous_crop_analysis": {
            "previous_crop": str(previous_crop) if previous_crop else "",
            "original_npk": [float(data['N']), float(data['P']), float(data['K'])],
            "adjusted_npk": [float(data['N']), float(data['P']), float(data['K'])],  # No adjustment in fallback
            "nutrient_impact": [0.0, 0.0, 0.0]  # No impact calculated in fallback
        },
        "season_analysis": {
            "detected_season": str(season) if season else "kharif",
            "season_suitability": "suitable" if season in ['kharif', 'rabi'] else "moderate",
            "season_explanation": f"{crop} is recommended for {season or 'kharif'} season based on climatic conditions"
        },
        "model_version": "rule_based_v2_enhanced",
        "timestamp": datetime.now().isoformat(),
        "area_analyzed_ha": area_ha,
        "region": data.get('region', 'default')
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

# Marketplace API Endpoints
@app.get("/marketplace/products")
async def get_marketplace_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    location: Optional[str] = None
):
    """Get marketplace products with optional filtering"""
    # Sample marketplace data
    products = [
        {
            "id": "1",
            "name": "Premium Rice Seeds (IR64)",
            "category": "seeds",
            "price": 120,
            "unit": "kg",
            "seller": "Green Valley Seeds",
            "location": "Punjab, India",
            "rating": 4.8,
            "reviews": 156,
            "inStock": True,
            "image": "🌾",
            "description": "High-yield IR64 rice variety suitable for kharif season",
            "priceChange": -2.5
        },
        {
            "id": "2",
            "name": "NPK Fertilizer (20:20:0)",
            "category": "fertilizer",
            "price": 850,
            "unit": "50kg bag",
            "seller": "FarmTech Solutions",
            "location": "Maharashtra, India",
            "rating": 4.6,
            "reviews": 89,
            "inStock": True,
            "image": "🌱",
            "description": "Balanced NPK fertilizer for optimal crop growth",
            "priceChange": 3.2
        },
        {
            "id": "3",
            "name": "Solar Water Pump",
            "category": "equipment",
            "price": 45000,
            "unit": "unit",
            "seller": "AgriTech India",
            "location": "Gujarat, India",
            "rating": 4.9,
            "reviews": 34,
            "inStock": True,
            "image": "⚡",
            "description": "5HP solar-powered water pump with 2-year warranty",
            "priceChange": -1.8
        }
    ]
    
    # Apply filters
    filtered_products = products
    
    if category and category != "all":
        filtered_products = [p for p in filtered_products if p["category"] == category]
    
    if search:
        search_lower = search.lower()
        filtered_products = [
            p for p in filtered_products 
            if search_lower in p["name"].lower() or search_lower in p["seller"].lower()
        ]
    
    if location:
        filtered_products = [
            p for p in filtered_products 
            if location.lower() in p["location"].lower()
        ]
    
    return filtered_products

@app.get("/marketplace/prices")
async def get_market_prices():
    """Get current market prices for major crops"""
    return [
        {
            "crop": "Rice",
            "currentPrice": 2100,
            "unit": "quintal",
            "change": 50,
            "changePercent": 2.4,
            "market": "Delhi Mandi",
            "lastUpdated": "2 hours ago"
        },
        {
            "crop": "Wheat",
            "currentPrice": 2050,
            "unit": "quintal",
            "change": -30,
            "changePercent": -1.4,
            "market": "Punjab Mandi",
            "lastUpdated": "1 hour ago"
        },
        {
            "crop": "Cotton",
            "currentPrice": 5800,
            "unit": "quintal",
            "change": 120,
            "changePercent": 2.1,
            "market": "Gujarat Mandi",
            "lastUpdated": "3 hours ago"
        }
    ]

@app.get("/marketplace/insights")
async def get_market_insights():
    """Get market insights and analytics data"""
    return [
        {
            "crop": "Rice",
            "demandTrend": "up",
            "priceProjection": 2250,
            "seasonalFactor": 1.15,
            "riskLevel": "low",
            "bestRegions": ["Punjab", "Haryana", "West Bengal"],
            "optimalTiming": "June - July"
        },
        {
            "crop": "Cotton",
            "demandTrend": "up",
            "priceProjection": 6200,
            "seasonalFactor": 1.25,
            "riskLevel": "medium",
            "bestRegions": ["Gujarat", "Maharashtra", "Andhra Pradesh"],
            "optimalTiming": "May - June"
        }
    ]

@app.post("/marketplace/orders")
async def place_order(order_data: dict):
    """Place a marketplace order"""
    # Validate order data
    required_fields = ["productId", "quantity", "deliveryAddress", "contactInfo"]
    for field in required_fields:
        if field not in order_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Generate order ID
    import uuid
    order_id = str(uuid.uuid4())[:8]
    
    return {
        "orderId": order_id,
        "status": "confirmed",
        "estimatedDelivery": "3-5 days",
        "trackingNumber": f"TRK{order_id.upper()}"
    }
    
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
    uvicorn.run("simple_app:app", host="localhost", port=8739, reload=True)
