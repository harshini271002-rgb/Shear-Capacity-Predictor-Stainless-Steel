import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import shap
import matplotlib.pyplot as plt
import os

# --- Page Config ---
st.set_page_config(page_title="Shear Capacity Analysis", layout="wide", page_icon="🏗️")

# --- CSS Styling ---
st.markdown("""
<style>
    .main {background-color: #1e1e2f; color: #ffffff;}
    h1, h2, h3 {color: #e2a9a9;}
    .stTabs [data-baseweb="tab-list"] {gap: 20px;}
    .stTabs [data-baseweb="tab"] {background-color: #2b2b40; color: #fff; border-radius: 5px; padding: 10px 20px;}
    .stTabs [aria-selected="true"] {background-color: #5c5c99 !important; border-bottom: none;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #f9a8d4;'>🏗️ Lipped Channel Beam Shear Capacity Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1aa;'>Stainless Steel Beams - With & Without Web Perforations | ML-Powered Predictions</p>", unsafe_allow_html=True)
st.markdown("<div style='display: flex; justify-content: center; gap: 10px;'>"
            "<span style='background: #312e81; padding: 5px 15px; border-radius: 20px;'>⚙️ FEA-Calibrated</span>"
            "<span style='background: #831843; padding: 5px 15px; border-radius: 20px;'>🤖 ML Predictions</span>"
            "<span style='background: #1e3a8a; padding: 5px 15px; border-radius: 20px;'>📊 9 Methods</span>"
            "</div><br><br>", unsafe_allow_html=True)

if not os.path.exists('model_metrics.csv'):
    st.warning("Models are currently training in the background. Please wait a few minutes and refresh this page. You can still see the UI structure!")
else:
    @st.cache_data
    def load_metrics():
        return pd.read_csv('model_metrics.csv', index_col=0)

@st.cache_data
def load_data():
    if os.path.exists('synthetic_beam_dataset.csv'):
        return pd.read_csv('synthetic_beam_dataset.csv')
    return pd.DataFrame()

@st.cache_resource
def load_models():
    models = {}
    model_names = ['Decision Tree', 'Random Forest', 'KNN', 'Gradient Boosting', 'XGBoost', 'LightGBM', 'CatBoost', 'SVR', 'MLP']
    for name in model_names:
        try:
            with open(f'{name.replace(" ", "_")}_model.pkl', 'rb') as f:
                models[name] = pickle.load(f)
        except:
            pass
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
    except:
        scaler = None
    return models, scaler

df = load_data()
if os.path.exists('model_metrics.csv'):
    metrics_df = load_metrics()
models, scaler = load_models()

tabs = st.tabs(["Predictor", "Beam Visualizer", "Failure Modes", "Analysis Graphs", "Applications"])

# --- Predictor Tab ---
with tabs[0]:
    st.markdown("### 💡 Shear Capacity Predictor")
    with st.form("predictor_form"):
        col1, col2 = st.columns(2)
        with col1:
            D = st.number_input("TOTAL DEPTH (D) [mm]", min_value=100.0, max_value=500.0, value=150.0)
            tw = st.number_input("WEB THICKNESS (tw) [mm]", min_value=1.0, max_value=5.0, value=1.5)
            B = st.number_input("FLANGE WIDTH (B) [mm]", min_value=30.0, max_value=150.0, value=60.0)
            L = st.number_input("LENGTH (L) [mm]", min_value=500.0, max_value=5000.0, value=1500.0)
        with col2:
            fy = st.number_input("YIELD STRENGTH (fy) [MPa]", min_value=200.0, max_value=800.0, value=350.0)
            E = st.number_input("YOUNGS MODULUS (E) [GPa]", min_value=150.0, max_value=250.0, value=200.0)
            v = st.number_input("POISSON RATIO", min_value=0.2, max_value=0.4, value=0.3)
            ratio = st.number_input("OPENING RATIO (d/D) [0 to 0.8]", min_value=0.0, max_value=0.8, value=0.2)
        submit = st.form_submit_button("Predict Shear Capacity")
        
    if submit:
        st.success("Predictions Generated!")
        # Create input df
        input_data = pd.DataFrame([[D, tw, B, L, fy, E, v, ratio]], 
                                  columns=['Depth_D_mm', 'Web_Thickness_tw_mm', 'Flange_B_mm', 'Length_L_mm', 
                                           'Yield_Strength_fy_MPa', 'Youngs_Modulus_E_GPa', 'Poisson_Ratio', 'Opening_Ratio'])
        
        preds = {}
        for name, m in models.items():
            if name in ['SVR', 'MLP', 'KNN'] and scaler:
                pred = m.predict(scaler.transform(input_data))[0]
            else:
                pred = m.predict(input_data)[0]
            preds[name] = pred
        
        if len(preds) == 0:
            st.warning("Models are still training!")
        else:
            cols = st.columns(4)
            for i, (name, pred) in enumerate(preds.items()):
                cols[i%4].metric(label=f"{name} (kN)", value=f"{pred:.2f}")

# --- Beam Visualizer Tab ---
with tabs[1]:
    st.markdown("### 📊 Beam Geometry Visualization")
    st.write("Cross-section view with perforation (Mockup).")
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-30, y0=-150, x1=30, y1=150, line=dict(color="RoyalBlue"), fillcolor="LightSkyBlue")
    fig.add_shape(type="circle", x0=-20, y0=-20, x1=20, y1=20, line_color="red", fillcolor="white")
    fig.update_layout(width=400, height=400, xaxis=dict(range=[-100, 100]), yaxis=dict(range=[-200, 200]), template="plotly_dark")
    st.plotly_chart(fig)

# --- Failure Modes Tab ---
with tabs[2]:
    st.markdown("### ⚠️ Failure Modes")
    st.info("Theoretical Models Comparison: Tension Field Action, Eurocode, Vierendeel Mechanism.")
    st.write("ML Models accurately capture shear buckling and tension field variations induced by perforations.")
    # Plot comparing FEA vs Eurocode vs TF
    if not df.empty:
        sample_df = df.sample(min(100, len(df)))
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=sample_df.index, y=sample_df['FEA_Shear_Capacity_kN'], name='FEA Capacity'))
        fig2.add_trace(go.Scatter(x=sample_df.index, y=sample_df['Eurocode_Capacity_kN'], name='Eurocode'))
        fig2.add_trace(go.Scatter(x=sample_df.index, y=sample_df['With_Tension_Field_kN'], name='Tension Field'))
        fig2.update_layout(template="plotly_dark", title="Theoretical vs FEA Capacities")
        st.plotly_chart(fig2, use_container_width=True)

# --- Analysis Graphs Tab ---
with tabs[3]:
    st.markdown("### 📈 Comprehensive ML Analysis")
    g_tabs = st.tabs(["Metrics & Architecture", "Distributions & Correlations", "SHAP Analysis (CatBoost)", "Contour/Performance Plots"])
    
    with g_tabs[0]:
        st.write("#### Cross Validation (10-Folds) & Tuning Metrics")
        if os.path.exists('model_metrics.csv'):
            st.dataframe(metrics_df.style.highlight_max(axis=0, subset=['Train R2','Test R2']))
        else:
            st.write("Waiting for models to complete training...")
        st.write("""
        **Architectural Overview of ML Models:**
        - **Tree-Based:** Random Forest, Decision Tree, Gradient Boosting, XGBoost, LightGBM, CatBoost. They use hierarchical splits over depth/tw/opening ratio avoiding complex data-scaling.
        - **Distance & Network-Based:** KNN, SVR, MLP. They map relationships in hyperplanes (SVR) or layered nodes (MLP), utilizing normalized inputs.
        """)
        
    with g_tabs[1]:
        st.write("#### Distributions and Ultimate Load vs Shear Capacity")
        if not df.empty:
            colA, colB = st.columns(2)
            with colA:
                fig_hist = px.histogram(df, x="Ultimate_Load_kN", marginal="box", title="Distribution of Ultimate Load Tests", template="plotly_dark", color_discrete_sequence=['#fb7185'])
                st.plotly_chart(fig_hist, use_container_width=True)
            with colB:
                corr = df[['FEA_Shear_Capacity_kN', 'Ultimate_Load_kN', 'Depth_D_mm', 'Yield_Strength_fy_MPa', 'Opening_Ratio', 'Web_Thickness_tw_mm']].corr()
                fig_corr = px.imshow(corr, text_auto=True, title="Correlation Matrix", color_continuous_scale="RdBu_r", template="plotly_dark")
                st.plotly_chart(fig_corr, use_container_width=True)
            
    with g_tabs[2]:
        st.write("#### SHAP Feature Importance & Plots (CatBoost)")
        if 'CatBoost' in models and not df.empty:
            cat_model = models['CatBoost']
            features = ['Depth_D_mm', 'Web_Thickness_tw_mm', 'Flange_B_mm', 'Length_L_mm', 
                        'Yield_Strength_fy_MPa', 'Youngs_Modulus_E_GPa', 'Poisson_Ratio', 'Opening_Ratio']
            explainer = shap.TreeExplainer(cat_model)
            sample_X = df[features].sample(min(100, len(df)))
            shap_values = explainer.shap_values(sample_X)
            
            scol1, scol2 = st.columns(2)
            with scol1:
                st.write("**SHAP Summary Plot**")
                fig_shap, ax = plt.subplots()
                shap.summary_plot(shap_values, sample_X, show=False)
                st.pyplot(fig_shap)
            with scol2:
                st.write("**SHAP Dependence Plot (Opening Ratio)**")
                fig_dep, ax = plt.subplots()
                shap.dependence_plot("Opening_Ratio", shap_values, sample_X, show=False, ax=ax)
                st.pyplot(fig_dep)
        else:
            st.warning("CatBoost model not found or data missing. Still training.")
            
    with g_tabs[3]:
        st.write("#### Contour Plot: Shear Capacity vs Depth & Opening Ratio")
        if not df.empty:
            fig_contour = go.Figure(data=
                go.Contour(
                    z=df['FEA_Shear_Capacity_kN'],
                    x=df['Opening_Ratio'],
                    y=df['Depth_D_mm'],
                    colorscale='Viridis'
                ))
            fig_contour.update_layout(title="Contour Plot of Shear Capacity", xaxis_title="Opening Ratio", yaxis_title="Depth (D) [mm]", template="plotly_dark")
            st.plotly_chart(fig_contour, use_container_width=True)

# --- Applications Tab ---
with tabs[4]:
    st.markdown("### 🏢 Practical Applications")
    st.info("The models herein can be directly applied to rapid sizing and safety checking of custom stainless steel profiled lipped channels in structural engineering projects.")

