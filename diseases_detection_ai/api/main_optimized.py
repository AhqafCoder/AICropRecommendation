"""
Memory-optimized FastAPI Backend for Crop Disease Detection
Optimized to use <512MB RAM
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
import gc
import psutil

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.model import CropDiseaseResNet50Lite
    from src.explain_lite import CropDiseaseExplainerLite
    from src.risk_level import RiskLevelCalculator
    from src.dataset import get_inference_transforms
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")

# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection API (Optimized)",
    description="Memory-optimized AI-powered crop disease detection",
    version="2.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
transforms = None

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # Convert to MB

def optimize_memory():
    """Force garbage collection and clear GPU cache"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def load_model_and_components():
    """Load trained model and initialize components with memory optimization"""
    global model, explainer, risk_calculator, class_names, device, transforms
    
    try:
        # Set device - prefer CPU for memory efficiency
        if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory > 2e9:
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')
        print(f"Using device: {device}")
        
        # Optimized class names (reduced set for memory efficiency)
        class_names = [
            'Pepper_Bacterial_spot',
            'Pepper_healthy',
            'Potato_Early_blight',
            'Potato_healthy',
            'Potato_Late_blight',
            'Tomato_Target_Spot',
            'Tomato_mosaic_virus',
            'Tomato_Yellow_Leaf_Curl',
            'Tomato_Bacterial_spot',
            'Tomato_Early_blight',
            'Tomato_healthy',
            'Tomato_Late_blight',
            'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot',
            'Tomato_Spider_mites'
        ]
        
        # Load model with memory optimization
        model_path = 'models/crop_disease_v3_model.pth'
        
        if os.path.exists(model_path):
            # Use lite version of model
            model = CropDiseaseResNet50Lite(num_classes=len(class_names), pretrained=False)
            
            # Load with memory mapping for large files
            checkpoint = torch.load(model_path, map_location=device, weights_only=True)
            
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                if 'class_names' in checkpoint:
                    class_names = checkpoint['class_names']
            else:
                state_dict = checkpoint
            
            # Load state dict and immediately clear checkpoint from memory
            model.load_state_dict(state_dict, strict=False)
            del checkpoint, state_dict
            optimize_memory()
            
            model.to(device)
            model.eval()
            
            # Enable memory efficient mode
            if hasattr(model, 'set_memory_efficient'):
                model.set_memory_efficient(True)
            
            print(f"Lite model loaded from {model_path}")
        else:
            print("Warning: No trained model found. Creating lite model.")
            model = CropDiseaseResNet50Lite(num_classes=len(class_names), pretrained=True)
            model.to(device)
            model.eval()
        
        # Initialize lite explainer only if needed
        explainer = CropDiseaseExplainerLite(model, class_names, device)
        print("Lite explainer initialized")
        
        # Initialize risk calculator
        risk_calculator = RiskLevelCalculator()
        print("Risk calculator initialized")
        
        # Pre-load transforms
        transforms = get_inference_transforms(input_size=224)
        
        # Force memory cleanup
        optimize_memory()
        
        memory_usage = get_memory_usage()
        print(f"Memory usage after loading: {memory_usage:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"Error loading model and components: {e}")
        traceback.print_exc()
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    print("Starting optimized disease detection API...")
    success = load_model_and_components()
    if success:
        print("✅ All components loaded successfully")
    else:
        print("⚠️ Failed to load some components")

@app.get("/")
async def root():
    """Root endpoint"""
    memory_usage = get_memory_usage()
    return {
        "message": "Crop Disease Detection API (Optimized)",
        "version": "2.1.0",
        "status": "active",
        "memory_usage_mb": f"{memory_usage:.1f}",
        "optimization": "Memory optimized for <512MB usage",
        "endpoints": {
            "predict": "/predict - POST with image file",
            "health": "/health - GET for health check",
            "memory": "/memory - GET memory usage info"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with memory info"""
    memory_usage = get_memory_usage()
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "explainer_loaded": explainer is not None,
        "device": str(device) if device else "unknown",
        "memory_usage_mb": f"{memory_usage:.1f}",
        "memory_optimized": memory_usage < 512
    }

@app.get("/memory")
async def memory_info():
    """Get detailed memory usage information"""
    memory_usage = get_memory_usage()
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return {
        "memory_usage_mb": f"{memory_usage:.1f}",
        "memory_percent": f"{process.memory_percent():.1f}%",
        "rss_mb": f"{memory_info.rss / 1024 / 1024:.1f}",
        "vms_mb": f"{memory_info.vms / 1024 / 1024:.1f}",
        "available_memory_mb": f"{psutil.virtual_memory().available / 1024 / 1024:.1f}",
        "gpu_memory_allocated": f"{torch.cuda.memory_allocated() / 1024 / 1024:.1f}" if torch.cuda.is_available() else "N/A",
        "optimization_status": "Optimized" if memory_usage < 512 else "Needs optimization"
    }

@app.post("/predict")
async def predict_disease(
    file: UploadFile = File(...),
    include_explanation: bool = Form(False),
    weather_humidity: Optional[float] = Form(None),
    weather_temperature: Optional[float] = Form(None),
    weather_rainfall: Optional[float] = Form(None)
):
    """
    Predict plant disease from uploaded image (memory optimized)
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Memory optimization: track usage
        initial_memory = get_memory_usage()
        
        # Read and validate image with memory limits
        contents = await file.read()
        if len(contents) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(status_code=413, detail="Image too large. Maximum size: 5MB")
        
        # Process image with memory optimization
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to reduce memory usage
        max_size = 224
        if image.size[0] > max_size or image.size[1] > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Apply transforms
        if transforms is None:
            transforms_fn = get_inference_transforms(input_size=224)
        else:
            transforms_fn = transforms
            
        input_tensor = transforms_fn(image).unsqueeze(0).to(device)
        
        # Clear image from memory
        del image, contents
        optimize_memory()
        
        # Prediction with memory optimization
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_class = class_names[predicted_idx.item()]
            confidence_score = confidence.item()
        
        # Get class probabilities (top 3 only to save memory)
        class_probs = {}
        top_probs, top_indices = torch.topk(probabilities[0], min(3, len(class_names)))
        for i, (prob, idx) in enumerate(zip(top_probs, top_indices)):
            class_probs[class_names[idx.item()]] = prob.item()
        
        # Clear tensors
        del input_tensor, outputs, probabilities
        optimize_memory()
        
        # Load disease information efficiently
        disease_info = get_disease_info_lite(predicted_class)
        
        # Calculate risk assessment
        weather_data = {}
        if weather_humidity is not None:
            weather_data['humidity'] = weather_humidity
        if weather_temperature is not None:
            weather_data['temperature'] = weather_temperature
        if weather_rainfall is not None:
            weather_data['rainfall'] = weather_rainfall
        
        risk_assessment = risk_calculator.calculate_risk(
            predicted_class, confidence_score, weather_data
        ) if risk_calculator else {"overall_risk": "unknown", "risk_factors": [], "recommendations": []}
        
        # Generate explanation only if requested and memory allows
        explanation_data = {}
        current_memory = get_memory_usage()
        
        if include_explanation and current_memory < 400 and explainer:  # Only if we have memory headroom
            try:
                explanation_data = explainer.generate_explanation_lite(
                    await file.read(), predicted_class
                )
            except Exception as e:
                print(f"Explanation generation failed: {e}")
                explanation_data = {"error": "Explanation unavailable due to memory constraints"}
        elif include_explanation:
            explanation_data = {"error": "Explanation disabled due to memory constraints"}
        
        # Final memory cleanup
        optimize_memory()
        final_memory = get_memory_usage()
        
        # Prepare response
        result = {
            "predicted_class": predicted_class,
            "confidence": confidence_score,
            "class_probabilities": class_probs,
            "disease_info": disease_info,
            "risk_assessment": risk_assessment,
            "crop": extract_crop_name(predicted_class),
            "memory_usage": {
                "initial_mb": f"{initial_memory:.1f}",
                "final_mb": f"{final_memory:.1f}",
                "memory_optimized": final_memory < 512
            }
        }
        
        if explanation_data:
            result["explanation"] = explanation_data
        
        return JSONResponse(content=result)
        
    except Exception as e:
        # Cleanup on error
        optimize_memory()
        print(f"Prediction error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

def get_disease_info_lite(disease_class: str) -> Dict[str, Any]:
    """Get disease information with memory optimization"""
    try:
        # Load only essential disease info to save memory
        knowledge_base_path = Path(__file__).parent.parent / "knowledge_base" / "disease_info.json"
        
        if knowledge_base_path.exists():
            with open(knowledge_base_path, 'r') as f:
                all_disease_info = json.load(f)
            
            # Get specific disease info
            disease_info = all_disease_info.get(disease_class, {})
            
            # Return only essential fields to save memory
            return {
                "symptoms": disease_info.get("symptoms", [])[:3],  # Limit to 3 symptoms
                "solutions": disease_info.get("solutions", [])[:3],  # Limit to 3 solutions
                "prevention": disease_info.get("prevention", [])[:3],  # Limit to 3 prevention methods
                "description": disease_info.get("description", "No description available")[:200]  # Truncate description
            }
    except Exception as e:
        print(f"Error loading disease info: {e}")
    
    return {
        "symptoms": ["Symptoms information unavailable"],
        "solutions": ["Please consult agricultural expert"],
        "prevention": ["Follow general plant care guidelines"],
        "description": "Disease information unavailable"
    }

def extract_crop_name(disease_class: str) -> str:
    """Extract crop name from disease class"""
    if disease_class.startswith(('Pepper', 'pepper')):
        return "Pepper"
    elif disease_class.startswith(('Potato', 'potato')):
        return "Potato"
    elif disease_class.startswith(('Tomato', 'tomato')):
        return "Tomato"
    else:
        return "Unknown"

if __name__ == "__main__":
    import uvicorn
    
    print("Starting memory-optimized disease detection API...")
    print("Target: <512MB RAM usage")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        workers=1,  # Single worker to save memory
        limit_concurrency=2  # Limit concurrent requests
    )