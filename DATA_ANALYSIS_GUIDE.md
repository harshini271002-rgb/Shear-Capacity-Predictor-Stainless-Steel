# Interactive Data Analysis Tool - User Guide

## What You Got

I've created **`interactive_data_analyzer.py`** - a powerful tool that:

### 1. **Loads and Analyzes Your Data**
- Reads `final_predictions.csv` (100 beam sections)
- Calculates comprehensive statistics
- Generates automatic findings

### 2. **Automatic Findings Generation**
The script analyzes your data and generates findings like:
- Data quality assessment
- Model performance evaluation (R²=0.9952!)
- Error analysis
- Feature importance
- Web opening effects on capacity
- Correlations

### 3. **Visual Analysis**
Generates 4 key plots:
- Predicted vs Actual scatter
- Error distribution histogram
- Web opening effect
- Capacity distribution

### 4. **Exports Reports**
Creates two files:
- `data_analysis_findings.png` - Visual plots
- `FINDINGS_REPORT.md` - Detailed findings report

## How to Use

### Run the Analysis:
```bash
python interactive_data_analyzer.py
```

### Edit Data:
1. Open `final_predictions.csv` in Excel/LibreOffice
2. Make your changes (edit values, add rows, etc.)
3. Save the file
4. Re-run the script to get updated findings!

### What the Script Shows:
- ✓ Data preview (first 10 rows)
- ✓ Statistical summary  
- ✓ Performance metrics (R², MAPE, MSE, MAE)
- ✓ Automatic key findings (6+ insights)
- ✓ Visual plots

## Example Findings Output

```
>> KEY FINDINGS:

1. [High] Data Overview
   → Dataset contains 100 beam sections with 86 parameters.

2. [Critical] Model Performance
   → Excellent prediction accuracy achieved with R² = 0.9952

3. [High] Error Analysis
   → Average prediction error: 4.22%, Maximum error: 20.44%

4. [Critical] Opening Effect
   → Web perforations reduce shear capacity by approximately 35%

5. [High] Feature Importance
   → Top correlated features: d1, tw, fyw
```

## Files Generated

After running, check:
1. **`output/data_analysis_findings.png`** - 4 analysis plots
2. **`FINDINGS_REPORT.md`** - Complete findings report

## View the Report

[Open Findings Report](file:///e:/Input%20Day%202/FINDINGS_REPORT.md)

## Quick Access

- **Data File**: [final_predictions.csv](file:///e:/Input%20Day%202/final_predictions.csv)
- **Analysis Script**: [interactive_data_analyzer.py](file:///e:/Input%20Day%202/interactive_data_analyzer.py)
- **Plots**: [data_analysis_findings.png](file:///e:/Input%20Day%202/output/data_analysis_findings.png)
