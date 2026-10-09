# Ben's Morning Briefing: daily runbook

Follow this every morning. A run is one dated JSON file (`data/runs/YYYY-MM-DD.json`) in the repo
`benweru/morning-briefing`. `publish_run.py` turns it into the live site:

- Latest briefing: https://benweru.github.io/morning-briefing/
- Archive: https://benweru.github.io/morning-briefing/archive/
- One run: https://benweru.github.io/morning-briefing/archive/YYYY-MM-DD/

All times are EAT (Africa/Nairobi, UTC+3). The box clock is already on EAT.

**The one rule: never invent anything.** Every posting, salary, location rule, date and story must
come from a page you opened today. If a detail isn't shown, write `Not shown` (salary) or leave the
field empty (dropped roles only). If you can't confirm a posting is live, it doesn't go on the shortlist.

---

## 0. Where things are

| What | Path |
|---|---|
| Local clone (remote `origin` = github.com/benweru/morning-briefing, branch `main`) | `/workspace/briefing-site` |
| Run data (one file per day) | `/workspace/briefing-site/data/runs/YYYY-MM-DD.json` |
| JSON Schema | `/workspace/briefing-site/data/run.schema.json` |
| Build scripts (working copy) | `/workspace/build/` (`briefing_lib.py`, `verify_run.py`, `publish_run.py`, this file) |
| Build scripts (versioned copy, synced on every publish) | `/workspace/briefing-site/build/` |
| Python with Playwright + jsonschema | `/workspace/.pwvenv/bin/python` (uses system Chrome `/usr/bin/google-chrome`) |
| Kenya jobs from the local search (written by Local Search Bot, read-only for this run) | `/workspace/shared/local-jobs/latest.json` (see section 3a) |

If the box was reset:

```bash
git clone https://github.com/benweru/morning-briefing.git /workspace/briefing-site
mkdir -p /workspace/build && cp /workspace/briefing-site/build/* /workspace/build/
python3 -m venv /workspace/.pwvenv && /workspace/.pwvenv/bin/pip install playwright jsonschema
```

Then use system Chrome as is, or run `/workspace/.pwvenv/bin/playwright install chromium` and change
`CHROME` in `verify_run.py`.

Before starting, run `git -C /workspace/briefing-site pull --ff-only` so the clone is current.

---

## 1. Who the search is for

**Ben Maina**, Nairobi, Kenya (UTC+3).

- **Education and role:** CS graduate (Strathmore). AI Prototyping & Automation Engineer at Kwara
  (fintech) since March 2026, so about 1 year of professional experience. Earlier data-ops work at Chumz.
- **CV focus:**
  - Python APIs and backend
  - LLM integrations, AI agents and automation (MCP, agent frameworks, n8n-style workflows, webhooks)
  - React/TypeScript
  - PostgreSQL
  - fintech integrations
- **Targets:** junior to mid-level software, backend, full-stack, AI or automation engineering, and
  forward-deployed or solutions engineering roles.

Use the same tone as the existing pages in the `fit` and `gaps` notes: plain, specific, one or two
sentences each.
- **`fit`** says what matches his CV.
- **`gaps`** says what's missing or risky, such as a stack he doesn't have, more years than he has,
  a time-zone overlap, a contract instead of salary, or an always-open listing.

## 2. Job search (about 60–90 min)

### 2.1 Sources (check all; record each one you used in `sources.jobs`)

