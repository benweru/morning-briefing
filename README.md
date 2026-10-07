# Ben's Morning Briefing

Remote roles open to Kenya, matched to Ben Maina's CV, plus the day's tech news. One run per morning.

- Latest: https://benweru.github.io/morning-briefing/
- Past briefings: https://benweru.github.io/morning-briefing/archive/

## Layout

```
index.html                     latest run (generated)
archive/index.html             all runs, newest first (generated)
archive/YYYY-MM-DD/index.html  permanent page per run (generated)
data/runs/YYYY-MM-DD.json      one structured file per run (source of truth)
data/run.schema.json           JSON Schema for run files
build/briefing_lib.py          data model, run-to-run diff, HTML rendering (v3 design system)
build/verify_run.py            headless-Chrome checks
build/publish_run.py           validate -> render -> verify -> commit -> push -> wait for Pages
build/RUNBOOK.md               how to do a daily run end to end
build/backfill_2026_10_07.py   one-off conversion of the first run
```

## Publish a run

```bash
/workspace/.pwvenv/bin/python /workspace/build/publish_run.py YYYY-MM-DD   # add --no-push for a dry run
```

See `build/RUNBOOK.md`.
