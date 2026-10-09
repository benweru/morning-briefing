#!/usr/bin/env python3
"""Publish one run of Ben's Morning Briefing to GitHub Pages (benweru/morning-briefing).

Usage (from anywhere):
    /workspace/.pwvenv/bin/python /workspace/build/publish_run.py 2026-10-08
    /workspace/.pwvenv/bin/python /workspace/build/publish_run.py /path/to/2026-10-08.json

    --no-push       build and verify only; do not commit, push or wait
    --rebuild-all   also regenerate every older archive page (only after a deliberate design change)
    --shots DIR     save 1280px and 390px screenshots of the three pages into DIR
    --message MSG   commit message (default: "Briefing run YYYY-MM-DD: N roles, M stories")
    --repo PATH     local clone (default /workspace/briefing-site)
    --local-jobs PATH   Kenya jobs file from the local search (default /workspace/shared/local-jobs/latest.json)
    --allow-example     render a local-jobs file marked "example": true (local tests only; never with a push)

What it does, in order (stops at the first failure, nothing is pushed unless all checks pass):
  1. Takes the run JSON (written by the morning search step to data/runs/YYYY-MM-DD.json; a
     file elsewhere is copied there). Fills derived fields (job ids from normalised posting
     URLs, story ids, counts) and validates it against the schema rules in briefing_lib.
     If the run is dated today (EAT), it also snapshots the Kenya jobs file into run["local_jobs"]:
     the jobs only when the file's "date" is today, otherwise a not-run record (page shows one line).
  2. Renders index.html (latest run), archive/YYYY-MM-DD/index.html and archive/index.html.
     Older archive pages are left untouched, so they stay permanent.
  3. Verifies with headless Chrome (verify_run.py): HTTP 200 under /morning-briefing/, counts,
     links, New / No longer listed diff, filters and search, AA contrast with the v3 tokens,
     type scale, no console errors, no external requests, no overflow at 390px.
  4. Copies the build scripts and RUNBOOK.md into the repo's build/ folder so they're versioned.
  5. Commits as Ben Waweru Maina <138494503+benweru@users.noreply.github.com> and pushes to
     origin main. Auth: GH_TOKEN (falls back to $GITHUB_TOKEN) via `gh auth setup-git`.
     The token is never printed; all git/gh output is masked.
  6. Waits until https://benweru.github.io/morning-briefing/ serves the new index, archive
     page and archive index byte-for-byte, and the latest Pages build is this commit.
  7. Prints the plain-text morning message (remote roles, Kenya jobs count, link) and saves it to
     /tmp/morning-briefing-summary-YYYY-MM-DD.txt (also on --no-push).
"""
import argparse, json, os, re, shutil, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import briefing_lib as bl  # noqa: E402

AUTHOR_NAME = 'Ben Waweru Maina'
AUTHOR_EMAIL = '138494503+benweru@users.noreply.github.com'
GH_REPO = 'benweru/morning-briefing'
LIVE = 'https://benweru.github.io/morning-briefing/'
BUILD_FILES = ['briefing_lib.py', 'verify_run.py', 'publish_run.py', 'backfill_2026_10_07.py', 'RUNBOOK.md']


def say(msg):
    print(f'[publish] {msg}', flush=True)


def default_repo():
    parent = os.path.dirname(HERE)       # running from the repo's own build/ folder?
    return parent if os.path.isdir(os.path.join(parent, 'data', 'runs')) else '/workspace/briefing-site'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def resolve_run(arg, repo, force):
    """Return the run date, making sure data/runs/<date>.json exists in the repo."""
    if re.match(r'^\d{4}-\d{2}-\d{2}$', arg):
        date, src = arg, bl.run_path(repo, arg)
    else:
        src = os.path.abspath(arg)
        date = os.path.basename(src)[:-5]
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date) or not src.endswith('.json'):
            sys.exit('run file must be named YYYY-MM-DD.json')
    dest = bl.run_path(repo, date)
    if not os.path.exists(src):
        sys.exit(f'no run file at {src}')
    if os.path.abspath(src) != os.path.abspath(dest):
        if os.path.exists(dest) and open(src, 'rb').read() != open(dest, 'rb').read() and not force:
            sys.exit(f'{dest} already exists with different content; pass --force to replace it')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(src, dest)
    return date


