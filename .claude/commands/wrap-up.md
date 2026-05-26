---
name: wrap-up
description: End-of-session update — reconcile plan, log what happened, set up next session
allowed_tools: ["Read", "Bash", "Edit", "Write"]
---

Run at the end of every session. Takes 2 minutes and means the next session picks up instantly.

## Step 1 — Audit completed work
```bash
ls -la *.py && git diff --stat 2>/dev/null || true
```

For every item in "In Progress" and "Up Next" in `ACTIVE_PLAN.md`:
- If it's done → move to "Done"
- If it's partially done → keep in "In Progress", add a note
- If it's no longer relevant → remove it

## Step 2 — Capture blockers
Add anything to "Blockers & Manual Input Needed" that:
- Requires a credential, URL, or decision from the user
- Is waiting on an external event (e.g. credentials at 16:00)
- Could not be completed without human action

Format: `- [ ] 🔑/🌐/❓/👥 **Short label** — what exactly is needed and where`

## Step 3 — Revise and improve the plan
Look at "Up Next" and "Backlog" with fresh eyes:
- Reorder tasks by impact given current state
- Add any new tasks discovered during this session
- Remove tasks that are no longer needed
- If the build timeline is tight, ruthlessly cut Backlog items that won't improve the demo score

## Step 4 — Update Current Focus
Rewrite the "Current Focus" section to reflect where things stand right now. One or two sentences max. Be specific enough that a fresh Claude session understands the state immediately.

## Step 5 — Add session log entry
Append a row to the Session Log table:
```
| [date + time] | [2-sentence summary: what was built, what's left] |
```

## Step 6 — Confirm
Print the updated "Up Next" list so the user can see what's queued for next session.
