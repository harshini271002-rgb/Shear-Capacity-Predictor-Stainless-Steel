@echo off
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Installation complete. You can now run the visualization script again to generate SHAP plots.
echo python visualize_results.py
pause
