import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-26.json'))
D = '2026-11-26'
dr = live['dropped']
final_kept = {}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
sh_sources.append({'name': 'Wellfound (signed-in browser pass)', 'ok': True, 'pulled': 2129, 'fresh': 2, 'kept': 2, 'error': None})
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 661, 'fresh': 1, 'kept': 1, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 125, 'fresh': 2, 'kept': 2, 'error': None})
WF = 'Wellfound browser pass (signed in, 26 Nov)'
WFV = 'Wellfound posting page opened, ' + D
jobs = [
 dict(rank=1, tier='evergreen', url='https://job-boards.greenhouse.io/canonical/jobs/2166631',
      title='Software Developer in Observability', company='Canonical',
      location_as_stated='Home based - EMEA ("based remotely in the EMEA and Americas regions")',
      posted='Himalayas listed 2026-11-01 (Greenhouse req first published 2020-04-28, updated 2026-11-19)', salary_as_shown='Not shown',
      experience_asked='"A proven track record in Python and/or Go"; no years stated in the text I read.',
      found_via='Himalayas (live search), checked against the Greenhouse API', verified='Greenhouse API listing, live ' + D,
      fit='Python is his core language, and the role is a cloud-native monitoring stack built in the open, with a fully remote EMEA option.',
      gaps='Always-open listing that Canonical keeps refreshing. Expects Kubernetes, Linux and observability depth that his CV does not show, and Canonical\'s process is long.'),
 dict(rank=2, tier='stretch', url='https://wellfound.com/jobs/5137127-software-engineer',
      title='Software Engineer', company='Grist',
      location_as_stated='Hires remotely "Everywhere"; remote only; company in New York City; requirement: "Working hours that overlap with New York\'s, give or take 3 hours" (Wellfound)',
      posted='Wellfound "Posted: yesterday" (2026-11-25)', salary_as_shown='$100k-$120k', experience_asked='"No experience required"; BS or higher in Computer Science or similar.',
      found_via=WF, verified=WFV + '; page opened with the listing live',
      fit='TypeScript, SQL and Node.js are what the role asks, the pay is well above the other roles today, and Grist builds an MCP server and AI features.',
      gaps='The New York overlap rule (give or take 3 hours) is hard from Nairobi, which is 8 hours ahead; hiring starts with a puzzle submission, and the team is distributed but US-centred.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
dropped = [
 drop('https://wellfound.com/jobs/5135205-software-engineer','Software Engineer','Azodha','Hires remotely "Everywhere"; page says "Fully remote within the US" and "Candidates must be authorized to work in the United States"','Requires US work authorisation despite the Everywhere tag; asks 1-3 years of backend.','location',posted='Wellfound "Reposted: 2 days ago"',found=WF,verified=WFV),
 drop('https://jobs.micro1.ai/post/53b35cc0-377e-4c11-b23f-289b0cf02a72','Engineering Education Practitioner - Learning & Assessment Specialist','micro1','Remote (global) tag; description says "Remote - USA Preferred"','The only new micro1 role: contractor work for engineering professors and education practitioners reviewing learning materials, not a software role.','stack',posted='2026-11-25',found='micro1 job portal API',verified='micro1 posting page opened, '+D),
 drop('https://jobgether.com/offer/6b07459e1870ab7f4cc869b0-forward-deployed-ai-engineer-python-llms-rag','Forward Deployed AI Engineer (Python, LLMs, RAG)','Gramian Consulting','Jobgether: Turkey, Asia, Middle East, EMEA, APAC; description says "Remote - Turkey and Georgia"','Kenya not named, description limits it to Turkey and Georgia, and it asks 6+ years.','location',posted='2026-11-25',found='Jobgether (live search)',verified='Jobgether page opened in the box browser, '+D),
 drop('https://jobgether.com/offer/6b07a8351870ab7f4cca3ddf-ai-software-engineer','AI Software Engineer','Scale Army Careers','Jobgether: Africa, Sub-Saharan Africa, EMEA and others; "must be available to work during U.S. business hours"','Asks 4+ years (Jobgether tags Mid-level 2-5) and US business-hours availability.','experience',posted='2026-11-26',found='Jobgether (live search)',verified='Jobgether page opened in the box browser, '+D),
 drop('https://jobgether.com/offer/6b07459e1870ab7f4cc86a1e-automation-specialist-web-developer','Automation Specialist / Web Developer','ReWorks Solutions','Jobgether: South Africa, Africa, Sub-Saharan Africa, EMEA','Asks 4+ years of Monday.com and Make.com experience; a Monday.com CRM role, not his stack.','stack',posted='2026-11-25',found='Jobgether (live search)',verified='Jobgether page opened in the box browser, '+D),
 drop('https://weworkremotely.com/remote-jobs/beyondtrust-software-development-engineer','Software Development Engineer','BeyondTrust','We Work Remotely: Anywhere in the World; benefits text says "Fully remote within the UK"','The posting restricts remote work to the UK; Java and Spring Boot with Angular.','location',posted='2026-11-25',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://arc.dev/remote-jobs/j/q251i19p5i','Python Software Engineer (Systematic Trading Infrastructure) - Part-time - Worldwide','Arc (exclusive listing)','Arc card: "Min. 4 hr working overlap with Hong Kong"; part-time','Part-time, with a four-hour Hong Kong overlap; finance trading infrastructure.','requirement',posted='2026-11-25',found='Arc (live search)',verified='Arc listing page opened, '+D+' (card only; no full posting text)'),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-26.json'))
def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None,salary='Not shown'):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown=salary,fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
feed_jobs=[
 fj('AI Automation & Operations Optimisation Specialist','Talent Match Africa','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/ai-automation-and-operations-optimisation-specialist-talent-match-africa','2026-11-25','AI and automation role that matches his n8n and workflow work.'),
 fj('Software Developer Intern','Softclans Technologies Limited','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/software-developer-intern-softclans-technologies-limited-8','2026-11-25','Probably too junior for him (internship level), kept for completeness.'),
 fj('Frontend Software Developer','Riset Software & Systems Ltd','Nairobi (on-site)','Fuzu','https://www.fuzu.com/kenya/jobs/frontend-software-developer-riset-software-systems-ltd-030f9ba6','2026-11-21','Entry level; React.js, JavaScript ES6+ and REST match his CV. On-site in Nairobi. Deadline 28 Nov.',deadline='2026-11-28'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 125, 'pulled_is_approximate': True, 'kept': 2, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 661, 'pulled_is_approximate': True, 'kept': 1, 'signed_in': True, 'error': None},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-26T08:45:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','Canonical Greenhouse board','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': sum(1 for j in jobs if j.get('unchecked')), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "ReliefWeb failed in the automated search (parse error) and the automated Wellfound fetch is disabled by design, so Wellfound is recorded as failed there; the signed-in browser pass covered it instead (about 2,129 listings seen, about 25 read, 2 kept). "
   "Jobgether returned 569 roles and 236 fresh; 35 passed the filters, but the ones I opened list Turkey and Georgia, or ask 4+ years with US business hours, or need Monday.com experience, so none were kept; the rest are Europe or UK lists that do not name Kenya. "
   "micro1 returned 66 roles and 12 fresh, 6 kept and 1 new: the new one is an engineering-professor education task, so there is nothing new for Ben there. "
   "Browser passes (signed in, 26 Nov): Wellfound (2 kept: Grist shortlisted, Azodha dropped because it needs US work authorisation), Fuzu (about 661 listings, 1 kept) and the MyJobMag personalised feed (about 125 pulled, 2 kept). "
   "Syd Life AI's Junior Software Engineer (within 3 hours of UK time) was left out because Ben applied to it on 24 Nov. "
   "BeyondTrust's role is tagged Anywhere in the World on We Work Remotely, but the text says fully remote within the UK, so it is dropped. "
   "Canonical's Observability role was re-checked against the Greenhouse API. Other new roles that passed the automated filters but were not opened are listed as unchecked.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
 'surfaced_exemptions': [
    'https://job-boards.greenhouse.io/canonical/jobs/2166631',
    'https://wellfound.com/jobs/5137127-software-engineer',
 ],
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
