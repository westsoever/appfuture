---
name: run
description: Start the Streamlit app
allowed_tools: ["Bash"]
---

Run the app:

```bash
conda run -n explainable-brains streamlit run app.py
```

If the environment isn't active yet, activate it first:
```bash
conda activate explainable-brains && streamlit run app.py
```

The app should open at http://localhost:8501. If port is busy: `streamlit run app.py --server.port 8502`
