from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import json
import os

app = FastAPI(title="Shear Capacity Predictor")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Scaler
try:
    scaler = joblib.load('../models/scaler.pkl')
    
    with open('../models/best_model_info.json', 'r') as f:
        info = json.load(f)
    best_model_name = info['best_model_name']
    model = joblib.load(f'../models/{best_model_name}_best.pkl')
    print(f"Loaded model: {best_model_name}")
except Exception as e:
    print(f"Error loading models: {e}")
    scaler = None
    model = None

class BeamInput(BaseModel):
    dwh_d1: float
    d1: float
    tw: float
    flange_width: float
    total_depth: float
    fyw: float
    E: float
    a_d: float

@app.get("/")
def read_root():
    return {"message": "Shear Capacity Prediction API is running"}

@app.post("/predict")
def predict(input_data: BeamInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Feature order must match training:
    # 'Depth of Web opening(dwh/d1)', 'd1', 'tw', 'flange width(mm)', 'total depth D (mm)', 'fyw', 'E', 'a/d'
    
    features = [
        input_data.dwh_d1,
        input_data.d1,
        input_data.tw,
        input_data.flange_width,
        input_data.total_depth,
        input_data.fyw,
        input_data.E,
        input_data.a_d
    ]
    
    # Scale
    features_scaled = scaler.transform([features])
    
    # Predict
    prediction = model.predict(features_scaled)
    
    return {"shear_capacity_kN": float(prediction[0])}

from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
import io

@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if not file.filename.endswith(('.xlsx', '.csv', '.xls')):
        raise HTTPException(status_code=400, detail="Must be an Excel or CSV file")
        
    try:
        content = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
            
        required_cols = [
            'Depth of Web opening(dwh/d1)', 'd1', 'tw', 
            'flange width(mm)', 'total depth D (mm)', 'fyw', 'E', 'a/d'
        ]
        
        # Check for missing columns 
        # (Be slightly flexible: find columns that exist, or do exact match)
        # We will require exact match for simplicity.
        actual_cols = df.columns.tolist()
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        # If headers are slightly different (e.g. from the UI map), we could try mapping them.
        # But let's stick to exact match and inform user.
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"Missing required columns in uploaded spreadsheet: {missing_cols}. Columns found: {df.columns.tolist()}")
            
        # Extract features
        X = df[required_cols]
        # Fill missing values with 0
        if X.isnull().values.any():
            X = X.fillna(0)
            
        # Scale inputs
        X_scaled = scaler.transform(X)
        
        # Predict
        predictions = model.predict(X_scaled)
        
        # Add to dataframe
        df['Predicted_Shear_Capacity_kN'] = predictions
        
        # Save to buffer
        output = io.BytesIO()
        if file.filename.endswith('.csv'):
            df.to_csv(output, index=False)
            media_type = "text/csv"
            out_filename = "predictions_" + file.filename
        else:
            df.to_excel(output, index=False, engine='openpyxl')
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            out_filename = "predictions_" + file.filename
            
        output.seek(0)
        
        # Return as downloadable file string
        headers = {
            'Content-Disposition': f'attachment; filename="{out_filename}"'
        }
        return StreamingResponse(output, headers=headers, media_type=media_type)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
