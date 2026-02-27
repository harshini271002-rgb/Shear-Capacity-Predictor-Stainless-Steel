63
with open("e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("$ {", "${")

with open("e:/Input Day 5 ML Parametric study/frontend/complete_analysis.html", "w", encoding="utf-8") as f:
    f.write(content)
