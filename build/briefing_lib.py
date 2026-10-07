"""Ben's Morning Briefing: run data model, run-to-run diff and HTML rendering.

Design system: v3 (editorial layout, section bands, tier and news-group colours). The CSS
below is the v3 stylesheet copied verbatim, plus a short "Run history" block that only
uses existing tokens. Do not add colours here without adding them to the token layer
and to the contrast checks in verify_run.py.

Pure functions only: no network, no git. publish_run.py drives this module.
"""
import datetime as dt
import hashlib
import html
import json
import os
import re
from urllib.parse import parse_qsl, urlencode, urlsplit

e = html.escape
SCHEMA_VERSION = 1

TIERS = [
    ('top', 'Top fit', 'Junior-friendly, open to Kenya, and close to Ben\u2019s current work.'),
    ('evergreen', 'Evergreen listings', 'Always-open listings that get reposted. The date shown is the latest relisting, not when the role was created.'),
    ('stretch', 'Stretch', 'Open to Kenya, but they ask for skills or experience that aren\u2019t on Ben\u2019s CV yet.'),
]
TIER_IDS = tuple(t[0] for t in TIERS)
TIER_NAME = {'top': 'Top fit', 'evergreen': 'Evergreen', 'stretch': 'Stretch'}
# News groups, in display order. Each id has a colour token (--news-<id>) in the CSS.
NEWS_GROUPS = {'ai': 'AI and LLMs', 'startups': 'Startups and funding', 'hiring': 'Hiring market', 'kenya': 'Kenya fintech'}
# Primary reason a closely reviewed role was dropped (the full reason text is kept too).
DROP_REASONS = {
    'location': 'Kenya not eligible, or eligibility not confirmed',
    'experience': 'Too senior, or asks for more years than Ben has',
    'stale': 'Posted more than 30 days ago',
    'closed': 'Posting closed or removed',
    'stack': 'Stack doesn\u2019t match his CV',
    'requirement': 'Other hard requirement (for example a language)',
    'other': 'Other',
}
CV_FOCUS = 'Python APIs, LLM integrations, React/TypeScript, PostgreSQL'
NEWTAB = '<span class="visually-hidden"> (opens in new tab)</span>'
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# ---------------------------------------------------------------- ids
HOST_ALIASES = {'boards.greenhouse.io': 'job-boards.greenhouse.io'}
TRACKING_PARAM = re.compile(r'^(utm_.*|gh_src|ref|referrer|source|src|lever-source.*|lever-origin|fbclid|gclid|mc_.*)$')


