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
        
        # Load class names from V3 model checkpoint (updated for Pepper, Potato, Tomato)
        class_names = [
            'Pepper__bell___Bacterial_spot',
            'Pepper__bell___healthy',
            'Potato___Early_blight',
            'Potato___healthy',
            'Potato___Late_blight',
            'Tomato__Target_Spot',
            'Tomato__Tomato_mosaic_virus',
            'Tomato__Tomato_YellowLeaf__Curl_Virus',
            'Tomato_Bacterial_spot',
            'Tomato_Early_blight',
            'Tomato_healthy',
            'Tomato_Late_blight',
            'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot',
            'Tomato_Spider_mites_Two_spotted_spider_mite'
        ]
        
        # Load trained model
        model_path = 'models/crop_disease_v3_model.pth'
        
        if os.path.exists(model_path):
            model = CropDiseaseResNet50(num_classes=len(class_names), pretrained=False)
            checkpoint = torch.load(model_path, map_location=device)
            
            # Handle checkpoint format from crop_disease_v3_model.pth
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                # Use class names from checkpoint if available
                if 'class_names' in checkpoint:
                    class_names = checkpoint['class_names']
            else:
                state_dict = checkpoint
            
            model.load_state_dict(state_dict, strict=True)
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
        
        # Parse crop and disease from class name (improved for V3 model formats)
        if '___' in predicted_class:
            parts = predicted_class.split('___')
            crop = parts[0]
            disease = parts[1]
        elif '__' in predicted_class:
            parts = predicted_class.split('__', 1)  # Split only on first occurrence
            crop = parts[0]
            disease = parts[1]
        elif '_' in predicted_class:
            parts = predicted_class.split('_', 1)  # Split only on first occurrence
            crop = parts[0]
            disease = parts[1]
        else:
            crop = "Unknown"
            disease = predicted_class
        
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
                    # Use the class_name field directly instead of constructing it
                    if d.get('class_name') == predicted_class:
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
            'predicted_class': predicted_class,
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
                
                if 'error' in explanation:
                    response['explanation'] = {
                        'error': explanation['error'],
                        'explanation_image': ''
                    }
                else:
                    response['explanation'] = {
                        'explanation_image': explanation.get('overlay_base64', ''),
                        'predicted_class': explanation.get('predicted_class', predicted_class),
                        'confidence': explanation.get('confidence', confidence_score),
                        'save_path': explanation.get('save_path', '')
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
        'crops': ['Pepper', 'Potato', 'Tomato']
    }

@app.get("/model_info")
async def get_model_info():
    """Get model architecture and training information"""
    return {
        'model_name': 'CropDiseaseResNet50',
        'architecture': 'ResNet50 with custom classifier',
        'input_size': [3, 224, 224],
        'num_classes': len(class_names),
        'device': str(device),
        'model_file': 'crop_disease_v3_model.pth',
        'features': {
            'backbone': 'ResNet50 (pretrained)',
            'classifier': 'Custom sequential layers with dropout',
            'grad_cam': 'Available for visual explanations',
            'risk_assessment': 'Multi-factor risk calculation'
        },
        'capabilities': [
            'Disease classification',
            'Visual explanations (Grad-CAM)',
            'Risk level assessment',
            'Treatment recommendations',
            'Batch processing'
        ]
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
    
    print("🌐 Starting server on http://localhost:4333")
    print("📖 API documentation available at http://localhost:4333/docs")

    uvicorn.run(app, host="localhost", port=4333)
