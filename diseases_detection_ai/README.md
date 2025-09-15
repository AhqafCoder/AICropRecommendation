# Crop Disease Detection AI 🌱🔍

> **Advanced Computer Vision System for Agricultural Disease Detection**

This folder contains a state-of-the-art PyTorch-based deep learning system for detecting diseases in crop images using ResNet50 architecture with comprehensive visual explanations and real-time risk assessment.

## 🚀 Key Features

- **Multi-Crop Disease Detection**: Supports Pepper (Bell), Potato, and Tomato crops
- **15 Disease Classes**: Comprehensive coverage of common agricultural diseases
- **Visual AI Explanations**: Grad-CAM and LIME explanations for prediction transparency
- **FastAPI Backend**: High-performance RESTful API with real-time predictions
- **High Accuracy**: 90.09% test accuracy on validation dataset (v3.0 model)
- **Risk Assessment**: Automated severity scoring and treatment recommendations
- **Memory Optimized**: Multiple model variants for different deployment scenarios
- **Production Ready**: Docker support, comprehensive testing, and monitoring

## 🧠 AI Model Architecture

### Core Model: Enhanced ResNet50
- **Base Architecture**: Pre-trained ResNet50 on ImageNet with custom classifier head
- **Fine-tuning**: Specialized transfer learning for agricultural disease detection
- **Input Specifications**: 224x224 RGB images, normalized with ImageNet statistics
- **Output**: 15-class disease classification with confidence scores
- **Model Depth**: 50 layers with residual connections for stable training

### Advanced Architecture Details
```
ResNet50 Feature Extractor (frozen/unfrozen)
├── Custom Classifier Head:
│   ├── Dropout(0.5)
│   ├── Linear(2048 → 1024) + BatchNorm + ReLU
│   ├── Dropout(0.3)
│   ├── Linear(1024 → 512) + BatchNorm + ReLU
│   ├── Dropout(0.2)
│   └── Linear(512 → 15) [Output Layer]
```

### Model Versions & Performance
- **v3.0** (Current): Retrained ResNet50 - 90.09% test accuracy
- **v2.0**: Enhanced feature extraction - 87.5% accuracy
- **v1.0**: Initial baseline model - 85.2% accuracy
- **Lite Variants**: Memory-optimized models for edge deployment

## 📊 Supported Disease Classes

### Pepper (Bell) - 2 Classes
1. **Bacterial Spot** - Xanthomonas infection
2. **Healthy** - No disease detected

### Potato - 3 Classes
1. **Early Blight** - Alternaria solani
2. **Late Blight** - Phytophthora infestans
3. **Healthy** - No disease detected

### Tomato - 10 Classes
1. **Bacterial Spot** - Xanthomonas perforans
2. **Early Blight** - Alternaria solani
3. **Late Blight** - Phytophthora infestans
4. **Leaf Mold** - Passalora fulva
5. **Septoria Leaf Spot** - Septoria lycopersici
6. **Spider Mites (Two-spotted)** - Tetranychus urticae
7. **Target Spot** - Corynespora cassiicola
8. **Yellow Leaf Curl Virus** - Begomovirus
9. **Mosaic Virus** - Tobacco mosaic virus
10. **Healthy** - No disease detected

## 🔧 Tech Stack

### Core AI/ML
- **Deep Learning**: PyTorch 2.1.0, TorchVision 0.16.0
- **Computer Vision**: OpenCV 4.8.1, PIL (Pillow) 10.0.1
- **Model Architecture**: ResNet50 with custom classification head

### API & Backend
- **Web Framework**: FastAPI 0.104.1 with async support
- **API Documentation**: Automatic OpenAPI/Swagger generation
- **CORS Support**: Configurable cross-origin resource sharing

### AI Explainability
- **Grad-CAM**: Gradient-weighted Class Activation Mapping
- **LIME**: Local Interpretable Model-agnostic Explanations
- **Custom Visualization**: matplotlib, seaborn for result plotting

### Data Processing
- **Numerical**: NumPy 1.24.3, Pandas 2.0.3
- **Image Processing**: Albumentations for augmentation
- **Serialization**: JSON, Pickle for model and data handling

## 📁 Project Structure

