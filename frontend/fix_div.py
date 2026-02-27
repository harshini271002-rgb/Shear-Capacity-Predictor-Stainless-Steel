import re
with open('e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(\s*)</div>(\s*)(<div class=\"card\" style=\"margin-top:20px; background: rgba\(102, 126, 234, 0\.1\);\">.*?</table>\s*</div>)\s*</div>'

new_text = re.sub(pattern, r'\2\3\1</div>', text, flags=re.DOTALL)

with open('e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print('Fixed dangling div and moved table inside model-results tab.')
