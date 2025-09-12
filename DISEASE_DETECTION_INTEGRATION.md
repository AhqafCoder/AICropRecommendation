# 🌱 Disease Detection Integration Guide

This guide explains how to integrate the Crop Disease Detection AI with the frontend application through direct API communication.

## 🏗️ Architecture Overview

```
Frontend (Next.js)  →  Disease Detection API (FastAPI)  →  AI Model (PyTorch)
     Port 3000              Port 8001                    GPU/CPU Processing
```

**Direct Integration Benefits:**
- ✅ No intermediate backend complexity
- ✅ Real-time AI processing
- ✅ Simplified architecture
- ✅ Better performance for AI tasks
- ✅ Easy to scale AI service independently

## 🚀 Quick Start

### 1. Start the Disease Detection API Server

**Windows:**
```bash
cd diseases_detection_ai
python api/main.py
```

**Or use the batch file:**
```bash
.\start_disease_api.bat
```

**Linux/Mac:**
```bash
cd diseases_detection_ai
python api/main.py
```

**Or use the shell script:**
```bash
./start_disease_api.sh
```

### 2. Start the Frontend Application

```bash
cd client
npm run dev
```

### 3. Test the Integration

1. Open your browser to `http://localhost:3000`
2. Navigate to the Disease Detection page
3. Upload a plant leaf image
4. Get AI-powered disease detection results!

## 📡 API Endpoints

The Disease Detection API runs on `http://localhost:8001` with the following endpoints:

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check API and model status |
| `/predict` | POST | Single image disease detection |
| `/batch_predict` | POST | Multiple image processing |
| `/classes` | GET | Get supported disease classes |
| `/disease_info/{crop}/{disease}` | GET | Get disease information |

### API Documentation

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

## 🔧 Frontend Integration Details

### Disease Detection Service (`client/src/lib/diseaseApi.ts`)

```typescript
import { diseaseApi } from '@/lib/diseaseApi';

// Detect disease from image
const result = await diseaseApi.detectDisease(imageFile, {
  includeExplanation: true,
  weatherHumidity: 70,
  weatherTemperature: 25
});
```

### React Component (`client/src/components/DiseaseDetection.tsx`)

The component provides:
- ✅ Image upload with validation
- ✅ Real-time API status monitoring
- ✅ Progress indicators during processing
- ✅ Comprehensive result display
- ✅ Error handling and retry mechanisms

## 📊 Response Format

```json
{
  "predicted_class": "Tomato_Early_blight",
  "crop": "Tomato",
  "confidence": 0.92,
  "risk_assessment": {
    "overall_risk": "Medium",
    "risk_factors": ["High humidity conditions", "Warm temperature"],
    "recommendations": ["Apply fungicide", "Improve ventilation"]
  },
  "disease_info": {
    "description": "Early blight is a fungal disease...",
    "symptoms": ["Dark spots on leaves", "Yellow halos"],
    "solutions": ["Remove affected leaves", "Apply copper fungicide"],
    "prevention": ["Proper spacing", "Avoid overhead watering"]
  },
  "explanation": {
    "heatmap_available": true,
    "attention_regions": ["Leaf edges", "Spot centers"]
  },
  "class_probabilities": {
    "Tomato_Early_blight": 0.92,
    "Tomato_Late_blight": 0.05,
    "Tomato_healthy": 0.03
  }
}
```

## ⚙️ Configuration

### Environment Variables

Add to `client/.env.local`:
```bash
# Disease Detection API
NEXT_PUBLIC_DISEASE_API_URL=http://localhost:8001

# For production
# NEXT_PUBLIC_DISEASE_API_URL=https://your-disease-api-domain.com
```

### API Service Configuration

The `diseaseApi` service automatically:
- ✅ Validates image files (type, size, format)
- ✅ Handles timeout and error scenarios
- ✅ Formats responses for frontend consumption
- ✅ Provides health checking capabilities

## 🔍 Features

### Image Processing
- **Supported formats:** JPEG, PNG, BMP, TIFF
- **Maximum size:** 10MB per image
- **Batch processing:** Up to 10 images
- **Real-time validation:** Client-side checks before upload

