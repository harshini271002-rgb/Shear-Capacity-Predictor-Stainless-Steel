import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    # Read the file, skipping the first 2 rows which seem to be headers/groupings
    # The actual header is likely on line 3 (index 2)
    df = pd.read_csv(filepath, header=2)
    
    # Print initial info
    print("\nInitial DataFrame Shape:", df.shape)
    # Safely print columns
    safe_cols = [str(c).encode('ascii', 'replace').decode('ascii') for c in df.columns]
    print("\nInitial Columns:", safe_cols)
    
    # Select relevant features and target
    # Based on the plan: 
    # Features: Depth of Web opening(dwh/d1), d1, tw, flange width(mm), total depth D (mm), fyw, E, a/d
    # Target: VU(FEA)
    
    target_col = 'VU(FEA)'
    feature_cols = [
        'Depth of Web opening(dwh/d1)', 
        'd1', 
        'tw', 
        'flange width(mm)', 
        'total depth D (mm)', 
        'fyw', 
        'E', 
        'a/d'
    ]
    
    # Check if columns exist
    missing_cols = [col for col in feature_cols + [target_col] if col not in df.columns]
    if missing_cols:
        print(f"WARNING: The following columns are missing: {missing_cols}")
        # Try to find similar columns or handle specific cases
        # Inspecting the CSV view from previous turn, 'd1' is there, 'tw' is 'tw(mm)' maybe? 
        # Let's adjust strict matching if needed after first run
        return None
    
    df_clean = df[feature_cols + [target_col]].copy()
    
    # Drop rows where Target is NaN
    df_clean = df_clean.dropna(subset=[target_col])
    
    # Convert to numeric, coercing errors to NaN
    for col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
    # Drop any remaining NaNs
    original_len = len(df_clean)
    df_clean = df_clean.dropna()
    print(f"\nDropped {original_len - len(df_clean)} rows due to invalid numeric values.")
    print("Cleaned DataFrame Shape:", df_clean.shape)
    
    return df_clean

def perform_eda(df, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 1. Correlation Matrix
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()
    print(f"Saved correlation_matrix.png to {output_dir}")
    
    # 2. Distribution of Target
    plt.figure(figsize=(8, 6))
    sns.histplot(df['VU(FEA)'], kde=True, bins=20)
    plt.title('Distribution of Shear Capacity (VU(FEA))')
    plt.xlabel('Shear Capacity (kN)')
    plt.savefig(os.path.join(output_dir, 'distribution_vu_fea.png'))
    plt.close()
    print(f"Saved distribution_vu_fea.png to {output_dir}")
    
    # 3. Pairplot
    sns.pairplot(df)
    plt.savefig(os.path.join(output_dir, 'pairplot.png'))
    plt.close()
    print(f"Saved pairplot.png to {output_dir}")

if __name__ == "__main__":
    input_csv = "e:/Input Day 2/Input csv.csv"
    output_folder = "e:/Input Day 2/eda_output"
    
    df = load_and_clean_data(input_csv)
    
    if df is not None:
        perform_eda(df, output_folder)
        
        # Save cleaned data for next steps
        clean_data_path = "e:/Input Day 2/cleaned_data.csv"
        df.to_csv(clean_data_path, index=False)
        print(f"\nSaved cleaned data to {clean_data_path}")