def schema_errors(repo, run):
    """Also check data/run.schema.json when the jsonschema package is installed."""
    try:
        import jsonschema
    except ImportError:
        return []
    schema = json.load(open(os.path.join(repo, 'data', 'run.schema.json'), encoding='utf-8'))
    v = jsonschema.Draft202012Validator(schema)
    return [f'schema: {"/".join(map(str, e.absolute_path))}: {e.message}' for e in v.iter_errors(run)]


def build(repo, date, rebuild_all, local_jobs=bl.LOCAL_JOBS_PATH, allow_example=False):
    dates = bl.list_run_dates(repo)
    runs = {}
    for d in dates:
        r = bl.load_run(bl.run_path(repo, d))
        if d == date:
            say(bl.attach_local_jobs(r, local_jobs, bl.today_eat(), allow_example))
        r = bl.normalise_run(r)
        errs, warns = bl.validate_run(r, d)
        errs += schema_errors(repo, r)
        if errs:
            sys.exit(f'{d}.json is not valid:\n  ' + '\n  '.join(errs))
        if d == date:
            for w in warns:
                say(f'warning: {w}')
            bl.write_run(r, bl.run_path(repo, d))   # store derived ids/counts
        runs[d] = r
    prev = lambda d: runs.get(bl.previous_date(dates, d))
    latest = dates[-1]
    if date != latest:
        say(f'note: {date} is not the newest run ({latest}); index.html keeps showing {latest}')
    write(os.path.join(repo, 'index.html'), bl.render_run_page(runs[latest], prev(latest), '', archived=False))
    for d in (dates if rebuild_all else sorted({date, latest})):
        write(os.path.join(repo, 'archive', d, 'index.html'), bl.render_run_page(runs[d], prev(d), '../../', archived=True))
    write(os.path.join(repo, 'archive', 'index.html'), bl.render_archive(bl.archive_rows(repo)))
    r = runs[date]
    d = bl.diff_runs(r, prev(date))
    say(f'built {date}: {len(r["jobs"])} roles ({len(d["new_ids"])} new, {len(d["gone"])} no longer listed), '
        f'{len(r["dropped"])} dropped, {r["counts"]["stories"]} stories; previous run: {d["prev_date"] or "none"}')
    return r


def sync_build_scripts(repo):
    dest = os.path.join(repo, 'build')
    if os.path.abspath(dest) == HERE:
        return
    os.makedirs(dest, exist_ok=True)
    for f in BUILD_FILES:
        if os.path.exists(os.path.join(HERE, f)):
            shutil.copyfile(os.path.join(HERE, f), os.path.join(dest, f))


def git_env():
    env = dict(os.environ)
    token = env.get('GH_TOKEN') or env.get('GITHUB_TOKEN')
    if not token:
        sys.exit('GH_TOKEN / GITHUB_TOKEN is not set; cannot push')
    env['GH_TOKEN'] = token
    env['GIT_TERMINAL_PROMPT'] = '0'
    return env, token


def run(cmd, repo, env=None, token=None, check=True):
    p = subprocess.run(cmd, cwd=repo, env=env, capture_output=True, text=True)
    out = (p.stdout + p.stderr)
    if token:
        out = out.replace(token, '***')
    out = re.sub(r'(gh[pousr]_|github_pat_)[A-Za-z0-9_]+', '***', out)
    if check and p.returncode != 0:
        sys.exit(f'command failed ({" ".join(cmd[:3])}...):\n{out}')
    return p.returncode, out.strip()


def commit_and_push(repo, message):
    env, token = git_env()
    run(['gh', 'auth', 'setup-git'], repo, env, token)
    run(['git', 'fetch', '-q', 'origin', 'main'], repo, env, token)
    _, behind = run(['git', 'rev-list', '--count', 'HEAD..origin/main'], repo, env, token)
    if behind != '0':
        sys.exit('origin/main has commits that are not in the local clone. Run `git pull --rebase` in the repo, '
                 'then re-run this script. (Nothing was pushed.)')
    run(['git', 'add', '-A', 'index.html', 'archive', 'data', 'build', 'README.md', '.nojekyll', '.gitignore'], repo, env, token)
    code, _ = run(['git', 'diff', '--cached', '--quiet'], repo, env, token, check=False)
    if code == 0:
        say('nothing changed since the last commit; skipping commit')
    else:
        run(['git', '-c', f'user.name={AUTHOR_NAME}', '-c', f'user.email={AUTHOR_EMAIL}', 'commit', '-q', '-m', message], repo, env, token)
    _, sha = run(['git', 'rev-parse', 'HEAD'], repo)
    _, out = run(['git', 'push', 'origin', 'HEAD:main'], repo, env, token)
    say(f'pushed {sha[:7]}: {out.splitlines()[-1] if out else "up to date"}')
    return sha, env, token


