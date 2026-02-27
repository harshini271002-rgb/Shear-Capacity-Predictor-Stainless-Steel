import pandas as pd
import joblib
import json
import os

def generate_predictions():
    print("Generating Final Predictions...")
    
    # Load Data (Full original data to keep context)
    input_path = 'e:/Input Day 2/Input csv.csv'
    df_raw = pd.read_csv(input_path, header=2)
    
    # We need to preprocess the features exactly as training
    # Training features:
    # 'Depth of Web opening(dwh/d1)', 'd1', 'tw', 'flange width(mm)', 'total depth D (mm)', 'fyw', 'E', 'a/d'
    
    feature_cols = [
        'Depth of Web opening(dwh/d1)', 'd1', 'tw', 'flange width(mm)', 
        'total depth D (mm)', 'fyw', 'E', 'a/d'
    ]
    
    # Create a copy for prediction
    df_pred = df_raw.copy()
    
    # Handle missing values in feature columns for prediction (if any)
    # We fill with 0 or drop? Training dropped. 
    # For output, we might want to predict where possible.
    # Coerce to numeric
    for col in feature_cols:
        df_pred[col] = pd.to_numeric(df_pred[col], errors='coerce')
        
    # Drop rows where features are NaN (cannot predict)
    df_valid = df_pred.dropna(subset=feature_cols).copy()
    
    # Load Scaler and Model
    scaler = joblib.load('models/scaler.pkl')
    with open('models/best_model_info.json', 'r') as f:
        info = json.load(f)
    best_model_name = info['best_model_name']
    model = joblib.load(f'models/{best_model_name}_best.pkl')
    
    print(f"Using model: {best_model_name}")
    
    # Scale Features
    X = df_valid[feature_cols]
    X_scaled = scaler.transform(X)
    
    # Predict
    predictions = model.predict(X_scaled)
    
    # Add to DataFrame
    df_valid['Predicted_Shear_Capacity_kN'] = predictions
    
    # Calculate error if Target exists
    target_col = 'VU(FEA)'
    if target_col in df_valid.columns:
        df_valid[target_col] = pd.to_numeric(df_valid[target_col], errors='coerce')
        # Only calc error where target is valid
        mask = df_valid[target_col].notna()
        df_valid.loc[mask, 'Absolute_Error'] = (df_valid.loc[mask, target_col] - df_valid.loc[mask, 'Predicted_Shear_Capacity_kN']).abs()
        df_valid.loc[mask, 'Percentage_Error'] = (df_valid.loc[mask, 'Absolute_Error'] / df_valid.loc[mask, target_col]) * 100
    
    # Save
    output_path = 'e:/Input Day 2/final_predictions.csv'
    df_valid.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")

if __name__ == "__main__":
    generate_predictions()