```
diseases_detection_ai/
├── main.py                 # FastAPI application entry point (477 lines)
├── requirements.txt        # Python dependencies and versions
├── README.md              # Comprehensive documentation (405 lines)
├── api/                   # API implementations
│   ├── main.py           # Main API server with full features
│   ├── main_optimized.py # Memory-optimized API variant
│   ├── Dockerfile        # Container configuration for deployment
│   ├── requirements.txt  # API-specific dependencies
│   └── __init__.py       # Package initialization
├── src/                   # Core AI modules (10 files)
│   ├── model.py          # ResNet50 model architecture (193 lines)
│   ├── model_lite.py     # Lightweight model variants for edge deployment
│   ├── explain.py        # Grad-CAM visual explanation system
│   ├── explain_lite.py   # Optimized explanation for mobile
│   ├── explain_new.py    # Latest explanation implementations
│   ├── dataset.py        # Data loading, preprocessing, and augmentation
│   ├── train.py          # Complete model training pipeline
│   ├── evaluate.py       # Model evaluation and metrics calculation
│   ├── risk_level.py     # Disease severity assessment algorithms
│   └── __init__.py       # Package initialization
├── models/               # Trained model checkpoints
│   ├── crop_disease_v3_model.pth  # Latest model (v3.0) - Primary
│   ├── crop_disease_v2_model.pth  # Previous stable version
│   ├── crop_disese_v0.pth        # Initial baseline model
│   ├── README.txt        # Model information and usage notes
│   └── .gitattributes    # Git LFS configuration for large files
├── knowledge_base/       # Disease information database
│   └── disease_info.json # Comprehensive disease database (552 lines)
├── data/                 # Training and test datasets
│   ├── raw/             # Original dataset images
│   └── processed/       # Preprocessed and augmented data
├── notebooks/            # Jupyter analysis and research notebooks
├── outputs/              # Generated visualizations and results
├── tests/               # Comprehensive testing suite
│   ├── test_model.py    # Model functionality tests
│   ├── test_api.py      # API endpoint testing
│   └── test_explain.py  # Explanation system tests
└── uselessfiles/        # Development artifacts and experimental code
```

## 🛠️ Setup Instructions

### System Requirements
- **Python**: 3.8+ (tested with 3.9, 3.10, 3.11)
- **GPU**: CUDA-compatible GPU recommended (NVIDIA RTX series optimal)
- **Memory**: 8GB+ RAM (16GB recommended for training)
- **Storage**: 2GB+ free space for models and datasets
- **OS**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+

### Installation Steps

1. **Environment Setup**:
   ```powershell
   # Navigate to project directory
   cd diseases_detection_ai
   
   # Create isolated virtual environment
   python -m venv disease_detection_env
   disease_detection_env\Scripts\activate  # Windows
   # source disease_detection_env/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies**:
   ```powershell
   # Install all required packages
   pip install -r requirements.txt
   
   # Verify PyTorch installation with CUDA support
   python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
   ```

3. **Model Preparation**:
   ```powershell
   # Models are included in the repository
   # Verify model files exist
   dir models\*.pth
   ```

4. **Test Installation**:
   ```powershell
   # Quick functionality test
   python -c "from src.model import CropDiseaseResNet50; print('Installation successful!')"
   ```

### Quick Start Guide

1. **Launch API Server**:
   ```powershell
   # Start FastAPI development server
   python main.py
   
   # Server will start on http://localhost:8000
   # API documentation available at http://localhost:8000/docs
   ```

2. **Test Disease Detection**:
   ```powershell
   # Using PowerShell with Invoke-RestMethod
   $response = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -InFile "test_image.jpg" -ContentType "multipart/form-data"
   $response | ConvertTo-Json
   ```

3. **Alternative API Testing**:
   ```powershell
   # Using curl (if available)
   curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@test_crop_image.jpg"
   ```

## 🔬 Model Training & Evaluation

### Training Dataset Statistics
- **Total Training Samples**: 14,440 high-quality crop images
- **Validation Samples**: 3,089 images for model validation
- **Test Samples**: 3,109 images for final evaluation
- **Image Resolution**: Variable (224x224 after preprocessing)
- **Data Augmentation**: Rotation, flip, brightness, contrast adjustments
- **Last Training Date**: September 9, 2025

### Training Configuration
```python
# Training hyperparameters for v3.0 model
{
    "epochs": 50,
    "batch_size": 32,
    "learning_rate": 0.001,
    "optimizer": "Adam",
    "scheduler": "ReduceLROnPlateau",
    "early_stopping": "patience=7",
    "data_augmentation": True
}
```

### Model Performance Metrics
- **Test Accuracy**: 90.09% (v3.0)
- **Validation Accuracy**: 90.06% (v3.0)
- **Model Size**: ~100MB (full model), ~25MB (lite variant)
- **Average Inference Time**: <200ms per image on GPU, <800ms on CPU
- **Memory Usage**: ~2GB GPU memory (full model), ~500MB (lite model)

### Training Commands
```powershell
# Train new model from scratch
python src\train.py --epochs 50 --batch_size 32 --lr 0.001 --save_best

