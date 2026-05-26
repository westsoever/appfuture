---
name: session-context
description: Load full project context at the start of a new Claude Code session
allowed_tools: ["Read"]
---

Read and internalize these files in order, then confirm you're ready with a one-line status:

1. Read `CLAUDE.md` — module map, data schema, run command
2. Read `hackathon_strategy.md` — challenge choice rationale, winning app blueprint, demo script
3. Run this to see current build state:

```bash
ls -la *.py && python smoke_test.py 2>/dev/null || echo "data not downloaded yet"
```

After reading, respond with exactly:
> Context loaded. [X] files present. Top priority: [one thing to do next].

Do not summarize what you read. Just confirm and state the next action.
