"""Headless-Chrome checks for a generated briefing run. Used by publish_run.py.

Serves the repo at http://127.0.0.1:<port>/morning-briefing/ (the same sub-path GitHub
Pages uses), then checks index.html, archive/<date>/ and archive/:
  - HTTP 200, no console or page errors, no requests leaving the local server
  - counts match the run JSON (jobs, tiers, dropped, stories, groups, New labels, gone list)
  - Kenya jobs section matches run["local_jobs"]: every job with a url is linked, or the single
    'didn't run today' line is shown; no section on runs without a snapshot
  - every job / dropped / story URL from the JSON is linked; external links open in a new tab
  - 'Past briefings' links in nav and footer resolve; archive rows match data/runs, newest first
  - filters, search and the empty state still work
  - design tokens are exactly the v3 values and every text/background pair passes WCAG AA
  - only the v3 type sizes are used; no horizontal overflow at 390px
Run directly:  /workspace/.pwvenv/bin/python verify_run.py [--repo PATH] DATE [--shots DIR]
"""
import argparse, functools, json, os, re, shutil, sys, tempfile, threading, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import briefing_lib as bl

# v3 colour tokens. If the CSS changes any of these, verification fails: update the
# design deliberately (and this table, and the pairs below), never by accident.
V3_COLOURS = {
    'paper': '#fbfaf7', 'surface': '#ffffff', 'ink': '#1b1a17', 'ink-muted': '#57544d', 'rule': '#e2ded5',
    'rule-strong': '#85817a', 'rule-jobs': '#e3d9c8', 'rule-news': '#d3dbe2', 'rule-appendix': '#d6d3cb',
    'accent': '#1f4e8c', 'accent-strong': '#163a69', 'accent-wash': '#eef2f8', 'band-jobs': '#f7f1e6',
    'band-news': '#edf2f6', 'band-appendix': '#ecebe6', 'sec-jobs': '#7a4520', 'sec-news': '#1f5470',
    'tier-top': '#2e6a3e', 'tier-evergreen': '#4a5870', 'tier-stretch': '#82560e', 'gap': '#9a3d22',
    'news-ai': '#3f4c88', 'news-startups': '#1d6561', 'news-hiring': '#6c4570', 'news-kenya': '#8a4a2c',
    # Kenya jobs section (added 2026-10-08)
    'band-local': '#f0f2e8', 'sec-local': '#4d5a22', 'rule-local': '#d9ddc8',
}
TEXT_PAIRS = [  # (foreground token, background token): every text colour on every background it is used on
    *[('ink', b) for b in ('paper', 'surface', 'band-jobs', 'band-news', 'band-appendix')],
    *[('ink-muted', b) for b in ('paper', 'surface', 'band-jobs', 'band-news', 'band-appendix')],
    *[('accent', b) for b in ('paper', 'band-jobs', 'band-news', 'band-appendix')],   # links, New label
    ('sec-jobs', 'band-jobs'), ('sec-news', 'band-news'),
    ('tier-top', 'band-jobs'), ('tier-evergreen', 'band-jobs'), ('tier-stretch', 'band-jobs'), ('gap', 'band-jobs'),
    ('news-ai', 'band-news'), ('news-startups', 'band-news'), ('news-hiring', 'band-news'), ('news-kenya', 'band-news'),
    ('surface', 'accent'), ('surface', 'accent-strong'), ('paper', 'ink'),
    ('ink', 'band-local'), ('ink-muted', 'band-local'), ('accent', 'band-local'), ('sec-local', 'band-local'),
]
GRAPHIC_PAIRS = [  # 3:1 for borders, swatches, rules
    ('rule-strong', 'surface'), ('rule-strong', 'band-jobs'), ('accent', 'band-jobs'),
    ('tier-top', 'band-jobs'), ('tier-evergreen', 'band-jobs'), ('tier-stretch', 'band-jobs'),
    ('sec-jobs', 'paper'), ('sec-news', 'paper'),
    ('sec-local', 'paper'), ('gap', 'band-local'), ('sec-local', 'band-local'), ('rule-strong', 'band-local'),
]
TYPE_SIZES = {'14px', '16px', '18px', '22px', '30px', '44px'}
CHROME = '/usr/bin/google-chrome'


def _lum(h):
    c = [int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def page_tokens(html_text):
    root = re.search(r':root\s*\{(.*?)\n\}', html_text, re.S).group(1)
    return {k: v.strip().lower() for k, v in re.findall(r'--([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;', root)}


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class _Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):   # browser closed a socket early: not a failure
        pass