### AI Model Features
- **Architecture:** ResNet50 with transfer learning
- **Classes:** 17 disease classes across 3 crops
- **Confidence scoring:** Probability-based predictions
- **Visual explanations:** Grad-CAM heatmaps
- **Risk assessment:** Multi-factor analysis

### Frontend Features
- **Real-time status:** API connection monitoring
- **Progressive loading:** Step-by-step processing indicators
- **Error handling:** Graceful degradation and retry options
- **Responsive design:** Mobile and desktop optimized
- **Accessibility:** Screen reader compatible

## 🛠️ Troubleshooting

### Common Issues

**1. API Connection Failed**
```
Error: Disease Detection service unavailable
```
**Solution:** 
- Check if the disease API server is running on port 8001
- Verify the NEXT_PUBLIC_DISEASE_API_URL environment variable
- Check firewall settings

**2. Model Not Loaded**
```
Error: Model not loaded
```
**Solution:**
- Ensure the model file exists at `diseases_detection_ai/models/crop_disease_v3_model.pth`
- Check Python dependencies are installed
- Verify PyTorch installation

**3. Image Upload Issues**
```
Error: Unsupported image format
```
**Solution:**
- Use JPEG, PNG, BMP, or TIFF format
- Ensure image size is under 10MB
- Check image file is not corrupted

### Debug Commands

```bash
# Check API health
curl http://localhost:8001/health

# Test image upload
curl -X POST "http://localhost:8001/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_leaf_sample.jpg"

# Check supported classes
curl http://localhost:8001/classes
```

## 📈 Performance Optimization

### API Server Optimization
- **GPU acceleration:** Automatic CUDA detection
- **Model caching:** Pre-loaded models for fast inference
- **Request queuing:** Handle concurrent requests
- **Response compression:** Optimized payload sizes

### Frontend Optimization
- **Image compression:** Client-side optimization before upload
- **Lazy loading:** Components loaded on demand
- **Caching:** API responses cached for repeated requests
- **Progressive enhancement:** Graceful degradation when offline

## 🔐 Security Considerations

### API Security
- **CORS configuration:** Properly configured for production
- **Input validation:** Server-side image validation
- **Rate limiting:** Prevent abuse (implement if needed)
- **Error handling:** No sensitive information in error messages

### Frontend Security
- **Input sanitization:** File type and size validation
- **Error boundaries:** Graceful error handling
- **Environment variables:** Secure API URL configuration

## 🚀 Production Deployment

### Disease Detection API
1. Deploy to cloud service (AWS, GCP, Azure)
2. Configure GPU instances for better performance
3. Set up load balancing for high availability
4. Configure monitoring and logging

### Frontend Configuration
1. Update `NEXT_PUBLIC_DISEASE_API_URL` to production URL
2. Enable production optimizations
3. Configure CDN for static assets
4. Set up error tracking

## 📝 API Usage Examples

### JavaScript/TypeScript
```typescript
import { diseaseApi } from '@/lib/diseaseApi';

// Basic detection
const result = await diseaseApi.detectDisease(imageFile);

// With weather data
const result = await diseaseApi.detectDisease(imageFile, {
  weatherHumidity: 75,
  weatherTemperature: 28,
  weatherRainfall: 120,
  growthStage: 'flowering'
});

// Batch processing
const results = await diseaseApi.batchDetectDisease([file1, file2, file3]);
```

### Python
```python
import requests

# Health check
response = requests.get('http://localhost:8001/health')
print(response.json())

# Image prediction
with open('leaf_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8001/predict', files=files)
    result = response.json()
```

### cURL
```bash
# Single prediction
curl -X POST "http://localhost:8001/predict" \
  -F "file=@leaf_image.jpg" \
  -F "include_explanation=true" \
  -F "weather_humidity=70"

# Get disease classes
curl "http://localhost:8001/classes"
```

## 🎯 Next Steps

1. **Test the integration** with various plant images
2. **Monitor API performance** during usage
3. **Implement additional features** like batch processing UI
4. **Add weather data integration** for enhanced risk assessment
5. **Deploy to production** with proper scaling configuration

## 📞 Support

For issues with the integration:
1. Check the troubleshooting section above
2. Review API logs at `diseases_detection_ai/logs/`
3. Test individual components separately
4. Check the comprehensive error messages in the frontend

**Happy crop disease detection! 🌱🔍**