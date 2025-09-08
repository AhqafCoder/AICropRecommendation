"""
Dedicated Backend Server for Marketplace and Analytics
FastAPI backend with comprehensive agricultural marketplace features
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import uvicorn
from datetime import datetime, timedelta
import uuid
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="CropAI Marketplace & Analytics API",
    description="Comprehensive backend for agricultural marketplace and market insights",
    version="2.0.0",
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

# Data Models
class Product(BaseModel):
    id: str
    name: str
    category: str = Field(..., pattern="^(seeds|fertilizer|equipment|pesticide)$")
    price: float = Field(..., gt=0)
    unit: str
    seller: str
    location: str
    rating: float = Field(..., ge=0, le=5)
    reviews: int = Field(..., ge=0)
    inStock: bool = True
    image: str
    description: str
    priceChange: float
    sellerId: str
    dateAdded: str

class MarketPrice(BaseModel):
    crop: str
    currentPrice: float
    unit: str
    change: float
    changePercent: float
    market: str
    lastUpdated: str
    volume: int
    demandLevel: str

class OrderRequest(BaseModel):
    productId: str
    quantity: int = Field(..., gt=0)
    deliveryAddress: Dict[str, str]
    contactInfo: Dict[str, str]
    paymentMethod: str = "cod"
    specialInstructions: Optional[str] = None

class MarketInsight(BaseModel):
    crop: str
    demandTrend: str = Field(..., regex="^(up|down|stable)$")
    currentPrice: float
    projectedPrice: float
    seasonalFactor: float
    riskLevel: str = Field(..., regex="^(low|medium|high)$")
    bestRegions: List[str]
    optimalPlantingWindow: str
    marketShare: float
    confidence: float

class WeatherForecast(BaseModel):
    region: str
    temperature: Dict[str, float]
    rainfall: float
    humidity: float
    outlook: str = Field(..., regex="^(favorable|moderate|challenging)$")
    impact: str
    windSpeed: float
    uvIndex: int

class ProfitabilityInsight(BaseModel):
    crop: str
    investmentPerAcre: float
    expectedRevenuePerAcre: float
    profitMargin: float
    paybackPeriod: str
    riskFactor: float
    marketDemand: str
    seasonality: str

# Sample Data Storage (In production, use a proper database)
PRODUCTS_DB = [
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
        "description": "High-yield IR64 rice variety suitable for kharif season with excellent disease resistance",
        "priceChange": -2.5,
        "sellerId": "seller_001",
        "dateAdded": "2025-08-15"
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
        "description": "Balanced NPK fertilizer for optimal crop growth with slow-release formula",
        "priceChange": 3.2,
        "sellerId": "seller_002",
        "dateAdded": "2025-08-20"
    },
    {
        "id": "3",
        "name": "Solar Water Pump (5HP)",
        "category": "equipment",
        "price": 45000,
        "unit": "unit",
        "seller": "AgriTech India",
        "location": "Gujarat, India",
        "rating": 4.9,
        "reviews": 34,
        "inStock": True,
        "image": "⚡",
        "description": "5HP solar-powered water pump with 2-year warranty and free installation",
        "priceChange": -1.8,
        "sellerId": "seller_003",
        "dateAdded": "2025-08-10"
    },
    {
        "id": "4",
        "name": "Organic Pesticide (Neem Oil)",
        "category": "pesticide",
        "price": 320,
        "unit": "liter",
        "seller": "Bio Solutions",
        "location": "Karnataka, India",
        "rating": 4.7,
        "reviews": 78,
        "inStock": False,
        "image": "🛡️",
        "description": "Eco-friendly organic pesticide for crop protection without harmful chemicals",
        "priceChange": 0.5,
        "sellerId": "seller_004",
        "dateAdded": "2025-08-25"
    },
    {
        "id": "5",
        "name": "Wheat Seeds (PBW 343)",
        "category": "seeds",
        "price": 95,
        "unit": "kg",
        "seller": "Punjab Seeds Co.",
        "location": "Punjab, India",
        "rating": 4.5,
        "reviews": 203,
        "inStock": True,
        "image": "🌾",
        "description": "High-yielding wheat variety suitable for rabi season with good disease tolerance",
        "priceChange": 1.2,
        "sellerId": "seller_005",
        "dateAdded": "2025-09-01"
    }
]

MARKET_PRICES_DB = [
    {
        "crop": "Rice",
        "currentPrice": 2100,
        "unit": "quintal",
        "change": 50,
        "changePercent": 2.4,
        "market": "Delhi Mandi",
        "lastUpdated": "2 hours ago",
        "volume": 1250,
        "demandLevel": "high"
    },
    {
        "crop": "Wheat",
        "currentPrice": 2050,
        "unit": "quintal",
        "change": -30,
        "changePercent": -1.4,
        "market": "Punjab Mandi",
        "lastUpdated": "1 hour ago",
        "volume": 980,
        "demandLevel": "medium"
    },
    {
        "crop": "Cotton",
        "currentPrice": 5800,
        "unit": "quintal",
        "change": 120,
        "changePercent": 2.1,
        "market": "Gujarat Mandi",
        "lastUpdated": "3 hours ago",
        "volume": 750,
        "demandLevel": "high"
    },
    {
        "crop": "Sugarcane",
        "currentPrice": 320,
        "unit": "quintal",
        "change": 0,
        "changePercent": 0,
        "market": "UP Mandi",
        "lastUpdated": "4 hours ago",
        "volume": 560,
        "demandLevel": "low"
    },
    {
        "crop": "Maize",
        "currentPrice": 1850,
        "unit": "quintal",
        "change": 75,
        "changePercent": 4.2,
        "market": "Bihar Mandi",
        "lastUpdated": "1 hour ago",
        "volume": 890,
        "demandLevel": "medium"
    }
]

MARKET_INSIGHTS_DB = [
    {
        "crop": "Rice",
        "demandTrend": "up",
        "currentPrice": 2100,
        "projectedPrice": 2250,
        "seasonalFactor": 1.15,
        "riskLevel": "low",
        "bestRegions": ["Punjab", "Haryana", "West Bengal"],
        "optimalPlantingWindow": "June - July",
        "marketShare": 35.2,
        "confidence": 0.87
    },
    {
        "crop": "Cotton",
        "demandTrend": "up",
        "currentPrice": 5800,
        "projectedPrice": 6200,
        "seasonalFactor": 1.25,
        "riskLevel": "medium",
        "bestRegions": ["Gujarat", "Maharashtra", "Andhra Pradesh"],
        "optimalPlantingWindow": "May - June",
        "marketShare": 28.7,
        "confidence": 0.82
    },
    {
        "crop": "Wheat",
        "demandTrend": "stable",
        "currentPrice": 2050,
        "projectedPrice": 2100,
        "seasonalFactor": 1.05,
        "riskLevel": "low",
        "bestRegions": ["Punjab", "Uttar Pradesh", "Madhya Pradesh"],
        "optimalPlantingWindow": "November - December",
        "marketShare": 22.1,
        "confidence": 0.91
    },
    {
        "crop": "Sugarcane",
        "demandTrend": "down",
        "currentPrice": 320,
        "projectedPrice": 310,
        "seasonalFactor": 0.95,
        "riskLevel": "high",
        "bestRegions": ["Uttar Pradesh", "Maharashtra", "Karnataka"],
        "optimalPlantingWindow": "February - March",
        "marketShare": 14.0,
        "confidence": 0.75
    }
]

# API Routes
@app.get("/")
async def root():
    return {
        "message": "CropAI Marketplace & Analytics API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "marketplace": "/marketplace/*",
            "analytics": "/analytics/*",
            "predictions": "/predict"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "marketplace": "active",
            "analytics": "active",
            "database": "connected"
        }
    }

# Marketplace Endpoints
@app.get("/marketplace/products")
async def get_marketplace_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    min_rating: Optional[float] = None
):
    """Get marketplace products with comprehensive filtering"""
    
    filtered_products = PRODUCTS_DB.copy()
    
    # Apply filters
    if category and category != "all":
        filtered_products = [p for p in filtered_products if p["category"] == category]
    
    if search:
        search_lower = search.lower()
        filtered_products = [
            p for p in filtered_products 
            if (search_lower in p["name"].lower() or 
                search_lower in p["seller"].lower() or
                search_lower in p["description"].lower())
        ]
    
    if location:
        filtered_products = [
            p for p in filtered_products 
            if location.lower() in p["location"].lower()
        ]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]
    
    if in_stock is not None:
        filtered_products = [p for p in filtered_products if p["inStock"] == in_stock]
    
    if min_rating is not None:
        filtered_products = [p for p in filtered_products if p["rating"] >= min_rating]
    
    return {
        "products": filtered_products,
        "total": len(filtered_products),
        "filters_applied": {
            "category": category,
            "search": search,
            "location": location,
            "price_range": f"{min_price or 0} - {max_price or 'unlimited'}",
            "in_stock_only": in_stock,
            "min_rating": min_rating
        }
    }

@app.get("/marketplace/products/{product_id}")
async def get_product_details(product_id: str):
    """Get detailed information about a specific product"""
    product = next((p for p in PRODUCTS_DB if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "product": product,
        "related_products": [p for p in PRODUCTS_DB if p["category"] == product["category"] and p["id"] != product_id][:3],
        "seller_info": {
            "id": product["sellerId"],
            "name": product["seller"],
            "verified": True,
            "total_products": len([p for p in PRODUCTS_DB if p["sellerId"] == product["sellerId"]]),
            "average_rating": 4.7
        }
    }

@app.get("/marketplace/prices")
async def get_market_prices(crop: Optional[str] = None):
    """Get current market prices for crops"""
    prices = MARKET_PRICES_DB.copy()
    
    if crop:
        prices = [p for p in prices if crop.lower() in p["crop"].lower()]
    
    return {
        "prices": prices,
        "last_updated": datetime.now().isoformat(),
        "total_markets": len(set(p["market"] for p in prices))
    }

@app.post("/marketplace/orders")
async def place_order(order_request: OrderRequest):
    """Place a new order in the marketplace"""
    
    # Validate product exists
    product = next((p for p in PRODUCTS_DB if p["id"] == order_request.productId), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product["inStock"]:
        raise HTTPException(status_code=400, detail="Product is out of stock")
    
    # Generate order
    order_id = str(uuid.uuid4())[:8].upper()
    total_amount = product["price"] * order_request.quantity
    
    # Calculate delivery estimate
    delivery_date = datetime.now() + timedelta(days=3)
    
    order = {
        "orderId": order_id,
        "productId": order_request.productId,
        "productName": product["name"],
        "quantity": order_request.quantity,
        "unitPrice": product["price"],
        "totalAmount": total_amount,
        "status": "confirmed",
        "orderDate": datetime.now().isoformat(),
        "estimatedDelivery": delivery_date.strftime("%Y-%m-%d"),
        "trackingNumber": f"TRK{order_id}",
        "seller": product["seller"],
        "deliveryAddress": order_request.deliveryAddress,
        "contactInfo": order_request.contactInfo,
        "paymentMethod": order_request.paymentMethod
    }
    
    return order

# Analytics Endpoints
@app.get("/analytics/insights")
async def get_market_insights(
    crop: Optional[str] = None,
    risk_level: Optional[str] = None
):
    """Get comprehensive market insights and analytics"""
    
    insights = MARKET_INSIGHTS_DB.copy()
    
    if crop:
        insights = [i for i in insights if crop.lower() in i["crop"].lower()]
    
    if risk_level:
        insights = [i for i in insights if i["riskLevel"] == risk_level]
    
    return {
        "insights": insights,
        "summary": {
            "total_crops_analyzed": len(insights),
            "average_confidence": sum(i["confidence"] for i in insights) / len(insights) if insights else 0,
            "high_potential_crops": [i["crop"] for i in insights if i["demandTrend"] == "up" and i["riskLevel"] == "low"],
            "market_trends": {
                "upward": len([i for i in insights if i["demandTrend"] == "up"]),
                "stable": len([i for i in insights if i["demandTrend"] == "stable"]),
                "downward": len([i for i in insights if i["demandTrend"] == "down"])
            }
        }
    }

@app.get("/analytics/weather")
async def get_weather_insights():
    """Get weather forecasts and agricultural impact analysis"""
    
    weather_data = [
        {
            "region": "Punjab",
            "temperature": {"min": 25, "max": 35},
            "rainfall": 120,
            "humidity": 75,
            "outlook": "favorable",
            "impact": "Ideal conditions for rice cultivation with adequate rainfall",
            "windSpeed": 12.5,
            "uvIndex": 7
        },
        {
            "region": "Gujarat",
            "temperature": {"min": 28, "max": 38},
            "rainfall": 80,
            "humidity": 65,
            "outlook": "moderate",
            "impact": "Good for cotton cultivation with supplemental irrigation",
            "windSpeed": 8.3,
            "uvIndex": 9
        },
        {
            "region": "Maharashtra",
            "temperature": {"min": 22, "max": 32},
            "rainfall": 150,
            "humidity": 80,
            "outlook": "favorable",
            "impact": "Excellent conditions for multiple crop varieties",
            "windSpeed": 15.2,
            "uvIndex": 6
        },
        {
            "region": "Karnataka",
            "temperature": {"min": 20, "max": 30},
            "rainfall": 100,
            "humidity": 70,
            "outlook": "challenging",
            "impact": "Requires careful water management for optimal yields",
            "windSpeed": 11.8,
            "uvIndex": 8
        }
    ]
    
    return {
        "forecasts": weather_data,
        "regional_summary": {
            "favorable_regions": len([w for w in weather_data if w["outlook"] == "favorable"]),
            "average_rainfall": sum(w["rainfall"] for w in weather_data) / len(weather_data),
            "temperature_range": {
                "min": min(w["temperature"]["min"] for w in weather_data),
                "max": max(w["temperature"]["max"] for w in weather_data)
            }
        }
    }

@app.get("/analytics/profitability")
async def get_profitability_analysis():
    """Get crop profitability analysis and ROI calculations"""
    
    profitability_data = [
        {
            "crop": "Cotton",
            "investmentPerAcre": 25000,
            "expectedRevenuePerAcre": 45000,
            "profitMargin": 44.4,
            "paybackPeriod": "6 months",
            "riskFactor": 0.6,
            "marketDemand": "high",
            "seasonality": "kharif"
        },
        {
            "crop": "Rice",
            "investmentPerAcre": 18000,
            "expectedRevenuePerAcre": 28000,
            "profitMargin": 35.7,
            "paybackPeriod": "4 months",
            "riskFactor": 0.3,
            "marketDemand": "very high",
            "seasonality": "kharif"
        },
        {
            "crop": "Wheat",
            "investmentPerAcre": 15000,
            "expectedRevenuePerAcre": 22000,
            "profitMargin": 31.8,
            "paybackPeriod": "5 months",
            "riskFactor": 0.2,
            "marketDemand": "high",
            "seasonality": "rabi"
        },
        {
            "crop": "Sugarcane",
            "investmentPerAcre": 35000,
            "expectedRevenuePerAcre": 48000,
            "profitMargin": 27.1,
            "paybackPeriod": "12 months",
            "riskFactor": 0.8,
            "marketDemand": "medium",
            "seasonality": "annual"
        }
    ]
    
    return {
        "analysis": profitability_data,
        "recommendations": {
            "highest_roi": max(profitability_data, key=lambda x: x["profitMargin"])["crop"],
            "lowest_risk": min(profitability_data, key=lambda x: x["riskFactor"])["crop"],
            "fastest_payback": min(profitability_data, key=lambda x: int(x["paybackPeriod"].split()[0]))["crop"]
        }
    }

# Prediction endpoint (from original API)
@app.post("/predict")
async def predict_crop(data: dict):
    """Basic crop prediction endpoint for compatibility"""
    # This would integrate with your existing ML model
    return {
        "recommended_crop": "rice",
        "confidence": 0.85,
        "message": "This is a basic prediction. Use the marketplace API for comprehensive features."
    }

if __name__ == "__main__":
    print("🚀 Starting CropAI Marketplace & Analytics Server...")
    print("📊 Features: Marketplace, Analytics, Weather, Profitability")
    print("🌐 API Documentation: http://localhost:5000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=5000,
        reload=True,
        log_level="info"
    )
