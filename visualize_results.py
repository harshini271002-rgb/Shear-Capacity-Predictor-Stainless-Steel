import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import os
from sklearn.inspection import permutation_importance
from sklearn.metrics import r2_score

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("SHAP not installed, skipping SHAP analysis.")

# Set style
sns.set(style="whitegrid")
os.makedirs('output', exist_ok=True)

def load_data():
    print("Loading data...")
    # Cleaned data for prediction
    df_clean = pd.read_csv('e:/Input Day 2/cleaned_data.csv')
    X = df_clean.drop(columns=['VU(FEA)'])
    y = df_clean['VU(FEA)']
    
    # Original data for comparison columns
    # We need to ensure rows align. cleaned_data was dropped NaNs.
    # We should re-process original to get the same rows or assume alignment if no drops happened (but drops happened).
    # Ideally, we should have saved the index or the full dataframe in data_analysis.
    # Let's clean the original csv again similarly to get the comparison columns.
    df_full = pd.read_csv('e:/Input Day 2/Input csv.csv', header=2)
    
    # Same cleaning logic as data_analysis.py to ensure alignment
    target_col = 'VU(FEA)'
    feature_cols = [
        'Depth of Web opening(dwh/d1)', 'd1', 'tw', 'flange width(mm)', 
        'total depth D (mm)', 'fyw', 'E', 'a/d', target_col
    ]
    # Keep comparison columns
    comparison_cols = [
        'Vnl(AS)FEA', 'VN PRO', 'Vnl with tension field', 
        'VnlWITHOUT TENSION FIELD', 'Design Shear Resistance (VRd)' # Potential mappings
    ]
    
    # Add comparison cols to "feature_cols" just for selection, then handle NaNs
    # Note: Column names must be exact. I'll use strict names from Step 5 view.
    # 'Vnl(AS)FEA', 'VN PRO', 'Vnl with tension field', 'VnlWITHOUT TENSION FIELD', 'Design Shear Resistance (VRd)'
    
    # Allow some missing columns if they don't exist
    existing_cols = [c for c in feature_cols + comparison_cols if c in df_full.columns]
    df_full_clean = df_full[existing_cols].copy()
    
    df_full_clean = df_full_clean.dropna(subset=[target_col])
    for col in df_full_clean.columns:
        df_full_clean[col] = pd.to_numeric(df_full_clean[col], errors='coerce')
    df_full_clean = df_full_clean.dropna() # This should match cleaned_data.csv rows
    
    print(f"Full Cleaned Data Shape: {df_full_clean.shape}")
    return X, y, df_full_clean

def plot_performance_graphs():
    print("Generating Performance Graphs...")
    results_df = pd.read_csv('results/model_comparison_metrics.csv')
    
    # Bar chart for R2
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Model', y='Test R2', data=results_df, palette='viridis')
    plt.title('Model Comparison - Test R2 Score')
    plt.ylabel('R2 Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/model_comparison_r2.png')
    plt.close()
    
    # Bar chart for MAPE
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Model', y='Test MAPE', data=results_df, palette='magma')
    plt.title('Model Comparison - Test MAPE (%)')
    plt.ylabel('MAPE (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/model_comparison_mape.png')
    plt.close()

def shap_analysis(X, model, model_name='CatBoost'):
    print(f"Running SHAP analysis for {model_name}...")
    try:
        explainer = shap.Explainer(model)
        shap_values = explainer(X)
        
        # Summary Plot
        plt.figure()
        shap.summary_plot(shap_values, X, show=False)
        plt.tight_layout()
        plt.savefig(f'output/shap_summary_{model_name}.png')
        plt.close()
        
        # Dependence Plots for top features
        # Get top features by mean abs shap value
        mean_shap = np.abs(shap_values.values).mean(axis=0)
        top_features_inds = mean_shap.argsort()[-3:][::-1] # Top 3
        
        for i in top_features_inds:
            feature_name = X.columns[i]
            plt.figure()
            shap.dependence_plot(feature_name, shap_values.values, X, show=False)
            plt.tight_layout()
            plt.savefig(f'output/shap_dependence_{feature_name}.png')
            plt.close()
            
    except Exception as e:
        print(f"Error in SHAP analysis: {e}")

def permutation_importance_analysis(model, X, y):
    print("Running Permutation Feature Importance...")
    try:
        r = permutation_importance(model, X, y, n_repeats=10, random_state=42, n_jobs=-1)
        sorted_idx = r.importances_mean.argsort()
        
        plt.figure(figsize=(10, 6))
        plt.boxplot(r.importances[sorted_idx].T, vert=False, labels=X.columns[sorted_idx])
        plt.title("Permutation Importances (test set)")
        plt.tight_layout()
        plt.savefig('output/permutation_importance.png')
        plt.close()
    except Exception as e:
        print(f"Error in Permutation Importance: {e}")

