"""
FastAPI Backend for Crop Disease Detection
Provides REST API endpoints for disease prediction with visual explanations
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import torch.nn.functional as F
from PIL import Image
import io
import json
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile
import traceback

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.model import CropDiseaseResNet50
    from src.explain import CropDiseaseExplainer
    from src.risk_level import RiskLevelCalculator
    from src.dataset import get_transforms
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")

# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection API",
    description="AI-powered crop disease detection with visual explanations",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and components
model = None
explainer = None
risk_calculator = None
class_names = []
device = None

def load_model_and_components():
    """Load trained model and initialize components"""
    global model, explainer, risk_calculator, class_names, device
    
    try:
        # Set device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # Load class names (from dataset or predefined)
        class_names = [
            'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
            'Corn___Common_rust',
            'Corn___healthy',
            'Corn___Northern_Leaf_Blight',
            'Potato___Early_Blight',
            'Potato___healthy',
            'Potato___Late_Blight',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___healthy',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites_Two_spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
        ]
        
        # Load trained model
        model_path = 'models/crop_disease_v2_model.pth'
        if not os.path.exists(model_path):
            model_path = 'models/crop_disease_resnet50.pth'
        
        if os.path.exists(model_path):
            model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=False)
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.to(device)
            model.eval()
            print(f"Model loaded from {model_path}")
        else:
            print("Warning: No trained model found. Creating untrained model for API structure.")
            model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=True)
            model.to(device)
            model.eval()
        
        # Initialize explainer
        explainer = CropDiseaseExplainer(model, class_names, device)
        print("Explainer initialized")
        
        # Initialize risk calculator
        risk_calculator = RiskLevelCalculator()
        print("Risk calculator initialized")
        
        return True
        
    except Exception as e:
        print(f"Error loading model and components: {e}")
        traceback.print_exc()
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    success = load_model_and_components()
    if not success:
        print("Warning: Failed to load some components. API may have limited functionality.")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Crop Disease Detection API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": {
            "predict": "/predict - POST with image file",
            "health": "/health - GET for health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "explainer_ready": explainer is not None,
        "risk_calculator_ready": risk_calculator is not None,
        "device": str(device) if device else "unknown",
        "classes": len(class_names)
    }

@app.post("/predict")
async def predict_disease(
    file: UploadFile = File(...),
    include_explanation: bool = Form(True),
    weather_humidity: Optional[float] = Form(None),
    weather_temperature: Optional[float] = Form(None),
    weather_rainfall: Optional[float] = Form(None),
    growth_stage: Optional[str] = Form(None)
):
    """
    Predict crop disease from uploaded image
    
    Args:
        file: Uploaded image file
        include_explanation: Whether to include Grad-CAM explanation
        weather_humidity: Optional humidity percentage
        weather_temperature: Optional temperature in Celsius
        weather_rainfall: Optional rainfall in mm
        growth_stage: Optional crop growth stage
    
    Returns:
        JSON response with prediction, risk assessment, and explanation
    """
    
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess image
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_class = class_names[predicted_idx.item()]
            confidence_score = confidence.item()
        
        # Get all class probabilities
        class_probabilities = {
            class_names[i]: probabilities[0, i].item() 
            for i in range(len(class_names))
        }
        
        # Parse crop and disease from class name
        parts = predicted_class.split('___')
        crop = parts[0] if len(parts) > 0 else "Unknown"
        disease = parts[1] if len(parts) > 1 else predicted_class
        
        # Calculate risk level
        weather_data = None
        if any([weather_humidity, weather_temperature, weather_rainfall]):
            weather_data = {
                'humidity': weather_humidity or 50,
                'temperature': weather_temperature or 25,
                'rainfall': weather_rainfall or 0
            }
        
        risk_assessment = risk_calculator.calculate_enhanced_risk(
            predicted_class, confidence_score, weather_data, growth_stage
        )
        
        # Load disease information
        disease_info = {}
        try:
            with open('knowledge_base/disease_info.json', 'r') as f:
                kb_data = json.load(f)
                for d in kb_data['diseases']:
                    if f"{d['crop']}___{d['disease']}" == predicted_class:
                        disease_info = {
                            'description': d['description'],
                            'symptoms': d['symptoms'],
                            'solutions': d['solutions'],
                            'prevention': d['prevention']
                        }
                        break
        except Exception as e:
            print(f"Error loading disease info: {e}")
        
        # Prepare response
        response = {
            'crop': crop,
            'disease': disease,
            'confidence': confidence_score,
            'risk_level': risk_assessment['risk_level'],
            'class_probabilities': class_probabilities,
            'risk_assessment': risk_assessment,
            'disease_info': disease_info,
            'prediction_timestamp': risk_assessment['assessment_timestamp']
        }
        
        # Generate visual explanation if requested
        if include_explanation and explainer:
            try:
                # Save temporary image file
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                    image.save(tmp_file.name)
                    tmp_path = tmp_file.name
                
                # Generate explanation
                explanation = explainer.explain_prediction(
                    tmp_path, return_base64=True
                )
                
                response['explanation'] = {
                    'explanation_image': explanation.get('explanation_image_base64', ''),
                    'heatmap_analysis': explanation.get('heatmap_regions', {}),
                    'attention_summary': f"Model focused on {explanation.get('heatmap_regions', {}).get('important_region_ratio', 0):.1%} of the image"
                }
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                print(f"Error generating explanation: {e}")
                response['explanation'] = {
                    'error': 'Could not generate visual explanation',
                    'explanation_image': ''
                }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/batch_predict")
async def batch_predict(files: list[UploadFile] = File(...)):
    """
    Predict diseases for multiple images
    
    Args:
        files: List of uploaded image files
    
    Returns:
        JSON response with predictions for all images
    """
    
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
    
    try:
        predictions = []
        
        for i, file in enumerate(files):
            if not file.content_type.startswith('image/'):
                predictions.append({
                    'filename': file.filename,
                    'error': 'Invalid file type'
                })
                continue
            
            try:
                # Process individual image
                image_data = await file.read()
                image = Image.open(io.BytesIO(image_data)).convert('RGB')
                
                # Make prediction (simplified for batch processing)
                from torchvision import transforms
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                
                input_tensor = transform(image).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probabilities = F.softmax(outputs, dim=1)
                    confidence, predicted_idx = torch.max(probabilities, 1)
                    
                    predicted_class = class_names[predicted_idx.item()]
                    confidence_score = confidence.item()
                
                # Calculate basic risk
                risk_level = risk_calculator.calculate_base_risk(predicted_class, confidence_score)
                
                predictions.append({
                    'filename': file.filename,
                    'predicted_class': predicted_class,
                    'confidence': confidence_score,
                    'risk_level': risk_level
                })
                
            except Exception as e:
                predictions.append({
                    'filename': file.filename,
                    'error': str(e)
                })
        
        # Generate summary
        summary = risk_calculator.get_risk_summary([
            p for p in predictions if 'error' not in p
        ])
        
        return JSONResponse(content={
            'predictions': predictions,
            'summary': summary,
            'total_processed': len(files),
            'successful_predictions': len([p for p in predictions if 'error' not in p])
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Get list of supported disease classes"""
    return {
        'classes': class_names,
        'total_classes': len(class_names),
        'crops': ['Corn', 'Potato', 'Tomato']
    }

@app.get("/disease_info/{crop}/{disease}")
async def get_disease_info(crop: str, disease: str):
    """Get detailed information about a specific disease"""
    
    try:
        with open('knowledge_base/disease_info.json', 'r') as f:
            kb_data = json.load(f)
            
        for d in kb_data['diseases']:
            if d['crop'].lower() == crop.lower() and d['disease'].lower() == disease.lower():
                return d
        
        raise HTTPException(status_code=404, detail="Disease information not found")
        
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Knowledge base not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving disease info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Crop Disease Detection API...")
    print("📊 Loading model and components...")
    
    # Load components
    success = load_model_and_components()
    if success:
        print("✅ All components loaded successfully!")
    else:
        print("⚠️ Some components failed to load")
    
    print("🌐 Starting server on http://localhost:8000")
    print("📖 API documentation available at http://localhost:8000/docs")
    
    uvicorn.run(app, host="localhost", port=8000)
