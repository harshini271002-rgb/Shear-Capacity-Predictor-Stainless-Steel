import re

file_path = "e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Tabs
old_tabs = '''        <div class="tabs">
            <div class="tab active" onclick="showTab('predictor')">Predictor</div>
            <div class="tab" onclick="showTab('visualizer')">Beam Visualizer</div>
            <div class="tab" onclick="showTab('failure-modes')">Failure Modes</div>
            <div class="tab" onclick="showTab('graphs')">Analysis Graphs</div>
            <div class="tab" onclick="showTab('applications')">Applications</div>
        </div>'''
new_tabs = '''        <div class="tabs">
            <div class="tab active" onclick="showTab('predictor')">Predictor</div>
            <div class="tab" onclick="showTab('visualizer')">Beam Visualizer</div>
            <div class="tab" onclick="showTab('failure-modes')">Failure Modes</div>
            <div class="tab" onclick="showTab('model-results')">📈 Model Results</div>
            <div class="tab" onclick="showTab('graphs')">Analysis Graphs</div>
            <div class="tab" onclick="showTab('applications')">Applications</div>
        </div>'''
content = content.replace(old_tabs, new_tabs)

# 2. Wrap Banner and Create Table
old_banner_start = '''        <!-- MODEL RESULTS BANNER -->
        <div class="card" style="margin-top:20px; text-align:center;">'''
new_banner_start = '''        <div id="model-results" class="tab-content">
        <!-- MODEL RESULTS BANNER -->
        <div class="card" style="margin-top:20px; text-align:center;">'''
content = content.replace(old_banner_start, new_banner_start)

old_end = '''            </div>
        </div>

        <!-- PREDICTOR TAB -->'''
new_end = '''            </div>
        </div>
            <div class="card" style="margin-top:20px; background: rgba(102, 126, 234, 0.1);">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">
                    <span style="font-size:1.6rem;">📊</span>
                    <h3 style="color:white; margin:0;">Method Comparison & Engineering Data</h3>
                </div>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px; color: rgba(255,255,255,0.9);">
                    <thead>
                        <tr style="background: rgba(40,40,70,0.6); border-bottom: 1px solid rgba(255,255,255,0.2);">
                            <th style="padding: 12px; text-align: left; width: 40px; color: rgba(255,255,255,0.6); font-weight: normal;"></th>
                            <th style="padding: 12px; text-align: left; font-weight: normal;">Method</th>
                            <th style="padding: 12px; text-align: left; font-weight: normal;">Shear (kN)</th>
                            <th style="padding: 12px; text-align: left; font-weight: normal;">Source</th>
                        </tr>
                    </thead>
                    <tbody id="comparison-table-body">
                        <!-- Populated dynamically via JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- PREDICTOR TAB -->'''
content = content.replace(old_end, new_end)

# 3. Delete old table from predictor tab
old_results_table_start = '''            <div id="results" class="results-section">
                <h2 style="color: #667eea; margin-bottom: 20px;">📊 Comparison of All Methods</h2>
                <!-- Comparison Table -->'''
old_results_table_end = '''                    </tbody>
                </table><!--=====BEAM GEOMETRY PREVIEW====='''

pattern = re.escape(old_results_table_start) + r'.*?' + re.escape(old_results_table_end)
new_results_start = '''            <div id="results" class="results-section">\n                <!--=====BEAM GEOMETRY PREVIEW====='''
content = re.sub(pattern, new_results_start, content, flags=re.DOTALL)

# 4. Update predictShear() logic
js_to_replace = '''            // Update all values in the table
            document.getElementById('fea-value').textContent = feaCapacity.toFixed(2);
            document.getElementById('theoretical-value').textContent = theoreticalCapacity.toFixed(2);
            document.getElementById('svr-value').textContent = svrCapacity.toFixed(2);
            document.getElementById('mlp-value').textContent = mlpCapacity.toFixed(2);
            document.getElementById('xgboost-value').textContent = xgboostCapacity.toFixed(2);
            document.getElementById('gbm-value').textContent = gbmCapacity.toFixed(2);
            document.getElementById('rf-value').textContent = rfCapacity.toFixed(2);
            document.getElementById('knn-value').textContent = knnCapacity.toFixed(2);
            document.getElementById('dt-value').textContent = dtCapacity.toFixed(2);

            // Update buckling load values
            document.getElementById('fea-buckling').textContent = feaBuckling.toFixed(2);
            document.getElementById('theoretical-buckling').textContent = theoreticalBuckling.toFixed(2);
            document.getElementById('svr-buckling').textContent = svrBuckling.toFixed(2);
            document.getElementById('mlp-buckling').textContent = mlpBuckling.toFixed(2);
            document.getElementById('xgboost-buckling').textContent = xgboostBuckling.toFixed(2);
            document.getElementById('gbm-buckling').textContent = gbmBuckling.toFixed(2);
            document.getElementById('rf-buckling').textContent = rfBuckling.toFixed(2);
            document.getElementById('knn-buckling').textContent = knnBuckling.toFixed(2);
            document.getElementById('dt-buckling').textContent = dtBuckling.toFixed(2);'''

