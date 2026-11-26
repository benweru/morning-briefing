# Job Search Plus: runbook

Recreated 2026-11-13 after the box restore of 2026-11-12 (~14:04 EAT) lost the original. Updated 2026-11-26.

Profile: Ben Maina, Full Stack & AI Engineer at Kwara (fintech), March–September 2026 (never an
internship). Targets software/backend/full-stack/AI/automation, forward-deployed, and sales/solution
consulting roles.

## Setup (after any box reset)

```bash
cd /workspace/job-search-plus
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
```

`.venv/`, `out/` and `state/seen.json` are not tracked anywhere, so they must be recreated.

## Daily remote search (morning briefing)

```bash
./.venv/bin/python live/remote_live.py YYYY-MM-DD
```

Writes `out/remote-live-YYYY-MM-DD.json` (per-source ok/pulled/fresh/kept counts, `kept` roles,
filter counts, `loc_status` per role: kenya/worldwide/africa/unconfirmed). Wellfound is never fetched
automatically; it needs the signed-in browser pass. ReliefWeb is retired (bot check; API needs an
approved appname). Requests retry with backoff; failed sources are re-run once.
Test without touching state: `REMOTE_LIVE_DRY=1 REMOTE_LIVE_OUT=/tmp/x.json ./.venv/bin/python live/remote_live.py YYYY-MM-DD`.
The briefing itself is built and published from `/workspace/build/` (see `/workspace/build/RUNBOOK.md`,
also in github.com/benweru/morning-briefing under `build/`).

## On-demand report

```bash
./.venv/bin/python render.py            # all collectors -> out/latest.{json,md}, dashboard.html
./.venv/bin/python report.py --out sample-report.md
```

`render.py` updates `state/seen.json`, `state/last_report.json` and `state/careers_watch.json`.
Back up `state/` first if you are only testing.

## State

- `state/applied_log.csv`: every application, one layout only: `date,title,company,url,status`
  (normalised 2026-11-26; write rows with a CSV writer so commas are quoted; `url` may be a
  `mailto:` or empty, never guessed). Check by company and URL/job id before applying or shortlisting.
- `state/reviewed_jobs.txt`: URLs already shown in a briefing; `publish_run.py` appends to it after each push.