| Source | How |
|---|---|
| Remotive | `https://remotive.com/api/remote-jobs?category=software-dev` (and `?search=python`, `?search=ai`) |
| RemoteOK | `https://remoteok.com/api` (first element is a legal notice; send a User-Agent) |
| Himalayas | `https://himalayas.app/jobs/api?limit=100&offset=N` and `https://himalayas.app/jobs/api/search?country=KE&q=python` (also `q=ai`, `q=react`, `q=automation`). himalayas.app *pages* return 403 to curl/WebFetch (Cloudflare), so confirm every Himalayas lead on the employer's own page or ATS. |
| Jobicy | `https://jobicy.com/api/v2/remote-jobs?count=50&tag=python` (also `tag=react`, `industry=dev`) |
| We Work Remotely | RSS: `https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss`, `.../remote-full-stack-programming-jobs.rss`, `.../remote-programming-jobs.rss` |
| Working Nomads | `https://www.workingnomads.com/api/exposed_jobs/` |
| Employer ATS boards | Greenhouse `https://boards-api.greenhouse.io/v1/boards/<company>/jobs?content=true` (EU boards: `job-boards.eu.greenhouse.io`), Lever `https://api.lever.co/v0/postings/<company>?mode=json`, Recruitee `https://<company>.recruitee.com/api/offers/`, Ashby `https://api.ashbyhq.com/posting-api/job-board/<company>`. Recheck employers that hire remotely worldwide (e.g. Canonical) and anything carried over from yesterday. |
| Web search | Junior/graduate remote roles that are worldwide, EMEA or Africa-friendly, for example "junior AI automation engineer remote worldwide", "graduate software engineer remote EMEA", and roles on DOU.ua, OpenTrain or Jobgether. Use the current year in queries. |

**Count** roughly how many postings you pulled in total (`counts.pulled`) and how many each bulk
filter removed (`counts.filtered_out`). Mark the counts approximate if they are.

### 2.2 Bulk filters (apply in this order)

1. **Posted in the last 30 days.** Use the source's date, or the ATS `updated_at`/`first_published`.
   An always-open listing that keeps being reposted can stay only in the **evergreen** tier, and its
   `posted` field must say what the date really is, e.g.
   `Himalayas listed 2026-09-19 (Greenhouse req first published 2023-10-11, updated 2026-08-05)`.
2. **Junior to mid-level only.**
   - Drop titles with Senior, Staff, Principal, Lead, Manager, Head or Director.
   - Drop roles that ask for 5+ years.
   - Roles asking for 3–4 years go to **stretch** at most, with the gap stated.
3. **Target role:** software, backend, full-stack, AI or LLM, automation, integrations, or
   forward-deployed engineering. Drop sales, design, pure data science, QA-only, PHP/WordPress-only,
   blockchain-only and similar.
4. **Kenya eligibility (strict)**, judged from the posting text. Quote it in `location_as_stated`.
   - **Eligible:**
     - "Worldwide", "Anywhere", "Remote (global)" with no country restriction;
     - an explicit country list that includes Kenya;
     - "EMEA" or "Africa";
     - a time-zone range that includes UTC+3 with no country restriction.
   - **Not eligible:**
     - US/Canada/UK/EU/LATAM/APAC-only;
     - "must be authorised to work in…" a country Ben isn't in;
     - a country list without Kenya;
     - a time-zone range that excludes UTC+3;
     - a required on-site or hybrid office.
   - **Unclear** (e.g. "Remote, abroad" with no list): it may stay on the shortlist only if
     everything else fits, and `gaps` must say "Kenya isn't named; confirm before applying".
     Otherwise drop it with reason code `location`.
   - Lead sites' location tags (Himalayas, Remotive) are hints only. The employer's page decides.

### 2.3 Close review and live check (for each remaining candidate)

- **Open the posting itself** (employer careers page or ATS), not just the aggregator. Confirm all
  of the following:
  - it is still open (no 404, no "no longer accepting", and `validThrough` not in the past);
  - the location rule;
  - the experience asked;
  - the salary as shown;
  - the posted date.
- **Record** in `verified` where and when you checked, e.g. `Greenhouse API, live 2026-10-08`.
  Record in `found_via` where the lead came from.
- **When a site blocks bots** (403 to curl/WebFetch, e.g. DOU.ua, Himalayas), use the box browser.
  A 403 is not proof that the page is gone.
- **Use the exact posting URL** in `url`; it is the job's identity. `publish_run.py` derives a stable
  `id` from the normalised URL (https, lower-case host without `www.`, no fragment or trailing slash,
  no `utm_*`/`ref`/`source`/`gh_src`/`lever-*` parameters, remaining parameters sorted). Use the same
  URL form every day so a role isn't wrongly marked **New**. Prefer the ATS URL
  (e.g. `https://job-boards.greenhouse.io/<co>/jobs/<id>`).