def normalise_url(url):
    """Canonical form of a posting URL: https, lower-case host without www, host aliases
    applied, no fragment, no trailing slash, tracking parameters removed, remaining query
    parameters sorted. Path case is kept (some ATS ids are case-sensitive)."""
    p = urlsplit(url.strip())
    host = (p.hostname or '').lower()
    if host.startswith('www.'):
        host = host[4:]
    host = HOST_ALIASES.get(host, host)
    path = re.sub(r'/+$', '', p.path) or ''
    query = sorted((k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not TRACKING_PARAM.match(k.lower()))
    return f'https://{host}{path}' + (f'?{urlencode(query)}' if query else '')


def job_id(url):
    """Stable job id: 'j-' + first 12 hex chars of sha1(normalised URL)."""
    return 'j-' + hashlib.sha1(normalise_url(url).encode()).hexdigest()[:12]


def story_id(url):
    return 's-' + hashlib.sha1(normalise_url(url).encode()).hexdigest()[:12]

# ---------------------------------------------------------------- dates


def to_date(s):
    return dt.date.fromisoformat(s)


def long_date(d):          # Wednesday, 7 October 2026
    return f'{d:%A}, {d.day} {d:%B} {d.year}'


def day_month(d):          # 7 October
    return f'{d.day} {d:%B}'


def full_date(d):          # 7 October 2026
    return f'{d.day} {d:%B} {d.year}'


def short_date(d):         # 7 Oct 2026
    return f'{d.day} {d:%b} {d.year}'


EAT = dt.timezone(dt.timedelta(hours=3))


def checked_label(iso):    # Oct 7, 2026, 9:30 PM EAT
    t = dt.datetime.fromisoformat(iso).astimezone(EAT)
    hour = t.hour % 12 or 12
    return f'{t:%b} {t.day}, {t.year}, {hour}:{t:%M} {"AM" if t.hour < 12 else "PM"} EAT'


def window_label(dates):   # 2–7 October 2026
    a, b = min(dates), max(dates)
    if a == b:
        return full_date(a)
    if (a.year, a.month) == (b.year, b.month):
        return f'{a.day}\u2013{b.day} {b:%B} {b.year}'
    if a.year == b.year:
        return f'{a.day} {a:%B} \u2013 {b.day} {b:%B} {b.year}'
    return f'{full_date(a)} \u2013 {full_date(b)}'


def join_and(items):
    items = list(items)
    if len(items) <= 1:
        return ''.join(items)
    if len(items) == 2:
        return f'{items[0]} and {items[1]}'
    return ', '.join(items[:-1]) + ', and ' + items[-1]


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'

# ---------------------------------------------------------------- data files


def runs_dir(repo):
    return os.path.join(repo, 'data', 'runs')


def list_run_dates(repo):
    d = runs_dir(repo)
    if not os.path.isdir(d):
        return []
    return sorted(f[:-5] for f in os.listdir(d) if re.match(r'^\d{4}-\d{2}-\d{2}\.json$', f))


def run_path(repo, date):
    return os.path.join(runs_dir(repo), f'{date}.json')


def load_run(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_run(run, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(run, f, indent=2, ensure_ascii=False)
        f.write('\n')


def normalise_run(run):
    """Fill derived fields in place: ids from URLs, rank order, counts that can be computed."""
    for j in run.get('jobs', []) + run.get('dropped', []):
        if isinstance(j.get('url'), str) and j['url']:
            j['id'] = job_id(j['url'])
    run['jobs'] = sorted(run.get('jobs', []), key=lambda j: j.get('rank') if isinstance(j.get('rank'), int) else 10**6)
    for g in run.get('news', {}).get('groups', []):
        g['name'] = NEWS_GROUPS.get(g['id'], g.get('name', g['id']))
        for s in g.get('stories', []):
            if isinstance(s.get('url'), str) and s['url']:
                s['id'] = story_id(s['url'])
    c = run.setdefault('counts', {})
    c['shortlisted'] = len(run['jobs'])
    c['dropped'] = len(run.get('dropped', []))
    c['reviewed_closely'] = c['shortlisted'] + c['dropped']
    by = {}
    for j in run.get('dropped', []):
        by[j.get('reason_code', 'other')] = by.get(j.get('reason_code', 'other'), 0) + 1
    c['dropped_by_reason'] = {k: by[k] for k in DROP_REASONS if k in by}
    c['stories'] = sum(len(g.get('stories', [])) for g in run.get('news', {}).get('groups', []))
    return run


JOB_REQUIRED = ['url', 'title', 'company', 'location_as_stated', 'posted', 'salary_as_shown', 'experience_asked', 'found_via', 'verified']


def validate_run(run, filename_date=None):
    """Return (errors, warnings). Errors block publishing; warnings are printed."""
    E, W = [], []
    need = lambda obj, keys, where: [E.append(f'{where}: missing "{k}"') for k in keys if k not in obj or obj[k] in (None, '') and k not in ('salary_as_shown',)]
    need(run, ['schema_version', 'run_date', 'checked_at', 'sources', 'counts', 'method', 'jobs', 'dropped', 'news'], 'run')
    if E:
        return E, W
    if run['schema_version'] != SCHEMA_VERSION:
        E.append(f'schema_version must be {SCHEMA_VERSION}')
    if not DATE_RE.match(str(run['run_date'])):
        E.append('run_date must be YYYY-MM-DD')
    elif filename_date and run['run_date'] != filename_date:
        E.append(f'run_date {run["run_date"]} does not match file name {filename_date}.json')
    try:
        t = dt.datetime.fromisoformat(run['checked_at'])
        if t.utcoffset() is None:
            E.append('checked_at needs a UTC offset, e.g. 2026-10-08T07:30:00+03:00')
    except (TypeError, ValueError):
        E.append('checked_at must be an ISO 8601 timestamp with offset')
    for k in ('jobs', 'news'):
        if not run['sources'].get(k):
            E.append(f'sources.{k} must list at least one source')
    if not run['method'].get('filtering_summary'):
        E.append('method.filtering_summary is required')
    ids = set()
    if not run['jobs']:
        E.append('jobs: at least one shortlisted job is required')
    for i, j in enumerate(run['jobs']):
        w = f'jobs[{i}] {j.get("title", "?")}'
        need(j, JOB_REQUIRED + ['rank', 'tier', 'fit', 'gaps'], w)
        if j.get('tier') not in TIER_IDS:
            E.append(f'{w}: tier must be one of {TIER_IDS}')
        if not str(j.get('url', '')).startswith(('https://', 'http://')):
            E.append(f'{w}: url must be http(s)')
        if j.get('id') in ids:
            E.append(f'{w}: duplicate job (same normalised URL as another entry)')
        ids.add(j.get('id'))
    ranks = [j.get('rank') for j in run['jobs']]
    if sorted(ranks) != list(range(1, len(ranks) + 1)):
        E.append('jobs: rank must run 1..N with no gaps or repeats')
    for i, j in enumerate(run['dropped']):
        w = f'dropped[{i}] {j.get("title", "?")}'
        need(j, ['url', 'title', 'company', 'location_as_stated', 'reason', 'reason_code'], w)
        if j.get('reason_code') not in DROP_REASONS:
            E.append(f'{w}: reason_code must be one of {tuple(DROP_REASONS)}')
        if j.get('id') in ids:
            E.append(f'{w}: also appears in jobs or earlier in dropped')
        ids.add(j.get('id'))
    groups = run['news'].get('groups', [])
    gids = [g.get('id') for g in groups]
    if any(g not in NEWS_GROUPS for g in gids) or len(set(gids)) != len(gids):
        E.append(f'news.groups: ids must be unique and from {tuple(NEWS_GROUPS)}')
    n = 0
    for g in groups:
        if not g.get('stories'):
            E.append(f'news group {g.get("id")}: empty group (leave it out instead)')
        for k, s in enumerate(g.get('stories', [])):
            n += 1
            w = f'news {g.get("id")}[{k}] {s.get("title", "?")}'
            need(s, ['title', 'summary', 'why', 'source', 'date', 'url'], w)
            if not DATE_RE.match(str(s.get('date', ''))):
                E.append(f'{w}: date must be YYYY-MM-DD')
            elif DATE_RE.match(str(run['run_date'])) and to_date(s['date']) > to_date(run['run_date']):
                E.append(f'{w}: dated after the run')
    if n == 0:
        E.append('news: at least one story is required')
    if not 6 <= len(run['jobs']) <= 10:
        W.append(f'{len(run["jobs"])} shortlisted jobs (runbook target is 6-10)')
    if not 8 <= n <= 12:
        W.append(f'{n} stories (runbook target is 8-12)')
    return E, W

# ---------------------------------------------------------------- diff


def previous_date(dates, date):
    earlier = [d for d in dates if d < date]
    return max(earlier) if earlier else None


def diff_runs(run, prev):
    """Compare a run's shortlist with the previous run's shortlist by job id."""
    if prev is None:
        return {'prev_date': None, 'new_ids': set(), 'gone': []}
    prev_ids = {j['id'] for j in prev['jobs']}
    cur_ids = {j['id'] for j in run['jobs']}
    dropped_now = {j['id']: j for j in run['dropped']}
    gone = [{'job': j, 'dropped_now': dropped_now.get(j['id'])} for j in prev['jobs'] if j['id'] not in cur_ids]
    return {'prev_date': prev['run_date'], 'new_ids': cur_ids - prev_ids, 'gone': gone}

# ---------------------------------------------------------------- rendering

CSS = r'''
/* ---------- Tokens ---------- */
:root {
  /* Type: two families, six sizes */
  --font-serif: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", "URW Palladio L", Georgia, serif;
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --fs-sm: 0.875rem;  /* 14px meta */
  --fs-base: 1rem;    /* 16px body */
  --fs-md: 1.125rem;  /* 18px item titles */
  --fs-lg: 1.375rem;  /* 22px group headings */
  --fs-xl: 1.875rem;  /* 30px section headings */
  --fs-xxl: clamp(2.25rem, 1.6rem + 2.6vw, 2.75rem); /* 36-44px masthead */
  --lh-tight: 1.2;
  --lh-body: 1.55;

  /* Space: 4px base */
  --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px;
  --s-5: 24px; --s-6: 32px; --s-7: 48px; --s-8: 64px;

  /* Color: warm neutrals + one accent */
  --paper: #fbfaf7;
  --surface: #ffffff;
  --ink: #1b1a17;
  --ink-muted: #57544d;
  --rule: #e2ded5;          /* decorative hairlines */
  --rule-strong: #85817a;   /* control borders, >= 3:1 on paper */
  --rule-jobs: #e3d9c8;     /* hairlines on the warm jobs band */
  --rule-news: #d3dbe2;     /* hairlines on the cool news band */
  --rule-appendix: #d6d3cb; /* hairlines on the appendix band */
  --accent: #1f4e8c;        /* links + primary actions */
  --accent-strong: #163a69; /* hover / pressed */
  --accent-wash: #eef2f8;   /* hover fill on light controls */

  /* Wayfinding colour. Every hue below has one job; all text uses pass AA (>= 4.5:1)
     on every band they appear on. Values are muted (low chroma, ~L35) so they read as
     ink, not decoration. */
  /* Section bands: full-bleed background tints that tell you which part you're in. */
  --band-jobs: #f7f1e6;      /* Jobs section: light warm tint */
  --band-news: #edf2f6;      /* Today in tech: light cool tint */
  --band-appendix: #ecebe6;  /* Dropped roles appendix: quiet neutral */
  /* Section identity: opening rule, eyebrow label, active nav indicator. */
  --sec-jobs: #7a4520;       /* warm umber, pairs with --band-jobs */
  --sec-news: #1f5470;       /* cool deep blue-teal, pairs with --band-news */
  /* Job tiers: heading rule, row marker, filter swatch. */
  --tier-top: #2e6a3e;       /* muted green = strongest match */
  --tier-evergreen: #4a5870; /* slate = always-open, neutral */
  --tier-stretch: #82560e;   /* ochre = reach, proceed with care */
  /* Fit / gaps lead-ins on each role. */
  --fit: var(--tier-top);    /* green = matches his CV (same meaning as Top fit) */
  --gap: #9a3d22;            /* rust = missing skill or requirement */
  /* News groups: one hue per topic, same lightness and low chroma so they harmonise. */
  --news-ai: #3f4c88;        /* indigo: AI and LLMs */
  --news-startups: #1d6561;  /* teal: startups and funding */
  --news-hiring: #6c4570;    /* plum: hiring market */
  --news-kenya: #8a4a2c;     /* terracotta: Kenya fintech */

  --radius: 2px;
  --measure: 68ch;
  --page: 1120px;
  --nav-h: 48px;
}

/* ---------- Base ---------- */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 400 var(--fs-base)/var(--lh-body) var(--font-sans);
  font-kerning: normal;
}
h1, h2, h3, h4 { font-family: var(--font-serif); line-height: var(--lh-tight); margin: 0; font-weight: 700; }
p, ol, ul, dl, dd { margin: 0; }
ol[role="list"], ul[role="list"] { list-style: none; padding: 0; }
a { color: var(--accent); text-underline-offset: 0.15em; text-decoration-thickness: 1px; }
a:hover { color: var(--accent-strong); text-decoration-thickness: 2px; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.visually-hidden {
  position: absolute !important; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.quiet { color: var(--ink-muted); }
.wrap { max-width: var(--page); margin-inline: auto; padding-inline: var(--s-5); }

.skip-link {
  position: absolute; left: var(--s-4); top: calc(-1 * var(--s-8));
  background: var(--ink); color: var(--paper); padding: var(--s-2) var(--s-4); z-index: 20;
}
.skip-link:focus { top: var(--s-2); color: var(--paper); }

/* ---------- Masthead ---------- */
.masthead { padding-block: var(--s-7) var(--s-5); border-bottom: 2px solid var(--ink); }
.masthead .dateline { font-size: var(--fs-sm); font-weight: 600; color: var(--ink-muted); margin-bottom: var(--s-2); }
.masthead h1 { font-size: var(--fs-xxl); letter-spacing: -0.01em; }
.masthead .dek { font-family: var(--font-serif); font-size: var(--fs-lg); line-height: 1.35; margin-top: var(--s-2); }
.masthead .facts { margin-top: var(--s-4); font-size: var(--fs-sm); color: var(--ink-muted); }

/* ---------- Section nav ---------- */
.section-nav {
  position: sticky; top: 0; z-index: 10;
  background: var(--paper); border-bottom: 1px solid var(--rule);
}
.section-nav[data-current="jobs"] { background: var(--band-jobs); }
.section-nav[data-current="news"] { background: var(--band-news); }
.section-nav ul { display: flex; gap: var(--s-5); height: var(--nav-h); }
.section-nav a {
  display: flex; align-items: center; height: 100%;
  color: var(--ink-muted); font-weight: 600; text-decoration: none;
  border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.section-nav a:hover { color: var(--ink); }
.section-nav a { --sec: var(--accent); }
.section-nav a[data-section="jobs"] { --sec: var(--sec-jobs); }
.section-nav a[data-section="news"] { --sec: var(--sec-news); }
.section-nav a[aria-current="true"] { color: var(--sec); border-bottom: 3px solid var(--sec); margin-bottom: -1px; }
.section-nav .n { font-weight: 400; margin-left: var(--s-2); color: var(--ink-muted); }

/* ---------- Sections ---------- */
.section { padding-block: var(--s-7) var(--s-6); scroll-margin-top: var(--nav-h); border-top: 4px solid var(--sec); }
.section-jobs { --sec: var(--sec-jobs); background: var(--band-jobs); padding-bottom: 0; }
.section-news { --sec: var(--sec-news); background: var(--band-news); }
.section-head .eyebrow { font-size: var(--fs-sm); font-weight: 600; color: var(--sec); margin-bottom: var(--s-2); }
.section-head { max-width: var(--measure); margin-bottom: var(--s-5); }
.section-head h2 { color: var(--ink); }
.section-head h2 { font-size: var(--fs-xl); letter-spacing: -0.005em; }
.section-head p { margin-top: var(--s-2); color: var(--ink-muted); }

/* ---------- Controls ---------- */
.section-jobs .controls { border-color: var(--rule-jobs); }
.controls {
  display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between;
  gap: var(--s-4); padding-block: var(--s-4); border-block: 1px solid var(--rule);
}
.filter-group { border: 0; margin: 0; padding: 0; min-width: 0; }
.filter-group legend, .search label { display: block; font-size: var(--fs-sm); font-weight: 600; color: var(--ink-muted); margin-bottom: var(--s-2); padding: 0; }
.segmented { display: flex; flex-wrap: wrap; }
.segmented button {
  font: 600 var(--fs-sm)/1 var(--font-sans);
  min-height: 40px; padding: 0 var(--s-4);
  color: var(--ink); background: var(--surface);
  border: 1px solid var(--rule-strong); border-radius: 0; margin-left: -1px; cursor: pointer;
}
.segmented button:first-child { margin-left: 0; border-radius: var(--radius) 0 0 var(--radius); }
.segmented button:last-child { border-radius: 0 var(--radius) var(--radius) 0; }
.segmented button:hover { background: var(--accent-wash); }
.segmented button:active { background: var(--rule); }
.segmented button[aria-pressed="true"] { background: var(--ink); color: var(--paper); border-color: var(--ink); position: relative; }
.segmented button:focus-visible { position: relative; z-index: 1; }
.segmented .n { font-weight: 400; margin-left: var(--s-1); }
.swatch { display: inline-block; width: 10px; height: 10px; margin-right: var(--s-2); background: var(--tier); flex: none; }
.segmented button { display: inline-flex; align-items: center; }
.segmented button[aria-pressed="true"] .swatch { box-shadow: 0 0 0 1px var(--paper); }
[data-filter="top"], .tier-top, .job[data-tier="top"] { --tier: var(--tier-top); }
[data-filter="evergreen"], .tier-evergreen, .job[data-tier="evergreen"] { --tier: var(--tier-evergreen); }
[data-filter="stretch"], .tier-stretch, .job[data-tier="stretch"] { --tier: var(--tier-stretch); }
.search { flex: 0 1 320px; }
.search input {
  width: 100%; min-height: 40px; padding: 0 var(--s-3);
  font: 400 var(--fs-base)/1 var(--font-sans); color: var(--ink);
  background: var(--surface); border: 1px solid var(--rule-strong); border-radius: var(--radius);
}
.search input::placeholder { color: var(--ink-muted); opacity: 1; }
.search input:focus-visible { outline-offset: 0; border-color: var(--accent); }
.result-status { font-size: var(--fs-sm); color: var(--ink-muted); padding-top: var(--s-4); }

/* ---------- Job tiers & rows ---------- */
.tier { margin-top: var(--s-6); }
.tier-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--s-1) var(--s-4); padding: var(--s-2) 0 var(--s-3) var(--s-3); border-left: 6px solid var(--tier); border-bottom: 2px solid var(--tier); }
.tier-head h3 { font-size: var(--fs-lg); color: var(--tier); }
.tier-head .count { font-family: var(--font-sans); font-size: var(--fs-base); font-weight: 400; color: var(--ink-muted); margin-left: var(--s-1); }
.tier-head p { font-size: var(--fs-sm); color: var(--ink-muted); }
.section-jobs .job { border-bottom-color: var(--rule-jobs); }
.job {
  display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(0, 1fr) 176px;
  gap: var(--s-6); padding-block: var(--s-5); border-bottom: 1px solid var(--rule);
}
.job-title { font-size: var(--fs-md); }
.tier-tag { display: flex; align-items: center; font-size: var(--fs-sm); font-weight: 600; color: var(--tier); margin-bottom: var(--s-2); }
.job-company { font-weight: 600; color: var(--ink-muted); margin-top: var(--s-1); margin-bottom: var(--s-3); }
.job-note + .job-note { margin-top: var(--s-2); }
.job-note strong { font-weight: 700; }
.note-fit strong { color: var(--fit); }
.note-gap strong { color: var(--gap); }
.note-fit, .note-gap { padding-left: var(--s-3); border-left: 2px solid var(--note); }
.note-fit { --note: var(--fit); }
.note-gap { --note: var(--gap); }
.job-facts { display: grid; gap: var(--s-2); font-size: var(--fs-sm); align-content: start; }
.job-facts div { display: grid; grid-template-columns: 88px minmax(0, 1fr); gap: var(--s-3); }
.job-facts dt { font-weight: 600; color: var(--ink-muted); }
.job-action { display: flex; flex-direction: column; gap: var(--s-3); align-items: stretch; }
.button {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 40px; padding: 0 var(--s-4);
  font-weight: 600; font-size: var(--fs-sm); text-decoration: none;
  color: var(--surface); background: var(--accent); border: 1px solid var(--accent); border-radius: var(--radius);
}
.button:hover { color: var(--surface); background: var(--accent-strong); border-color: var(--accent-strong); text-decoration: none; }
.button:active { background: var(--ink); border-color: var(--ink); }
.job-source { font-size: var(--fs-sm); color: var(--ink-muted); }

.empty { padding-block: var(--s-5) 0; }
.empty p + p { margin-top: var(--s-2); }
.link-button {
  font: inherit; color: var(--accent); background: none; border: 0; padding: 0;
  text-decoration: underline; text-underline-offset: 0.15em; cursor: pointer;
}
.link-button:hover { color: var(--accent-strong); text-decoration-thickness: 2px; }

/* ---------- Dropped roles ---------- */
.appendix { background: var(--band-appendix); border-top: 1px solid var(--rule-strong); margin-top: var(--s-7); padding-block: var(--s-2) var(--s-5); }
.dropped { scroll-margin-top: var(--nav-h); }
.dropped summary {
  display: grid; grid-template-columns: 1ch auto minmax(0, 1fr); align-items: baseline; gap: var(--s-1) var(--s-3); padding-block: var(--s-4);
  cursor: pointer; list-style: none;
}
.dropped summary::-webkit-details-marker { display: none; }
.dropped summary::before { content: "+"; font-family: var(--font-sans); font-weight: 600; width: 1ch; color: var(--ink-muted); }
.dropped[open] summary::before { content: "\2212"; }
.dropped summary h3 { font-size: var(--fs-lg); display: inline; }
.dropped summary span { font-size: var(--fs-sm); color: var(--ink-muted); }
.dropped table { width: 100%; border-collapse: collapse; font-size: var(--fs-sm); }
.dropped th, .dropped td { text-align: left; vertical-align: top; padding: var(--s-3) var(--s-4) var(--s-3) 0; border-top: 1px solid var(--rule-appendix); }
.dropped thead th { font-weight: 600; color: var(--ink-muted); border-top: 0; padding-top: 0; }
.dropped tbody th { font-weight: 600; }
.dropped td:last-child, .dropped th:last-child { padding-right: 0; }

/* ---------- News ---------- */
.news-group { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: var(--s-6); padding-block: var(--s-5); border-top: 3px solid var(--group); }
.news-group h3 { font-size: var(--fs-lg); color: var(--group); }
.ng-ai { --group: var(--news-ai); }
.ng-startups { --group: var(--news-startups); }
.ng-hiring { --group: var(--news-hiring); }
.ng-kenya { --group: var(--news-kenya); }
.stories { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 var(--s-6); }
.story { padding-bottom: var(--s-5); max-width: var(--measure); }
.story:nth-child(n+3) { padding-top: var(--s-5); border-top: 1px solid var(--rule-news); }
.story-title { font-size: var(--fs-md); margin-bottom: var(--s-2); }
.story-title a { color: var(--ink); text-decoration: none; }
.story-title a:hover { color: var(--accent); text-decoration: underline; }
.story p + p { margin-top: var(--s-2); }
.story-meta { font-size: var(--fs-sm); color: var(--ink-muted); }

/* ---------- Footer ---------- */
.site-footer { border-top: 2px solid var(--ink); background: var(--paper); padding-block: var(--s-6) var(--s-7); font-size: var(--fs-sm); color: var(--ink-muted); }
.site-footer h2 { font-size: var(--fs-lg); color: var(--ink); margin-bottom: var(--s-3); }
.site-footer dl { display: grid; grid-template-columns: 140px minmax(0, 1fr); gap: var(--s-2) var(--s-5); max-width: 880px; }
.site-footer dt { font-weight: 600; color: var(--ink); }

/* ---------- Responsive ---------- */
@media (max-width: 960px) {
  .job { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
  .job-main { grid-column: 1 / -1; }
  .news-group { grid-template-columns: 1fr; gap: var(--s-4); }
}
@media (max-width: 640px) {
  .wrap { padding-inline: var(--s-4); }
  .masthead { padding-block: var(--s-6) var(--s-4); }
  .section { padding-block: var(--s-6) var(--s-5); }
  .controls { flex-direction: column; align-items: stretch; }
  .search { flex-basis: auto; }
  .segmented button { flex: 1 1 auto; padding: 0 var(--s-3); }
  .job { grid-template-columns: 1fr; gap: var(--s-4); }
  .stories { grid-template-columns: 1fr; }
  .story:nth-child(n+2) { padding-top: var(--s-5); border-top: 1px solid var(--rule-news); }
  .dropped thead { display: none; }
  .dropped tr { display: block; padding-block: var(--s-3); border-top: 1px solid var(--rule-appendix); }
  .dropped th, .dropped td { display: block; border: 0; padding: 0; }
  .dropped td { color: var(--ink-muted); }
  .dropped td[data-label="Reason"] { color: var(--ink); margin-top: var(--s-1); }
  .site-footer dl { grid-template-columns: 1fr; gap: var(--s-1); }
  .dropped summary span { grid-column: 2 / -1; }
  .site-footer dd + dt { margin-top: var(--s-3); }
}
@media print {
  .section-nav, .controls, .skip-link { display: none; }
  .job, .story { break-inside: avoid; }
}
/* ---------- Run history (existing tokens only) ---------- */
.section-nav .nav-aside { margin-left: auto; }
.section-nav .nav-aside a { font-size: var(--fs-sm); font-weight: 400; }
.section-nav .nav-aside a:hover { text-decoration: underline; }
.section-nav a[aria-current="page"] { color: var(--ink); border-bottom: 3px solid var(--ink); }
.masthead .facts + .facts { margin-top: var(--s-1); }
.new-tag {
  margin-left: var(--s-2); padding: 0 var(--s-1);
  font-size: var(--fs-sm); font-weight: 600; line-height: var(--lh-body);
  color: var(--accent); border: 1px solid var(--accent); border-radius: var(--radius);
}
.gone { margin-top: var(--s-6); padding-top: var(--s-4); border-top: 1px solid var(--rule-jobs); scroll-margin-top: var(--nav-h); }
.gone h3 { font-size: var(--fs-md); }
.gone > p { margin-top: var(--s-1); font-size: var(--fs-sm); color: var(--ink-muted); }
.gone ul { display: grid; gap: var(--s-2); margin-top: var(--s-3); font-size: var(--fs-sm); }
.gone li .quiet { display: block; }
.section-archive { --sec: var(--ink); background: var(--paper); border-top: 0; }
.runs { width: 100%; border-collapse: collapse; }
.runs th, .runs td { text-align: left; vertical-align: baseline; padding: var(--s-3) var(--s-4) var(--s-3) 0; border-top: 1px solid var(--rule); }
.runs thead th { font-size: var(--fs-sm); font-weight: 600; color: var(--ink-muted); border-top: 0; padding-top: 0; }
.runs .num { text-align: right; font-variant-numeric: tabular-nums; }
.runs td:last-child, .runs th:last-child { padding-right: 0; text-align: right; }
.runs tbody tr:last-child > * { border-bottom: 1px solid var(--rule); }
.runs tbody th { font-family: var(--font-serif); font-size: var(--fs-md); font-weight: 700; }
.runs .latest { margin-left: var(--s-2); font-family: var(--font-sans); font-size: var(--fs-sm); font-weight: 400; color: var(--ink-muted); }
.runs .data-link { font-size: var(--fs-sm); }
@media (max-width: 640px) {
  .runs thead { display: none; }
  .runs tr { display: flex; flex-wrap: wrap; gap: var(--s-1) var(--s-4); padding-block: var(--s-3); border-top: 1px solid var(--rule); }
  .runs tbody tr:last-child { border-bottom: 1px solid var(--rule); }
  .runs th, .runs td, .runs tbody tr:last-child > * { display: block; border: 0; padding: 0; text-align: left; }
  .runs tbody th, .runs td:last-child { flex: 0 0 100%; text-align: left; }
  .runs td.num { font-size: var(--fs-sm); white-space: nowrap; }
  .runs td.num::before { content: attr(data-label) " "; color: var(--ink-muted); }
}
'''

JS = r'''
(function () {
  var jobs = [].slice.call(document.querySelectorAll('.job'));
  var groups = [].slice.call(document.querySelectorAll('.tier'));
  var buttons = [].slice.call(document.querySelectorAll('.segmented button'));
  var input = document.getElementById('job-search');
  var status = document.getElementById('result-status');
  var empty = document.getElementById('empty');
  var emptyText = document.getElementById('empty-text');
  var labels = { all: '', top: 'Top fit', evergreen: 'Evergreen', stretch: 'Stretch' };
  var filter = 'all';

  function apply() {
    var term = input.value.trim().toLowerCase();
    var shown = 0;
    jobs.forEach(function (job) {
      var match = (filter === 'all' || job.dataset.tier === filter) &&
                  (!term || job.dataset.search.indexOf(term) !== -1);
      job.hidden = !match;
      if (match) shown++;
    });
    groups.forEach(function (g) {
      g.hidden = !g.querySelector('.job:not([hidden])');
    });
    var scope = filter === 'all' ? '' : ' in ' + labels[filter];
    var query = term ? ' matching \u201c' + input.value.trim() + '\u201d' : '';
    status.textContent = shown === jobs.length ? 'All ' + jobs.length + ' roles'
      : shown + ' of ' + jobs.length + ' roles' + scope + query;
    empty.hidden = shown !== 0;
    if (shown === 0) emptyText.textContent = term
      ? 'Nothing matches that search' + scope + '. Try a broader term, such as a language or company name.'
      : 'No roles in this group.';
  }

  function setFilter(value) {
    filter = value;
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.filter === value)); });
    apply();
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { setFilter(b.dataset.filter); });
  });
  input.addEventListener('input', apply);
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && input.value) { input.value = ''; apply(); }
  });
  document.getElementById('clear-filters').addEventListener('click', function () {
    input.value = '';
    setFilter('all');
    input.focus();
  });

  // Section nav: mark the section currently in view.
  var navLinks = [].slice.call(document.querySelectorAll('.section-nav a'));
  var news = document.getElementById('news');
  function markCurrent() {
    var atEnd = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    var current = (news.getBoundingClientRect().top <= window.innerHeight * 0.4 || atEnd) ? 'news' : 'jobs';
    document.querySelector('.section-nav').setAttribute('data-current', current);
    navLinks.forEach(function (a) {
      if (a.dataset.section === current) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }
  window.addEventListener('scroll', markCurrent, { passive: true });
  window.addEventListener('hashchange', markCurrent);
  markCurrent();
  apply();
})();
'''


def _head(title, description):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<link rel="icon" href="data:,">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<style>{CSS}</style>
</head>
<body>'''


def _job_row(j, new_ids, prev_date):
    sal = (j.get('salary_as_shown') or '').strip()
    sal_html = e(sal) if sal and sal.lower() != 'not shown' else '<span class="quiet">Not shown</span>'
    search = ' '.join([j['title'], j['company'], j['location_as_stated'], j['experience_asked'], j['fit'], j['gaps']]).lower()
    new = ''
    if j['id'] in new_ids:
        new = f'<span class="new-tag">New<span class="visually-hidden"> since the {day_month(to_date(prev_date))} briefing</span></span>'
    return f'''
        <li class="job" data-tier="{j['tier']}" data-id="{j['id']}" data-search="{e(search)}">
          <div class="job-main">
            <p class="tier-tag"><span class="swatch" aria-hidden="true"></span>{TIER_NAME[j['tier']]}{new}</p>
            <h4 class="job-title">{e(j['title'])}</h4>
            <p class="job-company">{e(j['company'])}</p>
            <p class="job-note note-fit"><strong>Fit.</strong> {e(j['fit'])}</p>
            <p class="job-note note-gap"><strong>Gaps.</strong> {e(j['gaps'])}</p>
          </div>
          <dl class="job-facts">
            <div><dt>Location</dt><dd>{e(j['location_as_stated'])}</dd></div>
            <div><dt>Posted</dt><dd>{e(j['posted'])}</dd></div>
            <div><dt>Salary</dt><dd>{sal_html}</dd></div>
            <div><dt>Experience</dt><dd>{e(j['experience_asked'])}</dd></div>
          </dl>
          <div class="job-action">
            <a class="button" href="{e(j['url'])}" target="_blank" rel="noopener noreferrer">View posting{NEWTAB}</a>
            <p class="job-source">Found via {e(j['found_via'])}. Verified: {e(j['verified'])}.</p>
          </div>
        </li>'''


def _gone_html(d):
    if not d['prev_date'] or not d['gone']:
        return ''
    pd = day_month(to_date(d['prev_date']))
    lis = []
    for g in d['gone']:
        j, now = g['job'], g['dropped_now']
        status = f'Dropped this run: {e(now["reason"])}.' if now else 'Not found in this run\u2019s search.'
        lis.append(f'''
          <li><a href="{e(j['url'])}" target="_blank" rel="noopener noreferrer">{e(j['title'])}{NEWTAB}</a>, {e(j['company'])}.
            <span class="quiet">Was {TIER_NAME[j['tier']]} on {pd}. {status}</span></li>''')
    return f'''
      <section class="gone" id="gone" aria-labelledby="gone-heading">
        <h3 id="gone-heading">No longer listed since {pd}</h3>
        <p>On the {pd} shortlist, but not on this one.</p>
        <ul role="list">{''.join(lis)}
        </ul>
      </section>'''


def _diff_line(d):
    if not d['prev_date']:
        return 'First briefing, no earlier run to compare.'
    pd = day_month(to_date(d['prev_date']))
    n_new, n_gone = len(d['new_ids']), len(d['gone'])
    gone = f'<a href="#gone">{n_gone} no longer listed</a>' if n_gone else '0 no longer listed'
    return f'Compared with the {pd} briefing: {n_new} new, {gone}.'


def render_run_page(run, prev, root, archived):
    """One briefing page. root is the relative path to the site root ('' for index.html,
    '../../' for archive/YYYY-MM-DD/index.html)."""
    d = diff_runs(run, prev)
    date = to_date(run['run_date'])
    checked = checked_label(run['checked_at'])
    jobs, dropped = run['jobs'], run['dropped']
    groups = run['news']['groups']
    n_news = sum(len(g['stories']) for g in groups)
    story_dates = [to_date(s['date']) for g in groups for s in g['stories']]
    archive_href = f'{root}archive/'
    latest_href = root or './'
    data_href = f'{root}data/runs/{run["run_date"]}.json'
    counts = {t: sum(1 for j in jobs if j['tier'] == t) for t in TIER_IDS}

    tiers_html = []
    for tid, tname, tdesc in TIERS:
        items = [j for j in jobs if j['tier'] == tid]
        if not items:
            continue
        tiers_html.append(f'''
      <section class="tier tier-{tid}" data-group="{tid}" aria-labelledby="tier-{tid}">
        <header class="tier-head">
          <h3 id="tier-{tid}">{tname} <span class="count">{len(items)}</span></h3>
          <p>{tdesc}</p>
        </header>
        <ol class="jobs" role="list">{''.join(_job_row(j, d['new_ids'], d['prev_date']) for j in items)}
        </ol>
      </section>''')

    drop_rows = ''.join(f'''
            <tr>
              <th scope="row"><a href="{e(j['url'])}" target="_blank" rel="noopener noreferrer">{e(j['title'])}{NEWTAB}</a></th>
              <td data-label="Company">{e(j['company'])}</td>
              <td data-label="Location as stated">{e(j['location_as_stated'])}</td>
              <td data-label="Reason">{e(j['reason'])}</td>
            </tr>''' for j in dropped)

    order = list(NEWS_GROUPS)
    news_html = []
    for g in sorted(groups, key=lambda g: order.index(g['id'])):
        lis = ''.join(f'''
            <li class="story">
              <h4 class="story-title"><a href="{e(s['url'])}" target="_blank" rel="noopener noreferrer">{e(s['title'])}{NEWTAB}</a></h4>
              <p>{e(s['summary'])}</p>
              <p><strong>Why it matters:</strong> {e(s['why'])}</p>
              <p class="story-meta">{e(s['source'])}, {short_date(to_date(s['date']))}</p>
            </li>''' for s in g['stories'])
        news_html.append(f'''
      <section class="news-group ng-{g['id']}" aria-labelledby="news-{g['id']}">
        <h3 id="news-{g['id']}">{e(NEWS_GROUPS[g['id']])}</h3>
        <ol class="stories" role="list">{lis}
        </ol>
      </section>''')

    filter_buttons = ''.join(
        f'''
            <button type="button" data-filter="{tid}" aria-pressed="false"><span class="swatch" aria-hidden="true"></span>{TIER_NAME[tid]}<span class="n">{counts[tid]}</span></button>'''
        for tid in TIER_IDS)
    archived_note = ''
    if archived:
        archived_note = f'''
    <p class="facts">Permanent copy of the {full_date(date)} briefing. <a href="{latest_href}">Latest briefing</a> \u00b7 <a href="{archive_href}">Past briefings</a></p>'''

    return _head(f'Ben\u2019s Morning Briefing \u2014 {full_date(date)}',
                 'Remote roles open to Kenya, matched to Ben Maina\u2019s CV, and the day\u2019s tech news.') + f'''
<a class="skip-link" href="#jobs">Skip to jobs</a>

<header class="masthead">
  <div class="wrap">
    <p class="dateline">{long_date(date)}</p>
    <h1>Ben\u2019s Morning Briefing</h1>
    <p class="dek">Remote roles open to Kenya, and today in tech.</p>
    <p class="facts">{len(jobs)} shortlisted roles, {len(dropped)} reviewed and dropped, {n_news} stories. Jobs checked {checked}.</p>{archived_note}
  </div>
</header>

<nav class="section-nav" aria-label="Sections" data-current="jobs">
  <div class="wrap">
    <ul role="list">
      <li><a href="#jobs" data-section="jobs" aria-current="true">Jobs<span class="n">{len(jobs)}</span></a></li>
      <li><a href="#news" data-section="news">Today in tech<span class="n">{n_news}</span></a></li>
      <li class="nav-aside"><a href="{archive_href}" class="archive-link">Past briefings</a></li>
    </ul>
  </div>
</nav>

<main>
  <section id="jobs" class="section section-jobs" aria-labelledby="jobs-heading" tabindex="-1">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow">Part one: Jobs</p>
        <h2 id="jobs-heading">Remote roles open to Kenya</h2>
        <p>Matched to Ben Maina\u2019s CV: {CV_FOCUS}. Each posting was checked on the employer\u2019s careers page or the board that hosts it on {checked}. Location rules and salaries are quoted as the source showed them.</p>
        <p class="run-diff">{_diff_line(d)}</p>
      </header>

      <div class="controls">
        <fieldset class="filter-group">
          <legend>Show</legend>
          <div class="segmented">
            <button type="button" data-filter="all" aria-pressed="true">All<span class="n">{len(jobs)}</span></button>{filter_buttons}
          </div>
        </fieldset>
        <div class="search">
          <label for="job-search">Search roles</label>
          <input id="job-search" type="search" placeholder="Title, company or skill" autocomplete="off" aria-describedby="result-status">
        </div>
      </div>
      <p class="result-status" id="result-status" role="status" aria-live="polite">All {len(jobs)} roles</p>

      {''.join(tiers_html)}

      <div class="empty" id="empty" hidden>
        <p id="empty-text">No roles match.</p>
        <p><button type="button" class="link-button" id="clear-filters">Clear search and filters</button></p>
      </div>
{_gone_html(d)}
    </div>
    <div class="appendix">
      <div class="wrap">
      <details class="dropped">
        <summary><h3>Appendix: dropped roles</h3> <span>{len(dropped)} reviewed closely, with the reason each was rejected</span></summary>
        <table>
          <thead>
            <tr><th scope="col">Role</th><th scope="col">Company</th><th scope="col">Location as stated</th><th scope="col">Reason</th></tr>
          </thead>
          <tbody>{drop_rows}
          </tbody>
        </table>
      </details>
      </div>
    </div>
  </section>

  <section id="news" class="section section-news" aria-labelledby="news-heading" tabindex="-1">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow">Part two: News</p>
        <h2 id="news-heading">Today in tech</h2>
        <p>{n_news} stories from {window_label(story_dates)}, each with a note on why it matters for Ben.</p>
      </header>
      {''.join(news_html)}
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <h2>Sources and method</h2>
    <dl>
      <dt>Job sources</dt>
      <dd>{e(join_and(run['sources']['jobs']))}.</dd>
      <dt>Filtering</dt>
      <dd>{e(run['method']['filtering_summary'])}</dd>
      <dt>News sources</dt>
      <dd>{e(join_and(run['sources']['news']))}.</dd>
      <dt>Past briefings</dt>
      <dd><a href="{archive_href}" class="archive-link">Every run, newest first</a>. This run\u2019s data: <a href="{data_href}">{run['run_date']}.json</a>.</dd>
    </dl>
  </div>
</footer>

<script>{JS}</script>
</body>
</html>
'''


def archive_rows(repo):
    """Summary of every run, newest first: date, counts and diff against the run before."""
    dates = list_run_dates(repo)
    runs = {d: normalise_run(load_run(run_path(repo, d))) for d in dates}
    rows = []
    for d in dates:
        prev = runs.get(previous_date(dates, d))
        df = diff_runs(runs[d], prev)
        rows.append({'date': d, 'shortlisted': len(runs[d]['jobs']), 'stories': runs[d]['counts']['stories'],
                     'new': len(df['new_ids']) if prev else None, 'gone': len(df['gone']) if prev else None})
    return list(reversed(rows))


def render_archive(rows):
    """archive/index.html. All links are relative to /archive/."""
    latest = rows[0]['date']
    first = rows[-1]['date']
    trs = []
    for i, r in enumerate(rows):
        d = to_date(r['date'])
        tag = '<span class="latest">Latest</span>' if i == 0 else ''
        no_prev = '\u2013<span class="visually-hidden"> (first run, nothing to compare)</span>'
        new = no_prev if r['new'] is None else str(r['new'])
        gone = no_prev if r['gone'] is None else str(r['gone'])
        trs.append(f'''
            <tr>
              <th scope="row"><a class="run-link" href="{r['date']}/">{long_date(d)}</a>{tag}</th>
              <td class="num" data-label="Shortlisted">{r['shortlisted']}</td>
              <td class="num" data-label="New">{new}</td>
              <td class="num" data-label="No longer listed">{gone}</td>
              <td class="num" data-label="Stories">{r['stories']}</td>
              <td><a class="data-link" href="../data/runs/{r['date']}.json">Data<span class="visually-hidden"> for {full_date(d)} (JSON)</span></a></td>
            </tr>''')
    return _head('Past briefings \u2014 Ben\u2019s Morning Briefing',
                 'Every run of Ben\u2019s Morning Briefing, newest first.') + f'''
<a class="skip-link" href="#runs">Skip to the list of runs</a>

<header class="masthead">
  <div class="wrap">
    <p class="dateline">Ben\u2019s Morning Briefing</p>
    <h1>Past briefings</h1>
    <p class="dek">Every run, newest first. Each one keeps its own permanent page.</p>
    <p class="facts">{plural(len(rows), 'briefing')} since {full_date(to_date(first))}. Latest: {long_date(to_date(latest))}.</p>
  </div>
</header>

<nav class="section-nav" aria-label="Sections">
  <div class="wrap">
    <ul role="list">
      <li><a href="../">Latest briefing</a></li>
      <li><a href="./" aria-current="page">Past briefings<span class="n">{len(rows)}</span></a></li>
    </ul>
  </div>
</nav>

<main>
  <section id="runs" class="section section-archive" aria-labelledby="runs-heading" tabindex="-1">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow">Archive</p>
        <h2 id="runs-heading">All runs</h2>
        <p>New and No longer listed compare each run\u2019s shortlist with the run before it. The first run has nothing to compare with.</p>
      </header>
      <table class="runs">
        <thead>
          <tr><th scope="col">Date</th><th scope="col" class="num">Shortlisted</th><th scope="col" class="num">New</th><th scope="col" class="num">No longer listed</th><th scope="col" class="num">Stories</th><th scope="col"><span class="visually-hidden">Data file</span></th></tr>
        </thead>
        <tbody>{''.join(trs)}
        </tbody>
      </table>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <h2>About the archive</h2>
    <dl>
      <dt>Data</dt>
      <dd>Each run is stored as one JSON file in <a href="https://github.com/benweru/morning-briefing/tree/main/data/runs" target="_blank" rel="noopener noreferrer">data/runs/ on GitHub{NEWTAB}</a>, named by date; the Data link on each row opens that run\u2019s file. Pages are generated from those files.</dd>
      <dt>Comparing runs</dt>
      <dd>Every job has a stable id taken from its normalised posting URL, so a role counts as new only if its posting wasn\u2019t on the previous shortlist.</dd>
    </dl>
  </div>
</footer>
</body>
</html>
'''
