---
name: demo
description: Pre-demo checklist — run at 18:30 before presentations start
allowed_tools: ["Bash", "Read"]
---

Run through this before the 2-minute demo:

## Checklist

1. App is running: `streamlit run app.py`
2. Data is loaded (no blank charts on first tab open)
3. Pick your 3 demo regions — run this to find the best:

```bash
python -c "
import pandas as pd
df = pd.read_csv('data/cfos_statistics.csv')
top = df[df['is_lowest_level']==True].assign(afc=lambda d: d['log2_fold_change'].abs()).nlargest(5,'afc')[['acronym','region_name','log2_fold_change','p_corrected','significant_corrected']]
print(top.to_string())
"
```

4. Test the Claude "Explain this region" button on your chosen region — confirm it returns text
5. Brain slice renders for your chosen region (not a blank/error)
6. Have the 2-minute script ready (see hackathon_strategy.md)

## Demo narrative skeleton
- 0:00 Hook: "Ozempic changes the brain. We built a tool to see exactly where."
- 0:15 Volcano: point to top hits, name NTS/ARC/CEA
- 0:30 Click top region → violin → brain slice
- 0:45 Click Explain → Claude output live on screen
- 1:00 Unexpected finding: one surprising region with high significance
- 1:30 Scalability: "works for any Vibraint study"
- 1:45 Close
