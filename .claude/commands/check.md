---
name: check
description: Smoke-test data files and app imports — run after download_data.py
allowed_tools: ["Bash"]
---

Run the smoke test to verify everything is in place:

```bash
python smoke_test.py
```

Expected output:
- All 8 data files present ✓
- cfos_statistics.csv columns match expected schema ✓
- Top 3 regions by |log2FC| printed
- Claude API key found ✓

If any check fails, the script prints what's missing and what to do.