def comparative_analysis(X, y_true, df_full, best_model, scaler):
    print("Running Comparative Analysis...")
    # Predict
    X_scaled = scaler.transform(X)
    y_pred = best_model.predict(X_scaled)
    
    # Plot predicted vs actual
    plt.figure(figsize=(8, 8))
    plt.scatter(y_true, y_pred, alpha=0.7)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.xlabel('Actual Shear Capacity (kN) [FEA]')
    plt.ylabel('Predicted Shear Capacity (kN) [ML]')
    plt.title('Predicted vs Actual Shear Capacity')
    plt.savefig('output/predicted_vs_actual.png')
    plt.close()
    
    # Comparison with other methods
    # Columns: 'Vnl(AS)FEA', 'VN PRO', 'Vnl with tension field', 'VnlWITHOUT TENSION FIELD'
    # Plot Comparison of Ultimate Loads
    
    # We can create a multi-line plot or scatter comparisons
    plt.figure(figsize=(10, 6))
    # Sort by Index for cleaner line plot if applicable, or just scatter
    # Let's sort by Actual Capacity to make the graph readable
    sort_idx = np.argsort(y_true)
    
    plt.plot(np.arange(len(y_true)), y_true.iloc[sort_idx], label='FEA (Actual)', linewidth=2, color='black')
    plt.plot(np.arange(len(y_true)), y_pred[sort_idx], label='ML Prediction', linestyle='--', linewidth=2, color='red')
    
    # Add other columns if they exist
    cols_map = {
        'VN PRO': 'Euro Code (VN PRO)',
        'Vnl with tension field': 'Tension Field',
        'VnlWITHOUT TENSION FIELD': 'Without Tension Field'
    }
    
    for col, label in cols_map.items():
        if col in df_full.columns:
            plt.plot(np.arange(len(y_true)), df_full[col].iloc[sort_idx], label=label, alpha=0.6, linestyle=':')
            
    plt.legend()
    plt.title('Comparison of Shear Capacity Models')
    plt.xlabel('Sample Index (Sorted by Capacity)')
    plt.ylabel('Shear Capacity (kN)')
    plt.tight_layout()
    plt.savefig('output/comparison_ultimate_loads.png')
    plt.close()
    
    # Contour Plot for Shear Capacity as function of two main features (e.g. d1 vs tw)
    # Use grid values
    try:
        # Assuming d1 and tw are features 1 and 2
        feature1 = 'd1'
        feature2 = 'tw'
        
        if feature1 in X.columns and feature2 in X.columns:
            # Create a meshgrid
            # This is hard because other features need to be fixed.
            # Usually contour plots are done by varying 2 and fixing others at mean.
            
            # Simple 2D interpolation from data points
            plt.figure(figsize=(8, 6))
            plt.tricontourf(X[feature1], X[feature2], y_pred, levels=14, cmap="RdBu_r")
            plt.colorbar(label='Predicted Shear Capacity')
            plt.scatter(X[feature1], X[feature2], c='k', s=5, alpha=0.5)
            plt.xlabel(feature1)
            plt.ylabel(feature2)
            plt.title(f'Shear Capacity Contour ({feature1} vs {feature2})')
            plt.savefig('output/contour_shear_capacity.png')
            plt.close()
    except Exception as e:
        print(f"Skipping contour plot: {e}")

if __name__ == "__main__":
    X, y, df_full = load_data()
    
    # Load Scaler
    scaler = joblib.load('models/scaler.pkl')
    
    # Load Best Model Info
    with open('models/best_model_info.json', 'r') as f:
        info = json.load(f)
    best_model_name = info['best_model_name']
    print(f"Best model determined: {best_model_name}")
    
    # Load Best Model
    best_model = joblib.load(f'models/{best_model_name}_best.pkl')
    
    # Load CatBoost specifically for SHAP if available
    try:
        catboost_model = joblib.load('models/CatBoost_best.pkl')
    except:
        catboost_model = None
        print("CatBoost model not found for SHAP.")
        
    # Run Validations
    plot_performance_graphs()
    
    if SHAP_AVAILABLE and catboost_model:
        shap_analysis(X, catboost_model, 'CatBoost')
    elif not SHAP_AVAILABLE:
        print("Skipping SHAP (Library missing).")
    elif not catboost_model:
        print("Skipping SHAP (CatBoost model missing).")
        
    permutation_importance_analysis(best_model, X, y)
    
    comparative_analysis(X, y, df_full, best_model, scaler)
    
    print("Visualization Complete. Check output/ directory.")
