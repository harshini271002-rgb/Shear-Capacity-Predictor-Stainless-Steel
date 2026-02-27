import re
with open('e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix multiple tabs
text = re.sub(
    r'(<div class="card" style="margin-top:20px; background: rgba\(102, 126, 234, 0\.1\);">\s*<div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">\s*<span style="font-size:1\.6rem;">📊</span>\s*<h3 style="color:white; margin:0;">Method Comparison & Engineering Data</h3>\s*</div>.*?</div>\s*</div>\s*)+',
    r'\1', text, flags=re.DOTALL
)

with open('e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html', 'w', encoding='utf-8') as f:
    f.write(text)
    print("Fixed multiple tables!")