# Resume training from checkpoint
python src\train.py --resume models\crop_disease_v2_model.pth --epochs 20

# Evaluate existing model
python src\evaluate.py --model_path models\crop_disease_v3_model.pth --test_data data\test

# Generate visual explanations
python src\explain.py --image_path test_images\tomato_blight.jpg --output_dir outputs\
```

## 🌐 API Documentation

### Core Endpoints

#### Disease Prediction
```http
POST /predict
Content-Type: multipart/form-data
Parameters:
  - file: image file (JPG, PNG, JPEG)
  - explain: boolean (optional, default: true)
  - confidence_threshold: float (optional, default: 0.7)

Response Example:
{
  "disease": "Tomato___Early_blight",
  "disease_display": "Early Blight",
  "crop": "Tomato",
  "confidence": 0.9456,
  "severity": "High",
  "risk_level": 8.5,
  "symptoms": ["Brown spots with concentric rings", "Yellowing leaves"],
  "treatment": {
    "immediate": ["Remove affected leaves", "Apply fungicide"],
    "preventive": ["Improve air circulation", "Avoid overhead watering"]
  },
  "explanation": {
    "gradcam_regions": "base64_image_data",
    "attention_map": "visualization_data"
  },
  "processing_time": 0.184
}
```

#### Batch Prediction
```http
POST /predict/batch
Content-Type: multipart/form-data
Parameters:
  - files: multiple image files
  
Response: Array of prediction objects
```

#### Health Check
```http
GET /health
Response: {
  "status": "healthy",
  "model_loaded": true,
  "version": "3.0",
  "gpu_available": true,
  "memory_usage": "1.2GB"
}
```

#### Model Information
```http
GET /model/info
Response: {
  "version": "3.0",
  "classes": 15,
  "accuracy": 0.9009,
  "training_date": "2025-09-09",
  "supported_crops": ["Pepper (Bell)", "Potato", "Tomato"]
}
```

## 🔍 Visual Explanation System

### Grad-CAM Implementation
Gradient-weighted Class Activation Mapping highlights the most important regions:

```python
from src.explain import CropDiseaseExplainer