- **Yesterday's shortlist:** re-verify every role on it. If a role is still live and still fits,
  keep it with the same URL. If it closed or no longer fits, add it to `dropped` with the reason
  (e.g. `closed`). The page will then list it under "No longer listed since <date>" with that reason.
- **Shortlist 6–10 roles** and rank them 1..N by fit. Assign tiers:
  - `top`: junior-friendly, clearly open to Kenya, close to his current work.
  - `evergreen`: always-open or reposted listings.
  - `stretch`: open to Kenya, but asks for skills or years he doesn't have yet.
- **Every closely reviewed role that didn't make the shortlist** goes into `dropped`, with a specific
  `reason` (e.g. `EU-only; 3-5 yrs`) and one `reason_code`:
  - `location`: Kenya not eligible, or not confirmed
  - `experience`: too senior, or too many years
  - `stale`: more than 30 days old
  - `closed`: removed or closed
  - `stack`: stack mismatch
  - `requirement`: another hard requirement, e.g. a language
  - `other`

## 3. News (about 20–30 min)

Gather **8–12 stories published in the last 48 hours** (before `checked_at`), each verified on the
publisher's page, in these four groups (`news.groups[].id`):

| id | Group | Look for |
|---|---|---|
| `ai` | AI and LLMs | Model releases (especially open weights), agent tooling, developer platforms. Official blogs/press releases first. |
| `startups` | Startups and funding | Funding rounds and launches, especially African/Kenyan startups and agentic-AI companies likely to hire. TechCabal, TechCrunch, Disrupt Africa, The Condia, Techpoint Africa. |
| `hiring` | Hiring market | Junior/remote hiring trends, layoffs, AI-skills demand. Reputable outlets (AP, Reuters, Bloomberg, Rest of World). |
| `kenya` | Kenya fintech | M-PESA/Safaricom, CBK rules, Kenyan fintech launches. Safaricom newsroom, Techweez, Business Daily, TechCabal. |

Aim for 2–4 stories per group. If a group has nothing good in 48 hours, leave the group out rather
than padding it.

For each story:
- `title`: a short factual headline in your own words.
- `summary`: one line of facts from the article. Copy numbers exactly.
- `why`: one line on why it matters for Ben.
- `source`: the publisher.
- `date`: the publication date, as YYYY-MM-DD.
- `url`: the canonical article URL.

Never use a story you only saw in a search snippet; open it first.
List the publishers in `sources.news`.

## 3a. Kenya jobs (no searching needed here)

The page has a **Kenya jobs** section ("Part two", between the remote jobs and the news). This run
does not search for it. Local Search Bot checks MyJobMag and LinkedIn for Nairobi roles each weekday
at about 6:58 AM EAT and writes `/workspace/shared/local-jobs/latest.json` (directory mode 777, so
any agent can write it):

```jsonc
{
  "date": "2026-10-09",                          // YYYY-MM-DD; must equal today in EAT
  "generated_at": "2026-10-09T06:58:00+03:00",
  "sources_checked": ["myjobmag", "linkedin"],
  "errors": [{"source": "linkedin", "message": "..."}],   // strings are accepted too
  "jobs": [{"title": "...", "company": "...", "location": "...", "source": "myjobmag",
            "url": "https://...", "posted": "...", "fit_note": "..."}]   // any field may be missing
}
```

Rules (enforced in `briefing_lib.read_local_jobs` / `attach_local_jobs`):
- `publish_run.py` reads the file only when the run is dated today, and uses its jobs only when its
  `date` is today in EAT. If the file is missing, unreadable, stale or marked `"example": true`, the
  section shows one line: "The local search didn't run today, so there are no Kenya jobs in this
  briefing." Old jobs are never shown.
- The result is snapshotted into the run file as `local_jobs` (`status: "ok"` with the jobs, or
  `status: "not_run"` with a `reason`), so archive pages stay permanent. Runs without
  `local_jobs` (the 2026-10-07 and 2026-10-08 runs as published) show no Kenya section.
