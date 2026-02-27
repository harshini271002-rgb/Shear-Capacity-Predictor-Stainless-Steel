import pandas as pd
import numpy as np
import joblib
import os
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

# Ensure output directories exist
os.makedirs('models', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Load Data
print("Loading data...")
df = pd.read_csv('e:/Input Day 2/cleaned_data.csv')
target_col = 'VU(FEA)'
X = df.drop(columns=[target_col])
y = df[target_col]

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')

# Define Models dictionary dynamically
models = {
    'RandomForest': RandomForestRegressor(random_state=42),
    'DecisionTree': DecisionTreeRegressor(random_state=42),
    'KNN': KNeighborsRegressor(),
    'GBM': GradientBoostingRegressor(random_state=42),
    'SVR': SVR(),
    'MLP': MLPRegressor(random_state=42, max_iter=2000)
}

# Optional Models
try:
    from xgboost import XGBRegressor
    models['XGBoost'] = XGBRegressor(random_state=42, verbosity=0)
except ImportError:
    print("XGBoost not installed, skipping.")

try:
    from lightgbm import LGBMRegressor
    models['LightGBM'] = LGBMRegressor(random_state=42, verbose=-1)
except ImportError:
    print("LightGBM not installed, skipping.")

try:
    from catboost import CatBoostRegressor
    models['CatBoost'] = CatBoostRegressor(random_state=42, verbose=0)
except ImportError:
    print("CatBoost not installed, skipping.")

# Hyperparameter Grids (Simplified for demo/speed, can be expanded)
param_grids = {
    'RandomForest': {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5]},
    'DecisionTree': {'max_depth': [None, 10, 20], 'min_samples_split': [2, 5]},
    'KNN': {'n_neighbors': [3, 5, 7, 9], 'weights': ['uniform', 'distance']},
    'GBM': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2], 'max_depth': [3, 5]},
    'XGBoost': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2], 'max_depth': [3, 5, 7]},
    'LightGBM': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2], 'num_leaves': [31, 50]},
    'CatBoost': {'iterations': [100, 200, 500], 'learning_rate': [0.01, 0.1, 0.2], 'depth': [4, 6, 8]},
    'SVR': {'C': [0.1, 1, 10, 100], 'gamma': ['scale', 'auto']},
    'MLP': {'hidden_layer_sizes': [(50,), (100,), (50, 50)], 'alpha': [0.0001, 0.001]}
}

results = []

# Training Loop
print("Starting training and tuning...")
best_catboost_model = None

for name, model in models.items():
    print(f"Training {name}...")
    
    # Grid Search / Random Search
    grid = RandomizedSearchCV(model, param_grids[name], cv=5, n_iter=10, scoring='r2', n_jobs=-1, random_state=42)
    grid.fit(X_scaled, y)
    
    best_model = grid.best_estimator_
    
    # Save Best Model
    joblib.dump(best_model, f'models/{name}_best.pkl')
    if name == 'CatBoost':
        best_catboost_model = best_model
    
    # 10-Fold CV on Best Model
    cv = KFold(n_splits=10, shuffle=True, random_state=42)
    cv_scores_r2 = cross_val_score(best_model, X_scaled, y, cv=cv, scoring='r2')
    cv_scores_neg_mse = cross_val_score(best_model, X_scaled, y, cv=cv, scoring='neg_mean_squared_error')
    cv_scores_neg_mae = cross_val_score(best_model, X_scaled, y, cv=cv, scoring='neg_mean_absolute_error')
    
    # Calculate aggregate metrics
    mean_r2 = np.mean(cv_scores_r2)
    mean_mse = -np.mean(cv_scores_neg_mse)
    mean_mae = -np.mean(cv_scores_neg_mae)
    rmse = np.sqrt(mean_mse)
    
    # Calculate MAPE manually generally, but sklearn has it too now: 'neg_mean_absolute_percentage_error'
    # We can just do a predictable train/test split for a final robust metric set or stick to CV mean
    # Let's do a hold-out test set evaluation for final detailed metrics
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    
    test_r2 = r2_score(y_test, y_pred)
    test_mse = mean_squared_error(y_test, y_pred)
    test_mae = mean_absolute_error(y_test, y_pred)
    test_mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    result_entry = {
        'Model': name,
        'Best Params': grid.best_params_,
        'CV Mean R2': mean_r2,
        'CV Mean MSE': mean_mse,
        'Test R2': test_r2,
        'Test MSE': test_mse,
        'Test MAE': test_mae,
        'Test MAPE': test_mape
    }
    results.append(result_entry)
    print(f"  > Test R2: {test_r2:.4f}, Test MAPE: {test_mape:.2f}%")

# Save Results
results_df = pd.DataFrame(results)
results_df.to_csv('results/model_comparison_metrics.csv', index=False)
print("\nResults saved to results/model_comparison_metrics.csv")

# Identify Best Model based on Test R2
best_model_name = results_df.loc[results_df['Test R2'].idxmax()]['Model']
print(f"Best Model Overall: {best_model_name}")

# Save the name of the best model for usage in visualizer/app
with open('models/best_model_info.json', 'w') as f:
    json.dump({'best_model_name': best_model_name}, f)

print("Training Complete.")
