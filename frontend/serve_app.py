import streamlit as st
import os

st.set_page_config(page_title="Lipped Channel Beam Analysis", layout="wide")

html_path = os.path.join(os.path.dirname(__file__), "complete_analysis.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=1200, scrolling=True)
