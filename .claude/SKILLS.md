# Project Skills Quick Reference

Quick lookup for all custom skills defined in `.claude/commands/`. Use `/skillname` to invoke.

| Skill | Purpose | When to use | Key action |
|-------|---------|------------|-----------|
| **session-context** | Load full project context at session start | Session startup | Read CLAUDE.md, hackathon_strategy.md, run smoke test |
| **plan** | Load ACTIVE_PLAN.md + P3_PLAN.md, reconcile with reality, execute next task | Daily workflow | Pick next task, execute, update both plans |
| **run** | Start Streamlit app | Need to launch app | `streamlit run app.py` (conda-wrapped) |
| **check** | Smoke test data files + app imports | After download_data.py | Verify all 8 data files, Claude API key |
| **hackathon** | Full Challenge B competitive context (inject for full picture) | Need full challenge background | Review criteria, demo script, biology, build timeline |
| **demo** | Pre-demo checklist (run ~18:30 before presentations) | Before presenting | App running, data loaded, regions picked, Claude button tested |
| **wrap-up** | End-of-session audit + plan update | Session end or pause | Audit work, capture blockers, revise plan, log session |

## Typical Session Flow

1. `/session-context` — Load project rules + data schema
2. `/plan` — Pick next task, execute
3. `/wrap-up` — Before stopping

## Files Updated

- `ACTIVE_PLAN.md` — Session-level execution plan
- `P3_PLAN.md` — P3 project-level plan (synced with ACTIVE_PLAN.md)
- `CLAUDE.md` — Module map + data rules

## Notes

- Both `/plan` and `/wrap-up` now track `ACTIVE_PLAN.md` AND `P3_PLAN.md` to keep them in sync
- `/hackathon` is reference-only (no tools); use when you need the full competitive picture
- `/demo` is checklist-only (no tools); use to verify before presenting
