# Quick Start Guide

## 🌐 WEB APPLICATIONS

### **BEST - Interactive Predictor (NEW!)**
**[OPEN INTERACTIVE PREDICTOR](file:///e:/Input%20Day%202/frontend/interactive_predictor.html)**
- ✅ Beam visualization with dimensions
- ✅ Live input/output prediction
- ✅ Failure mode prediction
- ✅ Feature importance (what influences capacity)
- ✅ All metrics (R², MAPE, MAE, MSE)

### Full Metrics Dashboard
**[OPEN FULL DASHBOARD](file:///e:/Input%20Day%202/frontend/dashboard_full_metrics.html)**
- Complete metrics display
- Editable data links
- Multiple visualizations

---

## ✅ Installation Complete!

Successfully installed:
- FastAPI & Uvicorn (Web framework)
- SHAP (Feature explainability) 
- LightGBM (Advanced ML model)
- XGBoost (Gradient boosting)
- All visualization libraries

**Note:** CatBoost failed to install (requires Visual Studio). The system will work with the other 8+ models.

## 🚀 How to Run

### Step 1: Start the Backend API
Open a terminal and run:
```bash
cd "e:\Input Day 2\backend"
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Open the Dashboard
Open this file in your browser:
```
e:\Input Day 2\frontend\dashboard.html
```

### Step 3: Re-train with New Libraries (Optional)
Since SHAP and LightGBM are now installed, you can re-run:
```bash
cd "e:\Input Day 2"
python train_models.py
python visualize_results.py
```

## 📊 What You Get

### Dashboard Features:
1. **Overview Tab**: Key metrics (R²=0.9952, MAPE=4.22%)
2. **Predict Tab**: Enter beam parameters → Get instant predictions
3. **Visualizations Tab**: 12+ comprehensive graphs
4. **Models Tab**: Performance comparison table

### Available Files:
- `final_predictions.csv` - All 100 section predictions
- `output/` - 6 standard visualizations
- `output/comprehensive/` - 6 additional detailed plots
- `results/model_comparison_metrics.csv` - All metrics

## 🎯 Next Steps

1. **Use the Dashboard**: Interactive predictions and visualizations
2. **Re-train Models**: With SHAP installed, get feature importance plots
3. **Deploy**: Follow `deployment.md` for production deployment
