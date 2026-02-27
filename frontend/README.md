# 🚀 Frontend Web Applications Guide

This directory contains the user interface files for the **Shear Capacity Analysis** project. These HTML files are designed to be run locally using a local web server.

## 🌟 Available Applications

### 1. **Complete Analysis Suite (RECOMMENDED)**
📍 **[complete_analysis.html](complete_analysis.html)**
> The all-in-one comprehensive suite that includes the Interactive Predictor, Beam Visualizer, Failure Modes explanations, Analysis Graphs, and Practical Applications. This is the master dashboard.

### 2. **Interactive Predictor**
📍 **[interactive_predictor.html](interactive_predictor.html)**
> A dedicated interface specifically for inputting beam parameters and instantly retrieving predictions from the Machine Learning models (such as XGBoost, CatBoost, etc.).

### 3. **Full Metrics Dashboard**
📍 **[dashboard_full_metrics.html](dashboard_full_metrics.html)**
> Focuses heavily on the performance analytics of the trained Machine Learning models (R², MAE, MSE, MAPE) and provides comparison tables across the 9 evaluated algorithms.

### 4. **Original Dashboard**
📍 **[dashboard.html](dashboard.html)**
> The original 4-tab dashboard featuring high-level overviews and static visual representations of the data analysis.

### 5. **Simple Predictor**
📍 **[index.html](index.html)**
> A very basic, minimal version of the predictor.

---

## ⚙️ How to Run

1. Open a terminal or command prompt in the **parent directory** (`e:\Input Day 5 ML Parametric study`).
2. Run the provided batch script:
   ```cmd
   start_servers.bat
   ```
3. This will launch a local HTTP server on port `8080`.
4. Open your web browser and navigate to:
   👉 **http://localhost:8080/frontend/complete_analysis.html** (or any of the other HTML files listed above).
