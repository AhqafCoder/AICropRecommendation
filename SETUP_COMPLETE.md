# 🌾 Crop AI System - Quick Setup Guide

## ✅ Current Status
Your frontend and AI server are now **successfully connected**! 

## 🚀 How to Start Both Services

### Method 1: Automated Start (Recommended)

**Start AI Server:**
```bash
cd ai_v2
start_api_server.bat
```

**Start Frontend (in another terminal):**
```bash
cd client
npm run dev
```

### Method 2: Manual Start

**Terminal 1 - AI Server:**
```bash
cd ai_v2
.\venv\Scripts\Activate.ps1
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

## 🌐 Access Points

- **Main Application**: http://localhost:3000/recommend
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 What's Working

✅ **AI Backend (Port 8000)**
- FastAPI server with auto-reload
- ML models loaded successfully
- Input validation and error handling
- CORS enabled for frontend connection

✅ **Next.js Frontend (Port 3000)**
- React-based recommendation form
- Real-time input validation
- API integration with proper error handling
- Responsive design

✅ **Integration**
- Frontend → Next.js API Route → Python AI Backend
- Proper data flow and error handling
- Type-safe interfaces
- Performance optimized

## 🎯 Test the Integration

1. Open http://localhost:3000/recommend
2. Fill in the soil and climate data
3. Click "Get Crop Recommendation"
4. See AI-powered results with:
   - Recommended crop
   - Confidence score
   - Expected yield
   - Profit analysis
   - Fertilizer recommendations
   - AI explanations

## 🐛 Troubleshooting

**If AI server won't start:**
```bash
cd ai_v2
pip install fastapi uvicorn pydantic
python api_server.py
```

**If frontend has connection issues:**
- Check that .env.local has `AI_BACKEND_URL=http://localhost:8000`
- Verify both servers are running
- Check browser console for errors

**If models aren't loading:**
- The system has fallback predictions that work without trained models
- For full functionality, ensure model files are in ai_v2/models/

## 📝 API Examples

**Direct API Test:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.5, "humidity": 82,
    "ph": 6.5, "rainfall": 200,
    "area_ha": 1.0, "region": "default",
    "season": "kharif"
  }'
```

**Frontend API Test:**
```bash
curl -X POST "http://localhost:3000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.5, "humidity": 82,
    "ph": 6.5, "rainfall": 200,
    "area_ha": 1.0, "region": "default",
    "season": "kharif"
  }'
```

## 🎉 Success!

Your Crop AI Recommendation System is now fully operational with:
- Modern React frontend
- Powerful FastAPI backend  
- Advanced ML predictions
- Professional UI/UX
- Production-ready architecture

Happy farming! 🚜🌱