def serve(repo):
    tmp = tempfile.mkdtemp(prefix='briefing-serve-')
    os.symlink(os.path.abspath(repo), os.path.join(tmp, 'morning-briefing'))
    srv = _Server(('127.0.0.1', 0), functools.partial(_Quiet, directory=tmp))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, tmp, f'http://127.0.0.1:{srv.server_address[1]}/morning-briefing/'


def verify(repo, date, shots=None):
    from playwright.sync_api import sync_playwright
    fails, report = [], {}
    check = lambda ok, msg: ok or fails.append(msg)
    dates = bl.list_run_dates(repo)
    run = bl.normalise_run(bl.load_run(bl.run_path(repo, date)))
    latest = bl.normalise_run(bl.load_run(bl.run_path(repo, dates[-1])))
    prev_of = lambda r: (bl.normalise_run(bl.load_run(bl.run_path(repo, p))) if (p := bl.previous_date(dates, r['run_date'])) else None)

    # Design tokens + contrast, read from the generated files themselves.
    for rel in ('index.html', f'archive/{date}/index.html', 'archive/index.html'):
        toks = page_tokens(open(os.path.join(repo, rel), encoding='utf-8').read())
        changed = {k: (toks.get(k), v) for k, v in V3_COLOURS.items() if toks.get(k) != v}
        extra = sorted(set(toks) - set(V3_COLOURS))
        check(not changed and not extra, f'{rel}: colour tokens differ from v3: {changed} new: {extra}')
    ratios = {}
    for fg, bg in TEXT_PAIRS:
        ratios[f'{fg} on {bg}'] = r = contrast(V3_COLOURS[fg], V3_COLOURS[bg])
        check(r >= 4.5, f'contrast {fg} on {bg} = {r} < 4.5')
    for fg, bg in GRAPHIC_PAIRS:
        ratios[f'{fg} vs {bg} (graphic)'] = r = contrast(V3_COLOURS[fg], V3_COLOURS[bg])
        check(r >= 3, f'contrast {fg} vs {bg} = {r} < 3')
    report['contrast_min_text'] = min(v for k, v in ratios.items() if 'graphic' not in k)
    report['contrast_pairs'] = len(ratios)

    srv, tmp, base = serve(repo)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=['--no-sandbox'])
            ctx = b.new_context(viewport={'width': 1280, 'height': 900})
            errors, external = [], []
            ctx.on('request', lambda r: external.append(r.url) if not r.url.startswith((base.split('/morning')[0], 'data:', 'about:')) else None)
            pg = ctx.new_page()
            pg.on('pageerror', lambda x: errors.append(f'{pg.url}: {x}'))
            pg.on('console', lambda m: errors.append(f'{pg.url}: {m.text}') if m.type == 'error' else None)
            ctx.on('response', lambda r: errors.append(f'HTTP {r.status} for {r.url}') if r.status >= 400 else None)

            def load(url):
                resp = pg.goto(url)
                check(resp is not None and resp.status == 200, f'{url}: HTTP {resp.status if resp else "none"}')
                pg.wait_for_timeout(150)
                return resp

            def check_run_page(url, r, label):
                load(url)
                prev = prev_of(r)
                d = bl.diff_runs(r, prev)
                got = pg.evaluate('''() => ({
                  jobs: document.querySelectorAll('.job').length,
                  tiers: [...document.querySelectorAll('.tier')].map(t => t.dataset.group + ':' + t.querySelectorAll('.job').length).join(','),
                  dropped: document.querySelectorAll('.dropped tbody tr').length,
                  stories: document.querySelectorAll('.story').length,
                  groups: [...document.querySelectorAll('.news-group h3')].map(h => h.id.replace('news-', '')).join(','),
                  newTags: [...document.querySelectorAll('.job .new-tag')].map(n => n.closest('.job').dataset.id).sort().join(','),
                  gone: document.querySelectorAll('.gone li').length,
                  diff: document.querySelector('.run-diff').textContent,
                  dateline: document.querySelector('.dateline').textContent,
                  hrefs: [...document.querySelectorAll('a[href^="http"]')].map(a => [a.getAttribute('href'), a.target, a.rel]),
                  archiveLinks: [...document.querySelectorAll('a.archive-link')].map(a => a.href),
                  dataLink: [...document.querySelectorAll('.site-footer a')].map(a => a.href).filter(h => h.endsWith('.json')),
                  kenya: !!document.getElementById('kenya'),
                  kenyaNav: !!document.querySelector('.section-nav a[href="#kenya"]'),
                  localJobs: document.querySelectorAll('#kenya .local-job').length,
                  localLinks: [...document.querySelectorAll('#kenya .local-job a[href^="http"]')].map(a => a.getAttribute('href')),
                  localEmpty: [...document.querySelectorAll('#kenya .local-empty')].map(p => p.textContent),
                  localErrors: document.querySelectorAll('#kenya .local-error').length,
                })''')
                lj = r.get('local_jobs')
                if lj is None:
                    check(not got['kenya'] and not got['kenyaNav'], f'{label}: Kenya section shown but the run has no local_jobs snapshot')
                elif lj.get('status') == 'ok':
                    check(lj.get('date') == r['run_date'], f'{label}: local_jobs dated {lj.get("date")}, run is {r["run_date"]}')
                    check(got['kenya'] and got['kenyaNav'], f'{label}: Kenya section or nav link missing')
                    check(got['localJobs'] == len(lj['jobs']), f'{label}: {got["localJobs"]} Kenya jobs, JSON has {len(lj["jobs"])}')
                    want_local = [j['url'] for j in lj['jobs'] if j.get('url')]
                    check(got['localLinks'] == want_local, f'{label}: Kenya job links {got["localLinks"]} != {want_local}')
                    check(got['localErrors'] == len(lj.get('errors', [])), f'{label}: Kenya error notes {got["localErrors"]}')
                    check(not got['localEmpty'], f'{label}: not-run line shown although local_jobs is ok')
                else:
                    check(got['kenya'] and got['localJobs'] == 0 and got['localEmpty'] == [bl.LOCAL_NOT_RUN],
                          f'{label}: Kenya not-run state wrong: jobs={got["localJobs"]} line={got["localEmpty"]}')
                tiers = ','.join(f'{t}:{n}' for t in bl.TIER_IDS if (n := sum(1 for j in r['jobs'] if j['tier'] == t)))
                exp_groups = ','.join(g for g in bl.NEWS_GROUPS if g in {x['id'] for x in r['news']['groups']})
                check(got['jobs'] == len(r['jobs']), f'{label}: {got["jobs"]} jobs, JSON has {len(r["jobs"])}')
                check(got['tiers'] == tiers, f'{label}: tiers {got["tiers"]} != {tiers}')
                check(got['dropped'] == len(r['dropped']), f'{label}: dropped rows {got["dropped"]}')
                check(got['stories'] == r['counts']['stories'], f'{label}: stories {got["stories"]}')
                check(got['groups'] == exp_groups, f'{label}: news groups {got["groups"]}')
                check(got['newTags'] == ','.join(sorted(d['new_ids'])), f'{label}: New labels {got["newTags"]} != {sorted(d["new_ids"])}')
                check(got['gone'] == len(d['gone']), f'{label}: gone list {got["gone"]} != {len(d["gone"])}')
                if prev is None:
                    check(got['diff'] == 'First briefing, no earlier run to compare.', f'{label}: first-run diff text wrong: {got["diff"]}')
                check(got['dateline'] == bl.long_date(bl.to_date(r['run_date'])), f'{label}: dateline {got["dateline"]}')
                hrefs = {h for h, _, _ in got['hrefs']}
                want = [j['url'] for j in r['jobs']] + [j['url'] for j in r['dropped']] + [s['url'] for g in r['news']['groups'] for s in g['stories']]
                missing = [u for u in want if u not in hrefs]
                check(not missing, f'{label}: links missing for {missing}')
                check(all(t == '_blank' and 'noopener' in rel for _, t, rel in got['hrefs']), f'{label}: an external link does not open in a new tab')
                check(len(got['archiveLinks']) == 2 and all(a == base + 'archive/' for a in got['archiveLinks']), f'{label}: Past briefings links {got["archiveLinks"]}')
                for u in got['dataLink']:
                    with urllib.request.urlopen(u) as resp:
                        check(resp.status == 200 and json.load(resp)['run_date'] == r['run_date'], f'{label}: data link {u}')
                # interactions
                vis = lambda: pg.eval_on_selector_all('.job', 'x => x.filter(j => !j.hidden).length')
                for t in bl.TIER_IDS:
                    n = sum(1 for j in r['jobs'] if j['tier'] == t)
                    if n:
                        pg.click(f'.segmented button[data-filter="{t}"]')
                        check(vis() == n, f'{label}: filter {t} shows {vis()} not {n}')
                pg.click('.segmented button[data-filter="all"]')
                pg.fill('#job-search', 'zzqqxx-no-match')
                check(pg.is_visible('#empty') and vis() == 0, f'{label}: empty state not shown')
                pg.click('#clear-filters')
                check(vis() == len(r['jobs']) and pg.input_value('#job-search') == '', f'{label}: clear did not reset')
                pg.click('.section-nav a.archive-link')
                pg.wait_for_load_state()
                check(pg.url == base + 'archive/' and 'Past briefings' in pg.title(), f'{label}: nav Past briefings went to {pg.url}')
                return {'jobs': got['jobs'], 'dropped': got['dropped'], 'stories': got['stories'], 'new': len(d['new_ids']),
                        'gone': len(d['gone']), 'diff_line': got['diff'], 'links': len(got['hrefs']),
                        'kenya': None if lj is None else (got['localJobs'] if lj.get('status') == 'ok' else 'not run')}

            report['index'] = check_run_page(base, latest, 'index')
            report[f'archive/{date}/'] = check_run_page(base + f'archive/{date}/', run, f'archive/{date}')

            load(base + 'archive/')
            rows = pg.evaluate('''() => [...document.querySelectorAll('.runs tbody tr')].map(tr => ({
              href: tr.querySelector('a.run-link').href, date: tr.querySelector('a.run-link').getAttribute('href').slice(0, 10),
              cells: [...tr.querySelectorAll('td.num')].map(td => td.firstChild.textContent), data: tr.querySelector('a.data-link').href }))''')
            exp = bl.archive_rows(repo)
            check([x['date'] for x in rows] == [x['date'] for x in exp] == sorted(dates, reverse=True), f'archive: rows {[x["date"] for x in rows]} != runs {dates[::-1]}')
            for x, e_ in zip(rows, exp):
                want = [str(e_['shortlisted']), '\u2013' if e_['new'] is None else str(e_['new']), '\u2013' if e_['gone'] is None else str(e_['gone']), str(e_['stories'])]
                check(x['cells'] == want, f'archive {x["date"]}: counts {x["cells"]} != {want}')
            for x in rows:
                for u in (x['href'], x['data']):
                    try:
                        with urllib.request.urlopen(u) as resp:
                            check(resp.status == 200, f'archive link {u}: {resp.status}')
                    except Exception as ex:  # noqa: BLE001
                        fails.append(f'archive link {u}: {ex}')
            pg.click('.section-nav a[href="../"]'); pg.wait_for_load_state()
            check(pg.url == base, f'archive: Latest briefing link went to {pg.url}')
            report['archive'] = {'rows': len(rows), 'dates': [x['date'] for x in rows]}

            # type scale and mobile overflow on all three pages
            sizes = set()
            m = ctx.new_page()
            m.set_viewport_size({'width': 390, 'height': 844})
            for rel in ('', f'archive/{date}/', 'archive/'):
                pg.goto(base + rel); pg.wait_for_timeout(100)
                sizes |= set(pg.evaluate("[...new Set([...document.querySelectorAll('body *')].filter(e => e.offsetParent !== null && [...e.childNodes].some(n => n.nodeType == 3 && n.textContent.trim())).map(e => getComputedStyle(e).fontSize))]"))
                m.goto(base + rel); m.wait_for_timeout(100)
                check(not m.evaluate('document.documentElement.scrollWidth > innerWidth'), f'{rel or "index"}: horizontal overflow at 390px')
            check(sizes <= TYPE_SIZES, f'type sizes outside v3 scale: {sorted(sizes - TYPE_SIZES)}')
            report['type_sizes'] = sorted(sizes, key=lambda s: float(s[:-2]))
            if shots:
                os.makedirs(shots, exist_ok=True)
                for rel, name in (('', 'index'), (f'archive/{date}/', 'archive-run'), ('archive/', 'archive')):
                    pg.goto(base + rel); pg.wait_for_timeout(150)
                    pg.screenshot(path=os.path.join(shots, f'{name}-1280.png'), full_page=True)
                    m.goto(base + rel); m.wait_for_timeout(150)
                    m.screenshot(path=os.path.join(shots, f'{name}-390.png'), full_page=(name == 'archive'))
            check(not errors, f'console/page errors: {errors}')
            check(not external, f'requests left the local server: {external[:5]}')
            report['console_errors'] = len(errors)
            report['external_requests'] = len(external)
            b.close()
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
    return fails, report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('date')
    ap.add_argument('--repo', default='/workspace/briefing-site')
    ap.add_argument('--shots')
    a = ap.parse_args()
    f, rep = verify(a.repo, a.date, a.shots)
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    print('FAILURES:\n' + '\n'.join(f) if f else 'ALL CHECKS PASSED')
    sys.exit(1 if f else 0)
