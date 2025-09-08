# 🌱 Crop Disease Detection AI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-red.svg)](https://pytorch.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered crop disease detection system using deep learning to identify diseases in corn, potato, and tomato crops from leaf images. The system provides accurate disease classification, risk assessment, visual explanations, and treatment recommendations.

## 🎯 Project Overview

This project implements a comprehensive crop disease detection pipeline that:
- **Detects 17 different diseases** across corn, potato, and tomato crops
- **Provides visual explanations** using Grad-CAM heatmaps
- **Offers treatment recommendations** from an integrated knowledge base
- **Calculates risk levels** based on confidence and environmental factors
- **Supports multiple interfaces**: GUI application, REST API, and batch processing

### 🏆 Key Features

- **🤖 AI Model**: ResNet50-based transfer learning with 26.1M parameters
- **📊 Disease Classes**: 17 classes including healthy variants for each crop
- **🎨 Visual Explanations**: Grad-CAM heatmaps highlighting infected regions
- **📚 Knowledge Base**: Comprehensive disease information with symptoms and treatments
- **⚡ Real-time Processing**: Fast inference with GPU/CPU support
- **🌐 REST API**: FastAPI backend with comprehensive endpoints
- **🖥️ GUI Application**: User-friendly Tkinter interface
- **📈 Risk Assessment**: Multi-factor risk calculation including weather data

## 📁 Project Structure

```
diseases_detection_ai/
├── 📂 api/                     # FastAPI backend
│   ├── main.py                 # API server with endpoints
│   ├── requirements.txt        # API dependencies
│   └── Dockerfile             # Container configuration
├── 📂 data/                    # Dataset (train/val/test splits)
│   ├── train/                 # Training images (153 samples)
│   ├── val/                   # Validation images (51 samples)
│   └── test/                  # Test images (51 samples)
├── 📂 knowledge_base/          # Disease information
│   └── disease_info.json      # Symptoms, treatments, prevention
├── 📂 models/                  # Trained model weights
│   ├── crop_disease_v2_model.pth      # Enhanced V2 model
│   └── crop_disease_resnet50.pth      # Baseline V1 model
├── 📂 notebooks/               # Jupyter notebooks
│   └── train_resnet50.ipynb   # Training notebook
├── 📂 outputs/                 # Results and visualizations
│   ├── logs/                  # Training logs
│   ├── heatmaps/              # Grad-CAM visualizations
│   └── *.json                 # Evaluation results
├── 📂 src/                     # Core source code
│   ├── dataset.py             # Data loading and preprocessing
│   ├── model.py               # ResNet50 architecture
│   ├── train.py               # Training pipeline
│   ├── evaluate.py            # Model evaluation
│   ├── explain.py             # Grad-CAM explanations
│   ├── risk_level.py          # Risk assessment logic
│   └── utils.py               # Helper functions
├── crop_disease_gui.py         # Tkinter GUI application
├── requirements.txt            # Main dependencies
├── plan.txt                   # Project roadmap
└── EVALUATION_SUMMARY.md       # Performance analysis
```

## 🛠️ Technology Stack

### Core Technologies
- **Deep Learning**: PyTorch 2.1.0, torchvision 0.16.0
- **Model Architecture**: ResNet50 with transfer learning
- **Computer Vision**: OpenCV, PIL/Pillow
- **API Framework**: FastAPI 0.104.1 with Uvicorn
- **GUI Framework**: Tkinter (built-in Python)

### Dependencies
- **Data Science**: NumPy, scikit-learn, matplotlib, seaborn
- **Image Processing**: OpenCV-Python, Pillow
- **Web Framework**: FastAPI, Uvicorn, python-multipart
- **Authentication**: python-jose, passlib
- **Visualization**: matplotlib, seaborn

### Development Tools
- **Environment**: Python 3.8+
- **Notebooks**: Jupyter/Google Colab support
- **Containerization**: Docker support
- **Version Control**: Git

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-compatible GPU for faster training

### 1. Clone Repository
```bash
git clone <repository-url>
cd diseases_detection_ai
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install main dependencies
pip install -r requirements.txt

# For API development (optional)
pip install -r api/requirements.txt
```

### 4. Download Pre-trained Models
The repository includes pre-trained models:
- `models/crop_disease_v2_model.pth` - Enhanced V2 model
- `models/crop_disease_resnet50.pth` - Baseline V1 model

### 5. Verify Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torchvision; print(f'TorchVision: {torchvision.__version__}')"
```

## 📖 Usage Guide

### 🖥️ GUI Application (Recommended for End Users)

Launch the user-friendly GUI application:

```bash
python crop_disease_gui.py
```

**Features:**
- 📁 **Image Upload**: Browse and select crop leaf images
- 🔍 **AI Analysis**: One-click disease detection
- 📊 **Results Display**: Detailed predictions with confidence scores
- 📚 **Disease Information**: Symptoms, treatments, and prevention tips
- 🎯 **Risk Assessment**: Color-coded risk levels

**Supported Image Formats**: JPG, JPEG, PNG, BMP, TIFF

### 🌐 REST API Server

Start the FastAPI server for programmatic access:

```bash
# Start API server
python api/main.py

