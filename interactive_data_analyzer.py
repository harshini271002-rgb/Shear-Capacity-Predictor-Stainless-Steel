"""
Interactive Data Analysis and Findings Generator
This script allows you to load, edit, analyze, and generate findings from the shear capacity data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import warnings
import sys
import io
warnings.filterwarnings('ignore')

# Fix encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.unicode.east_asian_width', True)
sns.set(style="whitegrid")

class DataAnalyzer:
    def __init__(self, data_path='e:/Input Day 2/final_predictions.csv'):
        """Initialize with data path"""
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Load the data"""
        print("=" * 80)
        print("LOADING DATA")
        print("=" * 80)
        self.df = pd.read_csv(self.data_path)
        print(f"[OK] Loaded {len(self.df)} records")
        print(f"[OK] Columns: {len(self.df.columns)}")
        print("\n")
        
    def show_data(self, n=10):
        """Display first n rows"""
        print("=" * 80)
        print(f"DATA PREVIEW (First {n} rows)")
        print("=" * 80)
        print(self.df.head(n))
        print("\n")
        
    def edit_data_interactive(self):
        """Interactive data editing"""
        print("=" * 80)
        print("INTERACTIVE DATA EDITOR")
        print("=" * 80)
        print("Options:")
        print("1. Edit specific value")
        print("2. Filter data by condition")
        print("3. Add new column")
        print("4. Remove column")
        print("5. Save changes")
        print("6. Exit editor")
        print("\n")
        
    def get_statistics(self):
        """Get comprehensive statistics"""
        print("=" * 80)
        print("STATISTICAL SUMMARY")
        print("=" * 80)
        
        # Basic stats
        print("\n1. DESCRIPTIVE STATISTICS:")
        print(self.df.describe())
        
        # Prediction accuracy if available
        if 'VU(FEA)' in self.df.columns and 'Predicted_Shear_Capacity_kN' in self.df.columns:
            actual = self.df['VU(FEA)'].dropna()
            predicted = self.df['Predicted_Shear_Capacity_kN'][:len(actual)]
            
            r2 = r2_score(actual, predicted)
            mse = mean_squared_error(actual, predicted)
            mae = mean_absolute_error(actual, predicted)
            mape = np.mean(np.abs((actual - predicted) / actual)) * 100
            
            print("\n2. PREDICTION ACCURACY:")
            print(f"   R² Score:  {r2:.6f}")
            print(f"   MAPE:      {mape:.4f}%")
            print(f"   MSE:       {mse:.4f}")
            print(f"   MAE:       {mae:.4f}")
            print(f"   RMSE:      {np.sqrt(mse):.4f}")
        
        print("\n")
        
    def generate_findings(self):
        """Generate comprehensive findings"""
        print("=" * 80)
        print("AUTOMATIC FINDINGS GENERATION")
        print("=" * 80)
        
        findings = []
        
        # Finding 1: Data Overview
        findings.append({
            'category': 'Data Overview',
            'finding': f'Dataset contains {len(self.df)} beam sections with {len(self.df.columns)} parameters.',
            'significance': 'High'
        })
        
        # Finding 2: Prediction Performance
        if 'VU(FEA)' in self.df.columns and 'Predicted_Shear_Capacity_kN' in self.df.columns:
            actual = self.df['VU(FEA)'].dropna()
            predicted = self.df['Predicted_Shear_Capacity_kN'][:len(actual)]
            r2 = r2_score(actual, predicted)
            
            if r2 > 0.99:
                quality = "Excellent prediction accuracy"
            elif r2 > 0.95:
                quality = "Very good prediction accuracy"
            elif r2 > 0.90:
                quality = "Good prediction accuracy"
            else:
                quality = "Moderate prediction accuracy"
                
            findings.append({
                'category': 'Model Performance',
                'finding': f'{quality} achieved with R² = {r2:.4f}',
                'significance': 'Critical'
            })
        
        # Finding 3: Error Analysis
        if 'Percentage_Error' in self.df.columns:
            errors = self.df['Percentage_Error'].dropna()
            avg_error = errors.mean()
            max_error = errors.max()
            
            findings.append({
                'category': 'Error Analysis',
                'finding': f'Average prediction error: {avg_error:.2f}%, Maximum error: {max_error:.2f}%',
                'significance': 'High'
            })
        
        # Finding 4: Feature Ranges
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        key_features = ['d1', 'tw', 'fyw', 'E']
        
        for col in key_features:
            if col in numeric_cols:
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                findings.append({
                    'category': 'Data Range',
                    'finding': f'{col}: Range from {min_val:.2f} to {max_val:.2f}',
                    'significance': 'Medium'
                })
        
        # Finding 5: Correlation Analysis
        if 'VU(FEA)' in self.df.columns:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if 'VU(FEA)' in numeric_df.columns:
                correlations = numeric_df.corr()['VU(FEA)'].abs().sort_values(ascending=False)
                top_features = correlations.head(4).index.tolist()[1:]  # Exclude self-correlation
                
                findings.append({
                    'category': 'Feature Importance',
                    'finding': f'Top correlated features with shear capacity: {", ".join(top_features)}',
                    'significance': 'High'
                })
        
        # Finding 6: Web Opening Effect
        if 'Depth of Web opening(dwh/d1)' in self.df.columns and 'VU(FEA)' in self.df.columns:
            no_opening = self.df[self.df['Depth of Web opening(dwh/d1)'] == 0]['VU(FEA)'].mean()
            with_opening = self.df[self.df['Depth of Web opening(dwh/d1)'] > 0]['VU(FEA)'].mean()
            reduction = ((no_opening - with_opening) / no_opening) * 100
            
            findings.append({
                'category': 'Opening Effect',
                'finding': f'Web perforations reduce shear capacity by approximately {reduction:.1f}%',
                'significance': 'Critical'
            })
        
        # Print findings
        print("\n>> KEY FINDINGS:\n")
        for i, finding in enumerate(findings, 1):
            print(f"{i}. [{finding['significance']}] {finding['category']}")
            print(f"   → {finding['finding']}\n")
        
        return findings
    
    def plot_analysis(self):
        """Generate analysis plots"""
        print("=" * 80)
        print("GENERATING ANALYSIS PLOTS")
        print("=" * 80)
        
        if 'VU(FEA)' not in self.df.columns:
            print("Cannot generate plots - VU(FEA) column not found")
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Actual vs Predicted
        if 'Predicted_Shear_Capacity_kN' in self.df.columns:
            actual = self.df['VU(FEA)'].dropna()
            predicted = self.df['Predicted_Shear_Capacity_kN'][:len(actual)]
            
            axes[0, 0].scatter(actual, predicted, alpha=0.6)
            axes[0, 0].plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'r--', lw=2)
            axes[0, 0].set_xlabel('Actual Shear Capacity (kN)')
            axes[0, 0].set_ylabel('Predicted Shear Capacity (kN)')
            axes[0, 0].set_title('Predicted vs Actual')
            axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Error Distribution
        if 'Percentage_Error' in self.df.columns:
            axes[0, 1].hist(self.df['Percentage_Error'].dropna(), bins=20, edgecolor='black', alpha=0.7)
            axes[0, 1].axvline(x=0, color='r', linestyle='--', lw=2)
            axes[0, 1].set_xlabel('Percentage Error (%)')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].set_title('Error Distribution')
            axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Opening Effect
        if 'Depth of Web opening(dwh/d1)' in self.df.columns:
            self.df.plot(x='Depth of Web opening(dwh/d1)', y='VU(FEA)', 
                        kind='scatter', ax=axes[1, 0], alpha=0.6)
            axes[1, 0].set_xlabel('Web Opening Ratio (dwh/d1)')
            axes[1, 0].set_ylabel('Shear Capacity (kN)')
            axes[1, 0].set_title('Effect of Web Opening on Capacity')
            axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Capacity Distribution
        axes[1, 1].hist(self.df['VU(FEA)'].dropna(), bins=25, edgecolor='black', alpha=0.7, color='green')
        axes[1, 1].set_xlabel('Shear Capacity (kN)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Shear Capacity Distribution')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('e:/Input Day 2/output/data_analysis_findings.png', dpi=150)
        print("[OK] Plots saved to: output/data_analysis_findings.png")
        plt.show()
    
    def export_findings_report(self, findings):
        """Export findings to markdown report"""
        report_path = 'e:/Input Day 2/FINDINGS_REPORT.md'
        
        with open(report_path, 'w') as f:
            f.write("# Data Analysis Findings Report\n\n")
            f.write(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"This report presents findings from the analysis of {len(self.df)} stainless steel beam sections.\n\n")
            
            f.write("## Key Findings\n\n")
            for i, finding in enumerate(findings, 1):
                f.write(f"### {i}. {finding['category']} [{finding['significance']}]\n\n")
                f.write(f"{finding['finding']}\n\n")
            
            f.write("## Statistical Summary\n\n")
            f.write("```\n")
            f.write(str(self.df.describe()))
            f.write("\n```\n\n")
            
            if 'VU(FEA)' in self.df.columns and 'Predicted_Shear_Capacity_kN' in self.df.columns:
                actual = self.df['VU(FEA)'].dropna()
                predicted = self.df['Predicted_Shear_Capacity_kN'][:len(actual)]
                r2 = r2_score(actual, predicted)
                mape = np.mean(np.abs((actual - predicted) / actual)) * 100
                
                f.write("## Model Performance\n\n")
                f.write(f"- **R² Score:** {r2:.6f}\n")
                f.write(f"- **MAPE:** {mape:.4f}%\n\n")
            
            f.write("## Visualizations\n\n")
            f.write("![Analysis Plots](file:///e:/Input%20Day%202/output/data_analysis_findings.png)\n\n")
        
        print(f"[OK] Findings report saved to: {report_path}")

# Main execution
if __name__ == "__main__":
    print("\n>>> INTERACTIVE DATA ANALYZER <<<\n")
    
    # Initialize analyzer
    analyzer = DataAnalyzer()
    
    # Show data
    analyzer.show_data(10)
    
    # Get statistics
    analyzer.get_statistics()
    
    # Generate findings
    findings = analyzer.generate_findings()
    
    # Create plots
    analyzer.plot_analysis()
    
    # Export report
    analyzer.export_findings_report(findings)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n>> Files Generated:")
    print("   1. output/data_analysis_findings.png")
    print("   2. FINDINGS_REPORT.md")
    print("\n>> To edit data manually:")
    print("   1. Open: final_predictions.csv in Excel")
    print("   2. Make changes and save")
    print("   3. Re-run this script: python interactive_data_analyzer.py")
    print("\n")
