import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import os
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Set style
sns.set(style="whitegrid")
plt.rcParams['figure.dpi'] = 100
os.makedirs('output/comprehensive', exist_ok=True)

def load_all_models():
    """Load all trained models"""
    models = {}
    for file in os.listdir('models'):
        if file.endswith('_best.pkl'):
            name = file.replace('_best.pkl', '')
            models[name] = joblib.load(f'models/{file}')
    return models

def generate_all_visualizations():
    print("Generating comprehensive visualizations...")
    
    # Load data
    df = pd.read_csv('e:/Input Day 2/cleaned_data.csv')
    X = df.drop(columns=['VU(FEA)'])
    y = df['VU(FEA)']
    
    scaler = joblib.load('models/scaler.pkl')
    X_scaled = scaler.transform(X)
    
    models = load_all_models()
    results_df = pd.read_csv('results/model_comparison_metrics.csv')
    
    # 1. Individual Model Performance (Predicted vs Actual for each model)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, (name, model) in enumerate(models.items()):
        if idx >= 6:
            break
        y_pred = model.predict(X_scaled)
        r2 = r2_score(y, y_pred)
        
        axes[idx].scatter(y, y_pred, alpha=0.6, s=50)
        axes[idx].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
        axes[idx].set_xlabel('Actual Shear Capacity (kN)')
        axes[idx].set_ylabel('Predicted Shear Capacity (kN)')
        axes[idx].set_title(f'{name} (R² = {r2:.4f})')
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/comprehensive/individual_model_predictions.png', dpi=150)
    plt.close()
    print("Saved: individual_model_predictions.png")
    
    # 2. Residual Plots for Best Models
    best_models = results_df.nlargest(4, 'Test R2')['Model'].tolist()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, name in enumerate(best_models):
        if name in models:
            y_pred = models[name].predict(X_scaled)
            residuals = y - y_pred
            
            axes[idx].scatter(y_pred, residuals, alpha=0.6)
            axes[idx].axhline(y=0, color='r', linestyle='--', lw=2)
            axes[idx].set_xlabel('Predicted Values')
            axes[idx].set_ylabel('Residuals')
            axes[idx].set_title(f'{name} - Residual Plot')
            axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/comprehensive/residual_plots.png', dpi=150)
    plt.close()
    print("Saved: residual_plots.png")
    
    # 3. Error Distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, name in enumerate(best_models):
        if name in models:
            y_pred = models[name].predict(X_scaled)
            errors = y - y_pred
            
            axes[idx].hist(errors, bins=20, alpha=0.7, edgecolor='black')
            axes[idx].axvline(x=0, color='r', linestyle='--', lw=2)
            axes[idx].set_xlabel('Prediction Error (kN)')
            axes[idx].set_ylabel('Frequency')
            axes[idx].set_title(f'{name} - Error Distribution')
            axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/comprehensive/error_distributions.png', dpi=150)
    plt.close()
    print("Saved: error_distributions.png")
    
    # 4. Metrics Comparison Bar Charts
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # R2
    axes[0, 0].barh(results_df['Model'], results_df['Test R2'], color='steelblue')
    axes[0, 0].set_xlabel('R² Score')
    axes[0, 0].set_title('R² Score Comparison')
    axes[0, 0].grid(True, alpha=0.3, axis='x')
    
    # MAPE
    axes[0, 1].barh(results_df['Model'], results_df['Test MAPE'], color='coral')
    axes[0, 1].set_xlabel('MAPE (%)')
    axes[0, 1].set_title('MAPE Comparison (Lower is Better)')
    axes[0, 1].grid(True, alpha=0.3, axis='x')
    
    # MSE
    axes[1, 0].barh(results_df['Model'], results_df['Test MSE'], color='mediumpurple')
    axes[1, 0].set_xlabel('MSE')
    axes[1, 0].set_title('MSE Comparison (Lower is Better)')
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # MAE
    axes[1, 1].barh(results_df['Model'], results_df['Test MAE'], color='seagreen')
    axes[1, 1].set_xlabel('MAE')
    axes[1, 1].set_title('MAE Comparison (Lower is Better)')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('output/comprehensive/metrics_comparison.png', dpi=150)
    plt.close()
    print("Saved: metrics_comparison.png")
    
    # 5. Feature vs Target Relationships
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for idx, col in enumerate(X.columns):
        axes[idx].scatter(X[col], y, alpha=0.5, s=30)
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Shear Capacity (kN)')
        axes[idx].set_title(f'{col} vs Shear Capacity')
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/comprehensive/feature_relationships.png', dpi=150)
    plt.close()
    print("Saved: feature_relationships.png")
    
    # 6. Performance Summary Table
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = results_df[['Model', 'Test R2', 'Test MAPE', 'Test MSE', 'Test MAE']].round(4)
    table = ax.table(cellText=table_data.values, colLabels=table_data.columns, 
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Color header
    for i in range(len(table_data.columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Model Performance Metrics Summary', fontsize=14, fontweight='bold', pad=20)
    plt.savefig('output/comprehensive/metrics_table.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: metrics_table.png")
    
    # 7. Learning Curves (if CV data exists)
    # This would show CV scores across folds, but we'll create a simpler version
    
    print("\nAll comprehensive visualizations generated successfully!")
    print("Check the 'output/comprehensive/' directory for all images.")

if __name__ == "__main__":
    generate_all_visualizations()