# Initialize explainer with trained model
explainer = CropDiseaseExplainer(
    model_path="models/crop_disease_v3_model.pth",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

# Generate explanation for image
explanation = explainer.explain_prediction(
    image_path="test_image.jpg",
    save_path="outputs/explanation.jpg",
    alpha=0.4  # Overlay transparency
)
```

### LIME Integration
Local Interpretable Model-agnostic Explanations for segment-based analysis:

```python
# Generate LIME explanation
lime_explanation = explainer.lime_explanation(
    image_path="test_image.jpg",
    num_samples=1000,
    num_features=100
)
```

## 🧪 Testing & Quality Assurance

### Automated Testing Suite
```powershell
# Run complete test suite
python -m pytest tests\ -v --cov=src --cov-report=html

# Run specific test categories
python -m pytest tests\test_model.py -v      # Model functionality
python -m pytest tests\test_api.py -v       # API endpoints
python -m pytest tests\test_explain.py -v   # Explanation system
```

### Manual Testing
```powershell
# Test model loading and inference
python tests\manual_test_model.py

# Test API with sample images
python tests\manual_test_api.py

# Performance benchmarking
python tests\benchmark_inference.py
```

### Integration Testing
```powershell
# End-to-end API testing
python tests\integration_test.py --host localhost --port 8000
```

## 🚀 Production Deployment

### Docker Deployment
```powershell
# Build optimized container
docker build -t crop-disease-detection-api .\api

# Run with GPU support
docker run --gpus all -p 8000:8000 crop-disease-detection-api

# Run CPU-only version
docker run -p 8000:8000 -e USE_GPU=false crop-disease-detection-api
```

### Environment Configuration
```powershell
# Production environment variables
$env:ENVIRONMENT = "production"
$env:MODEL_PATH = "models/crop_disease_v3_model.pth"
$env:CONFIDENCE_THRESHOLD = "0.8"
$env:ENABLE_EXPLANATIONS = "true"
$env:MAX_IMAGE_SIZE = "10MB"
```

### Production Considerations
- **Load Balancing**: Use multiple API instances behind load balancer
- **Monitoring**: Implement comprehensive logging and metrics
- **Security**: Configure proper CORS, rate limiting, and authentication
- **Performance**: Use GPU acceleration and model quantization
- **Scalability**: Consider serverless deployment for variable workloads

## 📈 Performance Optimization

### Memory Optimization Strategies
```python
# Use lightweight model for resource-constrained environments
from src.model_lite import TinyDiseaseClassifier

model = TinyDiseaseClassifier(num_classes=15)  # ~5MB model size
```

### Speed Optimization
- **Model Quantization**: INT8 quantization for 4x speed improvement
- **Batch Processing**: Process multiple images simultaneously
- **Async API**: Non-blocking request handling
- **Caching**: Cache frequent predictions and explanations

### Edge Deployment
- **Model Pruning**: Remove unnecessary parameters
- **Knowledge Distillation**: Train smaller student models
- **ONNX Export**: Cross-platform deployment support

## 🤝 Development Workflow

### Contributing Guidelines
1. **Fork Repository**: Create personal fork for development
2. **Feature Branch**: Create descriptive branch name
3. **Code Standards**: Follow PEP 8 and add type hints
4. **Testing**: Add comprehensive tests for new features
5. **Documentation**: Update README and inline documentation
6. **Pull Request**: Submit with detailed description and test results

### Code Quality Standards
- **Type Hints**: All functions must include type annotations
- **Docstrings**: Google-style docstrings for all public methods
- **Testing**: Minimum 80% code coverage required
- **Linting**: Code must pass flake8 and black formatting

## 📄 License & Legal

This project is part of the HackBhoomi2025 agricultural intelligence platform. All rights reserved.

### Model Attribution
- Base ResNet50 architecture from torchvision (BSD License)
- Training dataset: Publicly available agricultural disease datasets
- Custom modifications and enhancements: HackBhoomi2025 team

## 🆘 Troubleshooting Guide

### Common Issues & Solutions

1. **CUDA Out of Memory Error**:
   ```powershell
   # Solution: Use lighter model or reduce batch size
   $env:USE_LITE_MODEL = "true"
   $env:BATCH_SIZE = "8"
   ```

2. **Model Loading Errors**:
   ```powershell
   # Verify model file integrity
   python -c "import torch; torch.load('models/crop_disease_v3_model.pth', map_location='cpu')"
   ```

3. **Low Prediction Accuracy**:
   - Ensure image quality (minimum 224x224 resolution)
   - Verify crop type is supported (Pepper, Potato, Tomato only)
   - Check image format (JPG, PNG supported)
   - Review confidence threshold settings

4. **API Connection Issues**:
   ```powershell
   # Check if server is running
   Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
   ```

5. **Dependencies Installation Problems**:
   ```powershell
   # Clean installation
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

### Performance Troubleshooting
- **Slow Inference**: Enable GPU acceleration, use lite model variant
- **High Memory Usage**: Reduce batch size, use memory-optimized model
- **API Timeout**: Increase request timeout, optimize image preprocessing

### Support & Resources
- **Issue Tracking**: GitHub Issues for bug reports and feature requests
- **Documentation**: Comprehensive API documentation at `/docs`
- **Community**: HackBhoomi2025 development team for technical support

---

**📊 Project Statistics:**
- **Lines of Code**: 2,000+ (main application)
- **Model Parameters**: 25.6M (ResNet50), 1.2M (Lite variant)
- **Supported Image Formats**: JPG, JPEG, PNG
- **API Response Time**: <200ms average
- **Model Accuracy**: 90.09% (state-of-the-art for agricultural disease detection)

*Last Updated: September 2025*  
*Model Version: 3.0*  
*API Version: 2.0.0*  
*Documentation Version: 1.5*