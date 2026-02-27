import pandas as pd
import numpy as np

def generate_beam_data(num_samples=1000):
    np.random.seed(42)
    
    # Beam geometries
    D = np.random.uniform(100, 300, num_samples) # Depth
    tw = np.random.uniform(1.2, 3.0, num_samples) # Web thickness
    B = np.random.uniform(50, 100, num_samples) # Flange
    L = np.random.uniform(1000, 3000, num_samples) # Length
    
    # Material properties
    fy = np.random.uniform(250, 550, num_samples) # Yield strength
    E = np.random.normal(200, 5, num_samples) # Young's modulus E in GPa
    poisson = np.random.normal(0.3, 0.01, num_samples) # Poisson ratio
    
    # Perforation configuration
    opening_ratio = np.random.uniform(0.0, 0.8, num_samples) # a/d1 or d0/D
    
    # Non-linear synthetic relations to get reasonable capacities
    area = (D + 2 * B) * tw
    web_area = (D - 2 * tw) * tw
    tau_y = fy / np.sqrt(3) # Shear yield stress
    
    # Theoretical capacities
    base_shear = web_area * tau_y / 1000 # in kN
    reduction_factor = 1.0 - (1.1 * opening_ratio) + 0.2 * (opening_ratio ** 2)
    reduction_factor = np.clip(reduction_factor, 0.2, 1.0) # avoid negative or too small
    
    # Introduce some non-linear dependencies
    V_FEA = base_shear * reduction_factor * (1.0 + 0.05 * np.sin(D/50)) + np.random.normal(0, 5, num_samples)
    V_Ultimate = V_FEA * np.random.uniform(1.05, 1.15, num_samples)
    
    V_Eurocode = base_shear * reduction_factor * 0.9 + np.random.normal(0, 2, num_samples)
    V_TensionField = base_shear * reduction_factor * 1.1 + np.random.normal(0, 3, num_samples)
    V_WithoutTF = base_shear * reduction_factor * 0.85 + np.random.normal(0, 2, num_samples)
    
    # Assemble dataframe
    df = pd.DataFrame({
        'Depth_D_mm': D,
        'Web_Thickness_tw_mm': tw,
        'Flange_B_mm': B,
        'Length_L_mm': L,
        'Yield_Strength_fy_MPa': fy,
        'Youngs_Modulus_E_GPa': E,
        'Poisson_Ratio': poisson,
        'Opening_Ratio': opening_ratio,
        'FEA_Shear_Capacity_kN': V_FEA,
        'Ultimate_Load_kN': V_Ultimate,
        'Eurocode_Capacity_kN': V_Eurocode,
        'With_Tension_Field_kN': V_TensionField,
        'Without_Tension_Field_kN': V_WithoutTF
    })
    
    # Ensure no negative capacities
    for col in ['FEA_Shear_Capacity_kN', 'Ultimate_Load_kN', 'Eurocode_Capacity_kN', 'With_Tension_Field_kN', 'Without_Tension_Field_kN']:
        df[col] = df[col].apply(lambda x: max(x, 5.0))
        
    df.to_csv('synthetic_beam_dataset.csv', index=False)
    print(f"Generated synthetic dataset with {len(df)} samples using provided theoretical formulas/properties.")

if __name__ == '__main__':
    generate_beam_data()
