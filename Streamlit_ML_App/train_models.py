import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

def train_and_save_models():
    print("Loading data...")
    df = pd.read_csv('synthetic_beam_dataset.csv')
    
    # Features and Target
    features = ['Depth_D_mm', 'Web_Thickness_tw_mm', 'Flange_B_mm', 'Length_L_mm', 
                'Yield_Strength_fy_MPa', 'Youngs_Modulus_E_GPa', 'Poisson_Ratio', 'Opening_Ratio']
    target = 'FEA_Shear_Capacity_kN'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    cv = KFold(n_splits=10, shuffle=True, random_state=42)
    
    models = {
        'Decision Tree': (DecisionTreeRegressor(random_state=42), {'max_depth': [None, 10, 20]}),
        'Random Forest': (RandomForestRegressor(random_state=42), {'n_estimators': [50, 100], 'max_depth': [None, 10]}),
        'KNN': (KNeighborsRegressor(), {'n_neighbors': [5, 10, 15]}),
        'Gradient Boosting': (GradientBoostingRegressor(random_state=42), {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1]}),
        'XGBoost': (XGBRegressor(random_state=42, objective='reg:squarederror'), {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1]}),
        'LightGBM': (LGBMRegressor(random_state=42), {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1]}),
        'CatBoost': (CatBoostRegressor(random_state=42, verbose=0), {'iterations': [100, 200], 'learning_rate': [0.05, 0.1], 'depth': [4, 6]}),
        'SVR': (SVR(), {'C': [1.0, 10.0], 'kernel': ['rbf']}),
        'MLP': (MLPRegressor(random_state=42, max_iter=500), {'hidden_layer_sizes': [(50,), (100,)], 'alpha': [0.0001, 0.001]})
    }
    
    results = {}
    best_models = {}
    
    for name, (model, params) in models.items():
        print(f"Training {name} with 10-fold CV and Hyperparameter Tuning...")
        
        # Use unscaled for tree-based except if we already scaled, let's just use scaled for all for simplicity
        is_tree = name in ['Decision Tree', 'Random Forest', 'Gradient Boosting', 'XGBoost', 'LightGBM', 'CatBoost']
        train_x = X_train if is_tree else X_train_scaled
        test_x = X_test if is_tree else X_test_scaled
        
        grid = GridSearchCV(model, params, cv=cv, scoring='r2', n_jobs=-1)
        grid.fit(train_x, y_train)
        
        best_model = grid.best_estimator_
        y_pred_train = best_model.predict(train_x)
        y_pred_test = best_model.predict(test_x)
        
        metrics = {
            'Train R2': r2_score(y_train, y_pred_train),
            'Test R2': r2_score(y_test, y_pred_test),
            'Test MAE': mean_absolute_error(y_test, y_pred_test),
            'Test MSE': mean_squared_error(y_test, y_pred_test),
            'Test MAPE': mean_absolute_percentage_error(y_test, y_pred_test) * 100
        }
        
        results[name] = metrics
        best_models[name] = best_model
        
        with open(f'{name.replace(" ", "_")}_model.pkl', 'wb') as f:
            pickle.dump(best_model, f)
            
    # Save results
    results_df = pd.DataFrame(results).T
    results_df.to_csv('model_metrics.csv')
    print("Models trained and saved successfully!")
    print(results_df)

if __name__ == '__main__':
    train_and_save_models()