def wait_live(repo, date, sha, env, token, timeout=900):
    pages = {'': 'index.html', f'archive/{date}/': f'archive/{date}/index.html', 'archive/': 'archive/index.html'}
    local = {k: open(os.path.join(repo, v), 'rb').read() for k, v in pages.items()}
    t0, done = time.time(), set()
    while time.time() - t0 < timeout:
        for rel in pages:
            if rel in done:
                continue
            try:
                req = urllib.request.Request(f'{LIVE}{rel}?nocache={int(time.time() * 1000)}', headers={'Cache-Control': 'no-cache'})
                with urllib.request.urlopen(req, timeout=20) as r:
                    if r.status == 200 and r.read() == local[rel]:
                        done.add(rel)
                        say(f'live: {LIVE}{rel} (200, matches local)')
            except Exception:  # noqa: BLE001  (404 until Pages has built)
                pass
        if len(done) == len(pages):
            break
        time.sleep(10)
    else:
        sys.exit(f'timed out after {timeout}s waiting for Pages; still stale: {sorted(set(pages) - done)}')
    _, out = run(['gh', 'api', f'repos/{GH_REPO}/pages/builds/latest', '--jq', '.status + " " + .commit'], repo, env, token, check=False)
    say(f'Pages build: {out}' + (' (this commit)' if sha in out else ' (note: latest build reports a different commit)'))


def print_summary(repo, date):
    dates = bl.list_run_dates(repo)
    r = bl.normalise_run(bl.load_run(bl.run_path(repo, date)))
    p = bl.previous_date(dates, date)
    prev = bl.normalise_run(bl.load_run(bl.run_path(repo, p))) if p else None
    text = bl.chat_summary(r, prev, f'{LIVE}archive/{date}/' if date != dates[-1] else LIVE)
    path = f'/tmp/morning-briefing-summary-{date}.txt'
    write(path, text + '\n')
    say(f'morning message (saved to {path}):')
    print(text, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('run', help='YYYY-MM-DD, or a path to YYYY-MM-DD.json')
    ap.add_argument('--repo', default=default_repo())
    ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--rebuild-all', action='store_true')
    ap.add_argument('--force', action='store_true', help='replace an existing data/runs file with a different one')
    ap.add_argument('--shots')
    ap.add_argument('--message')
    ap.add_argument('--local-jobs', default=bl.LOCAL_JOBS_PATH)
    ap.add_argument('--allow-example', action='store_true')
    a = ap.parse_args()
    if a.allow_example and not a.no_push:
        sys.exit('--allow-example is for local tests only; use it with --no-push')

    date = resolve_run(a.run, a.repo, a.force)
    r = build(a.repo, date, a.rebuild_all, a.local_jobs, a.allow_example)

    import verify_run
    say('verifying in headless Chrome...')
    fails, report = verify_run.verify(a.repo, date, a.shots)
    say('verification: ' + json.dumps({k: v for k, v in report.items() if k in ('index', f'archive/{date}/', 'archive', 'contrast_min_text', 'contrast_pairs', 'type_sizes', 'console_errors', 'external_requests')}, ensure_ascii=False))
    if fails:
        sys.exit('verification FAILED, nothing committed:\n  ' + '\n  '.join(fails))
    say('all checks passed')

    sync_build_scripts(a.repo)
    if a.no_push:
        say('--no-push: stopping before commit')
        print_summary(a.repo, date)
        return
    msg = a.message or f'Briefing run {date}: {len(r["jobs"])} roles, {r["counts"]["stories"]} stories'
    sha, env, token = commit_and_push(a.repo, msg)
    wait_live(a.repo, date, sha, env, token)
    say(f'done: {LIVE}  {LIVE}archive/  {LIVE}archive/{date}/')
    print_summary(a.repo, date)


if __name__ == '__main__':
    main()