- Each job links to its own `url` (non-http URLs are dropped and shown as "no link given"); company,
  location, source (MyJobMag / LinkedIn), posted and fit note appear only when present. Each entry
  in `errors` becomes a small note naming the failed source. Nothing is added or rewritten.
- **Never edit `latest.json` and never add Kenya jobs to the run file by hand.** If the section says
  the search didn't run, that's the correct output; mention it to Ben instead.

## 4. Write the run file

Save the file as `/workspace/briefing-site/data/runs/YYYY-MM-DD.json`, using today's date in EAT.
The formal schema is in `data/run.schema.json`. The easiest start is to copy yesterday's file and
replace every value. Summary of the fields:

```jsonc
{
  "schema_version": 1,
  "run_date": "2026-10-08",                       // must match the file name
  "checked_at": "2026-10-08T07:45:00+03:00",      // when postings were verified, EAT with offset
  "sources": {
    "jobs": ["Remotive API", "Himalayas API (including searches filtered to Kenya)", "..."],
    "news": ["TechCabal", "Safaricom", "..."]
  },
  "counts": {
    "pulled": 1000, "pulled_is_approximate": true,
    "filtered_out": {"older_than_30_days": 150, "senior_title": 250, "not_target_role": 400, "location_or_timezone": null},
    "filtered_out_is_approximate": true
    // shortlisted, dropped, reviewed_closely, dropped_by_reason, stories: filled in by publish_run.py
  },
  "method": {"filtering_summary": "Of about 1,000 postings pulled, about 150 were more than 30 days old, ..."},
  "jobs": [{
    "rank": 1, "tier": "top",                      // top | evergreen | stretch
    "url": "https://job-boards.greenhouse.io/canonical/jobs/8249005",
    "title": "...", "company": "...",
    "location_as_stated": "Home based - Worldwide",  // quoted from the posting
    "posted": "2026-10-05", "salary_as_shown": "Not shown", "experience_asked": "...",
    "found_via": "Greenhouse API", "verified": "Greenhouse API, live 2026-10-08",
    "fit": "One or two sentences.", "gaps": "One or two sentences.",
    "note": "optional research note, not rendered"
    // "id" is derived from url by publish_run.py
  }],
  "dropped": [{
    "url": "...", "title": "...", "company": "...", "location_as_stated": "...",
    "reason": "EU-only; 3-5 yrs", "reason_code": "location",   // location|experience|stale|closed|stack|requirement|other
    "posted": "", "salary_as_shown": "", "experience_asked": "", "found_via": "", "verified": "", "note": ""
  }],
  "news": {"groups": [
    {"id": "ai", "stories": [
      {"title": "...", "summary": "...", "why": "...", "source": "Mistral blog", "date": "2026-10-07", "url": "https://..."}
    ]}
  ]}
}
```

Quick self-check before publishing:
- Every URL was opened today.
- Kenya eligibility is quoted.
- Nothing older than 30 days is outside the evergreen tier.
- Ranks run 1..N.
- 6–10 jobs and 8–12 stories.

## 5. Publish

```bash
cd /workspace/briefing-site && git pull --ff-only
/workspace/.pwvenv/bin/python /workspace/build/publish_run.py 2026-10-08
```

The command is unchanged: the Kenya jobs file is picked up automatically. Optional flags:
`--local-jobs PATH` (another file, for tests) and `--allow-example` (render a file marked
`"example": true`; only allowed together with `--no-push`).

Or do a dry run first, which builds and verifies but doesn't commit:

```bash
/workspace/.pwvenv/bin/python /workspace/build/publish_run.py 2026-10-08 --no-push --shots /tmp/briefing-shots
```

`publish_run.py` then:

1. **Validates** the run against the rules in `briefing_lib.validate_run` and
   `data/run.schema.json`. It fills in ids and derived counts and writes them back into the file.
   For a run dated today it also snapshots the Kenya jobs file into `local_jobs` (section 3a).