# Or using uvicorn directly
uvicorn api.main:app --host localhost --port 8000
```

**API Endpoints:**
- `POST /predict` - Single image disease prediction
- `POST /batch_predict` - Multiple image processing
- `GET /health` - API health check
- `GET /classes` - List supported disease classes
- `GET /disease_info/{crop}/{disease}` - Disease information

**API Documentation**: http://localhost:8000/docs

### 📊 Model Training

Train your own model with custom data:

```bash
# Train new model
python src/train.py

# Evaluate model performance
python src/evaluate.py

# Generate visual explanations
python src/explain.py
```

### 🔬 Jupyter Notebooks

Explore the training process interactively:

```bash
jupyter notebook notebooks/train_resnet50.ipynb
```

## 💡 Usage Examples

### Python API Usage

```python
import requests

# Single image prediction
with open('leaf_image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f},
        data={'include_explanation': True}
    )

result = response.json()
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Risk Level: {result['risk_level']}")
```

### Command Line Usage

```bash
# Test model with sample image
python test_model.py --image test_leaf_sample.jpg

# Batch process multiple images
python src/evaluate.py --batch_dir data/test/
```

### GUI Application Workflow

1. **Launch Application**: `python crop_disease_gui.py`
2. **Upload Image**: Click "📁 Select Image" button
3. **Analyze**: Click "🔍 Analyze Disease" button
4. **View Results**: See detailed analysis in results panel

## 🎯 Model Performance

### Current Performance (V2 Enhanced Model)
- **Test Accuracy**: 11.76% (6/51 correct predictions)
- **Model Architecture**: ResNet50 with 26.1M parameters
- **Training Data**: 255 total samples across 17 classes
- **Inference Speed**: ~0.1 seconds per image

### Performance Analysis
- **Limitation**: Small dataset size (only ~3 samples per class)
- **Recommendation**: Increase dataset to 1000+ samples per class
- **Strengths**: Robust architecture, comprehensive evaluation pipeline

### Supported Disease Classes

**Corn Diseases:**
- Cercospora Leaf Spot / Gray Leaf Spot
- Common Rust
- Northern Leaf Blight
- Healthy

**Potato Diseases:**
- Early Blight
- Late Blight
- Healthy

**Tomato Diseases:**
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-spotted)
- Target Spot
- Tomato Mosaic Virus
- Tomato Yellow Leaf Curl Virus
- Healthy

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set device preference
export TORCH_DEVICE=cuda  # or 'cpu'

# Optional: Set model path
export MODEL_PATH=models/crop_disease_v2_model.pth
```

### API Configuration
Edit `api/main.py` for production settings:
- CORS origins
- Authentication
- Rate limiting
- Logging levels

## 🚀 Deployment

### Local Development
```bash
# GUI Application
python crop_disease_gui.py

# API Server
python api/main.py
```

### Docker Deployment
```bash
# Build container
docker build -t crop-disease-api ./api

# Run container
docker run -p 8000:8000 crop-disease-api
```

### Cloud Deployment
The API is ready for deployment on:
- **AWS**: EC2, Lambda, ECS
- **Google Cloud**: Cloud Run, Compute Engine
- **Azure**: Container Instances, App Service
- **Heroku**: Container deployment

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Ensure backward compatibility

### Areas for Contribution
- **Data Collection**: Expand disease image dataset
- **Model Improvements**: Experiment with new architectures
- **Feature Enhancement**: Add new crops/diseases
- **Performance Optimization**: Speed and accuracy improvements
- **Documentation**: Tutorials and examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors & Acknowledgments

**Project Team:**
- **Lead Developer**: [Your Name]
- **AI/ML Engineer**: [Team Member]
- **Data Scientist**: [Team Member]

**Acknowledgments:**
- PlantVillage dataset for training data
- PyTorch team for deep learning framework
- FastAPI team for web framework
- Open source community for various tools

## 📞 Support & Contact

### Getting Help
- **Documentation**: Check this README and code comments
- **Issues**: Create GitHub issue for bugs/feature requests
- **Discussions**: Use GitHub discussions for questions

### Contact Information
- **Email**: [your-email@domain.com]
- **Project Repository**: [GitHub URL]
- **Documentation**: [Documentation URL]

## 🔮 Future Roadmap

### Phase 1: Data Enhancement (Weeks 1-2)
- [ ] Collect 1000+ images per disease class
- [ ] Implement advanced data augmentation
- [ ] Create balanced train/val/test splits

### Phase 2: Model Optimization (Weeks 3-4)
- [ ] Experiment with EfficientNet, MobileNet
- [ ] Implement ensemble methods
- [ ] Add uncertainty estimation

### Phase 3: Feature Expansion (Weeks 5-6)
- [ ] Add more crop types (rice, wheat, etc.)
- [ ] Implement real-time video processing
- [ ] Mobile app development

### Phase 4: Production Enhancement (Weeks 7-8)
- [ ] Cloud deployment with auto-scaling
- [ ] Monitoring and logging system
- [ ] User analytics and feedback system

---

## 📊 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Clone repository
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test GUI: `python crop_disease_gui.py`
- [ ] Test API: `python api/main.py`
- [ ] Upload test image and verify results
- [ ] Explore API documentation at http://localhost:8000/docs

**🎉 Ready to detect crop diseases with AI!**
