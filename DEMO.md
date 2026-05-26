# Explainable Brains — 2-Minute Demo Script

## 0:00 — Setup (presenter says before clicking)
"Vibraint shared a real c-Fos study: Semaglutide — Ozempic — versus Vehicle, in mice. 12 animals, 459 brain regions. The data is here. The question is: what does Ozempic do to the brain, and can we see it in 2 minutes?"

## 0:15 — Volcano (Page 1)
Click Page 1. Point at the colored points.
"Each dot is a brain region. Right side: higher activity on Semaglutide. Left: higher on Vehicle. Color = uncorrected significance."
Click "Auto-summarize" → Claude streams a 4-sentence summary live.

## 0:45 — Ranking → Deep dive (Page 2 → Page 3)
Click Page 2. Click NTS row.
"NTS — nucleus of the solitary tract — brainstem satiety hub. We expect to see this. There it is, lit up."
Page 3 opens with NTS pre-selected. Show brain slice + violin.

## 1:15 — The surprising finding
Go back to Page 2. Click MD (Mediodorsal nucleus of thalamus).
"This one we did NOT expect. The mediodorsal thalamus is a key relay between prefrontal cortex and limbic circuits — its activation suggests Semaglutide is reshaping cognitive control and decision-making, not just hunger signalling."
Click "Explain this region" → Claude streams 3 sentences.

## 1:50 — Close
"Volcano, ranking, brain slice, Claude narration. Drop in any Vibraint study CSV — same app, new biology, ten seconds."

## Backup plan
- API stalls → cached responses in `demo_cache/<acronym>.txt`. Read with `Path("demo_cache/NTS.txt").read_text()`.
- Streamlit dies → screenshots in `demo_cache/screenshots/`