2. **Diffs** against the newest earlier run by job id. Shortlisted roles that weren't on the previous
   shortlist get a **New** label. Roles on the previous shortlist that are missing now appear in
   "No longer listed since <date>", with this run's drop reason if there is one. The first ever run
   shows "First briefing, no earlier run to compare."
3. **Renders** three pages:
   - `index.html`: always the newest run;
   - `archive/YYYY-MM-DD/index.html`: the run's permanent page;
   - `archive/index.html`: all runs, newest first, with Shortlisted, New, No longer listed and
     Stories counts.

   Older archive pages are not touched. Use `--rebuild-all` only after a deliberate design change.
4. **Verifies** in headless Chrome, serving the repo at `/morning-briefing/` as GitHub Pages does:
   - HTTP 200 for every page;
   - counts match the JSON;
   - every job, dropped and story URL is linked, and external links open in a new tab;
   - New labels and the no-longer-listed list match the diff;
   - filters, search, the empty state and Clear work;
   - "Past briefings" links work from the nav and footer, and archive rows and links resolve;
   - the Kenya jobs section matches `local_jobs` (job count, links, error notes), or shows only the
     "didn't run today" line; runs without `local_jobs` have no Kenya section;
   - colour tokens are exactly v3 plus the three Kenya tokens (`--band-local #f0f2e8`,
     `--sec-local #4d5a22`, `--rule-local #d9ddc8`) and all text pairs pass WCAG AA (lowest is 5.68:1);
   - only the v3 type sizes (14/16/18/22/30/44px) are used;
   - no console errors, no external requests, no overflow at 390px.

   Any failure stops the run before anything is committed.
5. **Copies** the build scripts and this runbook into the repo's `build/` folder.
6. **Commits** as `Ben Waweru Maina <138494503+benweru@users.noreply.github.com>` and pushes to
   `origin main`. Auth comes from `GH_TOKEN`, falling back to `$GITHUB_TOKEN`, via `gh auth setup-git`.
   Output is masked, so the token is never printed; never echo it yourself either. If `origin/main`
   has commits the clone doesn't, it stops instead of force-pushing: run `git pull --rebase`, then
   re-run.
7. **Waits** until the live index, the archive page and the archive index match the local files
   byte for byte, then reports the latest Pages build commit. This usually takes under a minute;
   it times out at 15 minutes.
8. **Prints the morning message** (also on `--no-push`) and saves it to
   `/tmp/morning-briefing-summary-YYYY-MM-DD.txt`: the remote shortlist count with new/no longer
   listed, the story count, a "Kenya jobs:" line (how many Nairobi roles and from which sources,
   any source that failed, or "the local search didn't run today"), and the live link.

## 6. After publishing

Open the live URLs in the box browser and glance at:
- the New labels;
- the no-longer-listed note;
- the archive row.

Then report to Ben, starting from the printed morning message:
- the shortlist, with what's new;
- what dropped off, and why;
- the Kenya jobs count (or that the local search didn't run today), exactly as the message says;
- the live link.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `X.json is not valid` | Fix the listed fields; the messages name the job or story. |
| `already exists with different content` | You passed a file from outside the repo and a different one is already in `data/runs/`. Check which is right; `--force` replaces it. |
| Verification failure about colour tokens or type sizes | Someone changed the CSS in `briefing_lib.py`. Revert, or update `V3_COLOURS`/`TEXT_PAIRS` in `verify_run.py` deliberately, with new contrast checks. |
| Every role shows **New** | The URLs differ from yesterday's (different host or path form). Use the same canonical posting URL. |
| Pages wait times out | Check `gh api repos/benweru/morning-briefing/pages/builds/latest` (with `GH_TOKEN` exported) and the repo's Actions/Pages settings, then re-run the script; it skips the commit if nothing changed. |
| Kenya section says the local search didn't run | Check the `[publish] Kenya jobs:` line for the reason (missing, stale date, unreadable, example). Don't edit the file; tell Ben, and Local Search Bot if it's missing or stale. If the file appears later the same morning, re-running `publish_run.py` for today refreshes the snapshot. |
| Run for a past date | Works. `index.html` keeps showing the newest run; only that day's archive page and the archive index change. |
