# Deployment Guide

This guide explains how to install dependencies, run the application locally, and deploy to a server.

## Prerequisites
- Python 3.8+
- pip package manager
- Optional: Docker (for containerized deployment)

## Local Installation

### Step 1: Install Dependencies

**Option A: Using the batch script (Windows)**
```bash
install_dependencies.bat
```

**Option B: Using pip directly**
```bash
pip install -r requirements.txt
```

### Step 2: Install Additional Libraries (Optional)

For full SHAP analysis and advanced models:
```bash
pip install catboost lightgbm xgboost shap
```

**Note:** If installation fails due to network issues, the application will work with the available models (SVR, RandomForest, GBM, etc.).

## Running the Application

### Backend Server (API)
```bash
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

### Frontend Dashboard

**Option 1: Simple HTTP Server**
```bash
cd frontend
python -m http.server 8080
```
Then open: `http://localhost:8080/dashboard.html`

**Option 2: Direct File Opening**
Simply open `frontend/dashboard.html` in your web browser.

## Docker Deployment

### Build the Docker Image
```bash
docker build -t shear-capacity-api .
```

### Run the Container
```bash
docker run -p 8000:8000 shear-capacity-api
```

## Cloud Deployment

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn backend.app:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS EC2

1. Launch an EC2 instance
2. SSH into the instance
3. Clone repository and install dependencies
4. Run with gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app:app --bind 0.0.0.0:8000
   ```

### DigitalOcean / Other VPS

1. Create a droplet/server
2. Install Python and dependencies
3. Use systemd service or supervisor to run the application
4. Configure nginx as reverse proxy

## Re-training Models with Full Libraries

If you successfully install CatBoost/LightGBM/SHAP:

```bash
# Re-train models
python train_models.py

# Generate comprehensive visualizations
python create_comprehensive_visualizations.py

# Generate SHAP analysis
python visualize_results.py
```

## Troubleshooting

**Issue: Module not found errors**
- Solution: Run `pip install -r requirements.txt`

**Issue: Cannot connect to backend**
- Solution: Ensure backend is running on port 8000
- Check firewall settings

**Issue: Images not loading in dashboard**
- Solution: Ensure you're serving the frontend from the correct directory
- Check image paths in `dashboard.html`

## Project Structure
```
e:/Input Day 2/
├── backend/
│   └── app.py              # FastAPI backend
├── frontend/
│   ├── index.html          # Simple prediction UI
│   └── dashboard.html      # Full dashboard
├── models/                 # Trained models
├── output/                 # Visualizations
│   └── comprehensive/      # Additional plots
├── results/                # Metrics CSV
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── *.py                   # Training/analysis scripts
```
