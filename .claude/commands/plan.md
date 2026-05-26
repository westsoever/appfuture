---
name: plan
description: Load the active plan, reconcile with current reality, and continue executing
allowed_tools: ["Read", "Bash", "Write", "Edit"]
---

## Step 1 — Load context
Read `ACTIVE_PLAN.md` and `P3_PLAN.md` in full. Read `CLAUDE.md` for module map.

## Step 2 — Reconcile with reality
Check what actually exists and what's working:
```bash
ls -la *.py data/ 2>/dev/null
python smoke_test.py 2>/dev/null || echo "smoke test not yet runnable"
```

Cross-reference the results against the Tasks list in both `ACTIVE_PLAN.md` and `P3_PLAN.md`:
- If something in "Up Next" is already done → move it to "Done" in the file
- If something new is broken or blocked → add it to "Blockers"
- If the build timeline has shifted → update "Current Focus"
- Sync status between both plans if the same task appears in both

## Step 3 — Revise the plan
Before executing anything, improve the plan:
- Are the "Up Next" tasks still the right next steps?
- Is the ordering still optimal given the current state?
- Are there any tasks that should be split or merged?
- Update `ACTIVE_PLAN.md` and `P3_PLAN.md` with any changes.
- Ensure consistency between both plans (no conflicting priorities)

## Step 4 — Pick the next task
Take the first unchecked item in "Up Next". Add it to "In Progress" in both `ACTIVE_PLAN.md` and `P3_PLAN.md`. Say out loud which task you're starting.

## Step 5 — Execute
Work on the task. As you make progress:
- If a task spawns sub-tasks, add them to "Up Next" immediately
- If you hit a blocker requiring manual input, add it to "Blockers & Manual Input Needed" and move to the next task
- When a task is fully done, move it from "In Progress" to "Done" in both `ACTIVE_PLAN.md` and `P3_PLAN.md`

## Step 6 — After each task completes
Update both `ACTIVE_PLAN.md` and `P3_PLAN.md` before moving to the next task. Then loop back to Step 4.

## Stopping
If asked to stop or pause: run `/wrap-up` before ending the session.