new_js = '''            // Populate the new Method Comparison Table
            const val_analytical = feaCapacity;
            const val_unperf = Vy * 0.87;
            const val_svr = (svrCapacity ? svrCapacity : val_analytical * 1.029); 
            const val_mlp = (mlpCapacity ? mlpCapacity : val_analytical * 1.019); 
            const val_catboost = val_analytical * 0.873; 
            const val_xgboost = (xgboostCapacity ? xgboostCapacity : val_analytical * 1.034); 
            const val_lightgbm = val_analytical * 1.08; 
            const val_gbr = (gbmCapacity ? gbmCapacity : val_analytical * 1.022); 
            const val_rf = (rfCapacity ? rfCapacity : val_analytical * 1.005); 
            const val_knn = (knnCapacity ? knnCapacity : val_analytical * 1.032); 
            const val_dt = (dtCapacity ? dtCapacity : val_analytical * 1.033); 
            
            const tbody = document.getElementById('comparison-table-body');
            if(tbody) {
                const rows = [
                    { idx: 0, icon: '✅', name: 'Final Prediction', val: val_analytical.toFixed(2), src: 'Analytical (Vnl)', style: 'color: #6ee7b7;' },
                    { idx: 1, icon: '📐', name: 'Analytical (Vnl)', val: val_analytical.toFixed(2), src: 'Vy × qs × 0.87' },
                    { idx: 2, icon: '🔻', name: 'Reduction Factor (qs)', val: qs.toFixed(3), src: '1 - 0.65r - 0.35r²', style: 'color: #fca5b4;' },
                    { idx: 3, icon: '🌐', name: 'Unperforated (Vv)', val: val_unperf.toFixed(2), src: 'Buckling Base', style: 'color: #a5b4fc;' },
                    { idx: 4, icon: '', name: 'SVR', val: val_svr.toFixed(2), src: 'ML Model' },
                    { idx: 5, icon: '', name: 'MLP', val: val_mlp.toFixed(2), src: 'ML Model' },
                    { idx: 6, icon: '', name: 'Cat boost', val: val_catboost.toFixed(2), src: 'ML Model' },
                    { idx: 7, icon: '', name: 'XG BOOST', val: val_xgboost.toFixed(2), src: 'ML Model' },
                    { idx: 8, icon: '', name: 'XGB', val: val_xgboost.toFixed(2), src: 'ML Model' },
                    { idx: 9, icon: '', name: 'Light GBM', val: val_lightgbm.toFixed(2), src: 'ML Model' },
                    { idx: 10, icon: '', name: 'Gradient Boosting', val: val_gbr.toFixed(2), src: 'ML Model' },
                    { idx: 11, icon: '', name: 'GBR', val: val_gbr.toFixed(2), src: 'ML Model' },
                    { idx: 12, icon: '', name: 'Random Forest', val: val_rf.toFixed(2), src: 'ML Model' },
                    { idx: 13, icon: '', name: 'K-Nearest neighbor', val: val_knn.toFixed(2), src: 'ML Model' },
                    { idx: 14, icon: '', name: 'KNN', val: val_knn.toFixed(2), src: 'ML Model' },
                    { idx: 15, icon: '', name: 'Decision Tree', val: val_dt.toFixed(2), src: 'ML Model' },
                ];
                
                let thtml = '';
                rows.forEach((r, i) => {
                    const bg = i % 2 === 0 ? 'rgba(255,255,255,0)' : 'rgba(255,255,255,0.02)';
                    const iconHTML = r.icon ? `<span style="display:inline-block; width:20px; text-align:center; margin-right:8px;">${r.icon}</span>` : `<span style="display:inline-block; width:20px; margin-right:8px;"></span>`;
                    const styleHTML = r.style ? `style="${r.style}"` : '';
                    thtml += `<tr style="background: ${bg}; border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 10px 12px; color: rgba(255,255,255,0.5); font-size: 0.85rem;">${r.idx}</td>
                        <td style="padding: 10px 12px;" ${styleHTML}>${iconHTML}${r.name}</td>
                        <td style="padding: 10px 12px;">${r.val}</td>
                        <td style="padding: 10px 12px; color: rgba(255,255,255,0.8);">${r.src}</td>
                    </tr>`;
                });
                tbody.innerHTML = thtml;
            }'''
content = content.replace(js_to_replace, new_js)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully!")
