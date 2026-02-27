import re

with open('e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html', 'r', encoding='utf-8') as f:
    text = f.read()

ids_in_js = re.findall(r"getElementById\('([^']+)'\)", text)
ids_in_js += re.findall(r'getElementById\("([^"]+)"\)', text)
ids_in_html = re.findall(r'id=["\']([^"\']+)["\']', text)

missing = set(ids_in_js) - set(ids_in_html)
print('Missing IDs used in JS:', missing)
