"""One-off: convert the 2026-10-07 run (CSV + data_meta.py + data_news.py) into
data/runs/2026-10-07.json. Everything is copied from the verified sources; nothing is invented.
Job / story ids are filled in by briefing_lib.normalise_run()."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import briefing_lib as bl

ns = {}
exec(open('/workspace/build/data_meta.py').read(), ns)
exec(open('/workspace/build/data_news.py').read(), ns)
meta, NEWS = ns['meta'], ns['NEWS']
rows = list(csv.DictReader(open('/workspace/remote-jobs-2026-10-07.csv')))

# Primary reason code for each dropped role (the full reason text is kept verbatim in "reason").
REASON_CODE = {
 'spotter.ai': 'location', 'viseven': 'closed', 'powerprozesse': 'location', 'sobes.tech': 'requirement',
 'kdci1': 'location', 'clanx': 'location', 'talent-journey': 'location', 'dualentry': 'location',
 'makersite': 'location', 'namecheap': 'location', 'wesoftyou': 'experience', 'novakid': 'experience',
 'the-agency-fund': 'experience', 'g2i': 'experience', 'accelerant': 'experience', 'trafilea': 'experience',
 'nodeworthy': 'experience', 'distantjob': 'experience', 'correlation-one': 'location',
 'canonical/jobs/6707669': 'stale', 'remotive.com': 'location', 'launchdarkly': 'location', 'hr-plus': 'stack',
}
def code_for(url):
    hits = [c for k, c in REASON_CODE.items() if k in url]
    assert len(hits) == 1, url
    return hits[0]

def common(r):
    return {
        'url': r['posting_url'], 'title': r['title'], 'company': r['company'],
        'location_as_stated': r['location_eligibility_as_stated'], 'posted': r['posted_date'],
        'salary_as_shown': r['salary_as_shown'], 'experience_asked': r['experience_asked'],
        'found_via': r['found_via'], 'verified': r['verified_on'], 'note': r['fit_note'],
    }

jobs, dropped = [], []
for r in rows:
    if r['rank']:
        n = int(r['rank']); tier, fit, gaps = meta[n]
        jobs.append({'rank': n, 'tier': tier, **common(r), 'fit': fit, 'gaps': gaps})
    else:
        dropped.append({**common(r), 'reason': r['status'].replace('Dropped: ', '', 1), 'reason_code': code_for(r['posting_url'])})

MONTHS = {'Oct': 10, 'Sep': 9}
def iso(label):            # "6 Oct 2026" -> "2026-10-06"
    d, m, y = label.split(); return f'{y}-{MONTHS[m]:02d}-{int(d):02d}'

groups = []
for gname, gid, items in NEWS:
    assert bl.NEWS_GROUPS[gid] == gname
    groups.append({'id': gid, 'stories': [
        {'title': t, 'summary': s, 'why': w, 'source': src, 'date': iso(d), 'url': u} for (t, s, w, src, d, u) in items]})

run = {
  'schema_version': bl.SCHEMA_VERSION,
  'run_date': '2026-10-07',
  'checked_at': '2026-10-07T21:30:00+03:00',
  'sources': {
    'jobs': ['Remotive API (returned only 17 jobs)', 'RemoteOK API', 'Himalayas API (including searches filtered to Kenya)',
             'Jobicy API', 'We Work Remotely RSS', 'Working Nomads', 'employer job pages on Greenhouse, Lever and Recruitee',
             'web search (DOU.ua, OpenTrain, Jobgether)'],
    'news': ['Mistral', 'Google', 'Reflection AI', 'GitLab', 'TechCabal', 'TechCrunch', 'Disrupt Africa', 'The Condia',
             'The Star (AP)', 'Boston Globe', 'Safaricom', 'Techweez'],
  },
  'counts': {
    'pulled': 1060, 'pulled_is_approximate': True,
    'filtered_out': {'older_than_30_days': 150, 'senior_title': 250, 'not_target_role': 400, 'location_or_timezone': None},
    'filtered_out_is_approximate': True,
    'reviewed_closely': len(jobs) + len(dropped),
    'shortlisted': len(jobs),
    'dropped': len(dropped),
    'dropped_by_reason': {},   # filled by normalise_run
    'stories': sum(len(g['stories']) for g in groups),
  },
  'method': {
    'filtering_summary': 'Of about 1,060 postings pulled, about 150 were more than 30 days old, about 250 had senior, lead or manager titles, about 400 weren\u2019t target roles, and most of the rest were limited to the US, EU or LATAM, or to time zones that exclude UTC+3.',
  },
  'jobs': jobs,
  'dropped': dropped,
  'news': {'groups': groups},
}
run = bl.normalise_run(run)
errs, warns = bl.validate_run(run, '2026-10-07')
assert not errs, errs
out = '/workspace/briefing-site/data/runs/2026-10-07.json'
bl.write_run(run, out)
print('wrote', out, len(jobs), len(dropped), run['counts']['stories'], run['counts']['dropped_by_reason'], warns)
