# Full ML Model Deployment Guide

## 🎯 Deploy Complete Crop AI with All ML Libraries

If you want to keep scikit-learn, lightgbm, xgboost, and shap, here are the best platforms:

---

## 🚂 **Option 1: Railway (Recommended)**

### Why Railway?
- ✅ Docker support out of the box
- ✅ Automatic deployments from GitHub
- ✅ $5/month for production apps
- ✅ Easy scaling and monitoring
- ✅ Built-in databases (PostgreSQL, Redis)

### Setup Steps:
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project (from crop_ai directory)
railway init

# 4. Deploy using Docker
railway up

# 5. Set environment variables (if needed)
railway variables set PYTHONPATH=/app/src
```

### Files You Already Have:
- ✅ `Dockerfile` - Multi-stage build ready
- ✅ `docker-compose.yml` - For local development
- ✅ `requirements.txt` - Full ML dependencies
- ✅ `app.py` - Complete FastAPI with ML models

### Expected Performance:
- **Cold start:** 30-60 seconds (model loading)
- **Warm requests:** 100-500ms
- **Memory usage:** 1-2GB
- **Cost:** ~$5-10/month

---

## 🎨 **Option 2: Render**

### Why Render?
- ✅ Free tier available
- ✅ Automatic GitHub deployments
- ✅ Docker support
- ✅ Built-in SSL certificates

### Setup Steps:
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add full ML deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Connect GitHub repository
   - Select "Web Service"
   - Render auto-detects Dockerfile

3. **Configure:**
   - **Build Command:** `docker build -t crop-ai .`
   - **Start Command:** `docker run -p 10000:8000 crop-ai`
   - **Environment:** Add `PYTHONPATH=/app/src`

### Expected Performance:
- **Free tier:** 512MB RAM, may be slow
- **Paid tier:** $7/month, 1GB RAM
- **Cold start:** 60-120 seconds on free tier

---

## ☁️ **Option 3: Google Cloud Run**

### Why Cloud Run?
- ✅ Pay only for requests
- ✅ Scales to zero (cost-effective)
- ✅ Handle large models (up to 8GB RAM)
- ✅ Google's global infrastructure

### Setup Steps:
```bash
# 1. Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login and set project
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# 3. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# 4. Build and deploy
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/crop-ai
gcloud run deploy crop-ai \
  --image gcr.io/YOUR-PROJECT-ID/crop-ai \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 300s \
  --allow-unauthenticated
```

### Expected Costs:
- **Requests:** $0.40 per million requests
- **CPU/Memory:** $0.00002400 per vCPU-second
- **Example:** 1000 requests/month ≈ $2-5

---

## 🤗 **Option 4: Hugging Face Spaces**

### Why Hugging Face?
- ✅ Free GPU access
- ✅ ML-focused platform
- ✅ Great for model demos
- ✅ Built-in model versioning

### Setup Steps:
1. **Create Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Create new Space with "Docker" template

2. **Upload Files:**
   ```
   crop-ai-space/
   ├── Dockerfile
   ├── app.py
   ├── requirements.txt
   ├── models/
   └── src/
   ```

3. **Configure Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 7860
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
   ```

---

## 🔄 **Hybrid Approach: Best of Both Worlds**

Deploy on multiple platforms for different use cases:

### Architecture:
```
Frontend (Vercel) → Load Balancer → {
  ├── Light API (Vercel) - Fast responses
  └── Full ML API (Railway) - Complex predictions
}
```

### Implementation:
1. **Light requests** → Vercel (rule-based predictions)
2. **Heavy ML requests** → Railway (full model predictions)
3. **Frontend** decides which endpoint to use

---

## 📊 **Platform Comparison**

| Platform | Cost | Setup | Performance | ML Support |
|----------|------|-------|-------------|------------|
| **Railway** | $5/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Render** | Free/$7 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cloud Run** | Pay-per-use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **HF Spaces** | Free | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Vercel** | Free | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |

---

## 🚀 **Recommended Next Steps**

### For Quick Start (Railway):
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### For Production (Google Cloud Run):
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/crop-ai
gcloud run deploy --image gcr.io/PROJECT-ID/crop-ai
```

### For Demo/Testing (Hugging Face):
- Upload to HF Spaces with Docker template
- Free GPU for inference

---

## 🔧 **Files Ready for Deployment**

You already have everything needed:
- ✅ `Dockerfile` - Production-ready container
- ✅ `docker-compose.yml` - Local development
- ✅ `app.py` - Full FastAPI with ML models
- ✅ `requirements.txt` - Complete dependencies
- ✅ `nginx.conf` - Production proxy (optional)

**No changes needed** - your existing files work perfectly with these platforms!

---

## 💡 **Pro Tips**

1. **Start with Railway** - Easiest deployment
2. **Use Docker locally** first to test
3. **Monitor memory usage** - ML models are memory-intensive
4. **Set up CI/CD** with GitHub for automatic deployments
5. **Use environment variables** for configuration

Choose the platform that fits your budget and requirements. Railway is the easiest to start with!
