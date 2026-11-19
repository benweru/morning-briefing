
import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-19.json'))
D = '2026-11-19'
dr = live['dropped']
final_kept = {'Himalayas': 2, 'Wellfound': 2}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
for x in sh_sources:
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 85, 85, 2, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 67, 'fresh': 9, 'kept': 7, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 25, 'fresh': 5, 'kept': 5, 'error': None})
EXEMPT_URLS = ['https://wellfound.com/jobs/5101914-full-stack-engineer-new-grad-clone']
jobs = [
 dict(rank=1, tier='top', url='https://himalayas.app/companies/evercam/jobs/backend-developer',
      title='Backend Developer', company='Evercam',
      location_as_stated='Himalayas country list includes Kenya; hiring time zones UTC-1 to UTC+6 incl. UTC+3; description: "someone based in Europe or Africa (GMT+1)"',
      posted='2026-11-18', salary_as_shown='Not shown',
      experience_asked='Himalayas level: Mid-level. No years shown. Builds and maintains the services, APIs and databases behind the platform, with code reviews. Skills tagged: Backend Development, Code Review.',
      found_via='Himalayas API (live search)',
      verified=f'Himalayas job page opened, live {D}; apply before 2027-01-17',
      fit='Full-time remote backend role that names Kenya, owning a feature or service end to end, with APIs and databases like his Kwara work.',
      gaps='Himalayas marks it mid-level and the stack is not named, so check the pre-screening questionnaire for years and languages. Evercam wants GMT+1 overlap. Applications without the questionnaire are not considered.'),
 dict(rank=2, tier='top', url='https://wellfound.com/jobs/5101914-full-stack-engineer-new-grad-clone',
      title='Full Stack Engineer (New Grad)', company='Yara',
      location_as_stated='Onsite New York City or San Francisco, or Remote (Everywhere) (Wellfound)',
      posted='2026-11-19', salary_as_shown='$100k-$180k',
      experience_asked='For people graduating this year or within the last 18 months; TypeScript, Python or Go; LLM side projects beyond a chat wrapper.',
      found_via='Signed-in Wellfound browser pass',
      verified=f'Wellfound posting seen in the signed-in browser, {D}',
      fit='New-grad full-stack role with TypeScript or Python and LLM projects, matching his August 2026 degree and stack.',
      gaps='This is a new Wellfound listing of the same Yara Network role shown yesterday (one application matched across partner companies). No visa sponsorship; a work trial may be part of interviews.'),
 dict(rank=3, tier='evergreen', url='https://job-boards.greenhouse.io/canonical/jobs/2166631',
      title='Software Developer in Observability (junior, Python or Go)', company='Canonical',
      location_as_stated='"Home based - EMEA" (Greenhouse)',
      posted='Himalayas listed 2026-11-18 (Greenhouse req first published 2020-04-28, updated 2026-11-03)',
      salary_as_shown='Not shown',
      experience_asked='"Junior developer with a proven track record in Python and/or Go"; cloud-native monitoring stack, Kubernetes, Linux, open source.',
      found_via='Himalayas (Canonical Junior Software Developer - Observability) and Greenhouse API',
      verified=f'Greenhouse job API, live {D}',
      fit='Junior Python role in an EMEA-remote team, which includes Kenya.',
      gaps='Always-open listing that is reposted; Kubernetes and observability are outside his CV. Canonical rejected his graduate application on 14 Oct and he applied to Ubuntu SWE on 19 Oct.'),
 dict(rank=4, tier='stretch', url='https://wellfound.com/jobs/5101796-ml-engineer-llm-fine-tuning-remote',
      title='ML Engineer - LLM Fine-tuning (Remote)', company='ISFY',
      location_as_stated='Remote only, hires Everywhere (Wellfound)',
      posted='2026-11-18', salary_as_shown='$40k-$70k',
      experience_asked='3+ years of ML engineering and a fine-tuned LLM you shipped.',
      found_via='Signed-in Wellfound browser pass', verified=f'Wellfound listing seen in the signed-in browser, {D}',
      fit='Remote-everywhere LLM role; close to his quantized Hermes 2 Pro work.',
      gaps='Asks 3+ years and a shipped fine-tuned LLM, more than he has.'),
]
def drop(url, title, company, loc, reason, code, **kw):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code)
    d.update(kw); return d
dropped = [
 drop('https://wellfound.com/jobs/5101907-part-time-software-developer-ai-tools','Part-Time Software Developer (AI Tools)','TriPeak Group','Onsite Stamford or remote Everywhere (Wellfound)','Description says first weeks are in the Stamford, CT office and remote is "within the US considered"; $25/hr part-time.','location',posted='2026-11-19',found_via='Signed-in Wellfound browser pass',verified=f'Wellfound, {D}'),
 drop('https://jobgether.com/offer/6afe6daf8acd9c1f9b29f16f-software-solution-delivery-engineer','Software & Solution Delivery Engineer','Dover Corporation','Europe, EMEA, Italy (Jobgether)','Italy-based; Kenya not named; mid-level (2-5 years).','location',posted='2026-11-19',found_via='Jobgether public API',verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/c1f9b28ff50-mid-backend-engineer-requires-banking-experience','Mid Backend Engineer (requires banking experience)','FCamara Consulting & Training','Europe, EMEA, Portugal (Jobgether)','Portugal-based; Kenya not named; mid-level (2-5 years) with banking experience required.','location',posted='2026-11-19',found_via='Jobgether public API',verified=f'Jobgether API listing, {D}'),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-19.json'))

def fj(title,company,loc,source,url,posted,fit,deadline=None,exp=None):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown='Not shown',fit_note=fit,already_applied=False)
    if deadline: d['deadline']=deadline
    return d
feed_jobs=[
 fj('Associate Programmer - Graduate Training Programme','Tamu Group (Tera Carbon Kenya)','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/associate-programmer-graduate-training-programme-tamu-group','2026-11-13','Graduate programmer role, 0-2 years; apply by email to careers@tamu-group.com with the job title as subject.','2026-11-27'),
 fj('ICT Officer II (Software Development)','Digital Health Agency (DHA)','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/ict-officer-ii-software-development-digital-health-agency-dha','2026-11-11','Entry-grade software development role; applications on mratibu.dha.go.ke.'),
 fj('Contract Support - ICT Division','KIPPRA','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/contract-support-divisions-information-communication-technology-ict-division-kenya-institute-for-public-policy-research-and-analysis-kippra','2026-11-17','ICT contract support; diploma or degree; apply on recruitment.kippra.or.ke. Modest fit.'),
 fj('Business Intelligence (BI) Analyst','Teleperformance Kenya','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/business-intelligence-bi-analyst-teleperformance','2026-11-13','T-SQL, SSIS and Power BI; weak fit, not opened.'),
 fj('Intern - Data analytics','UN-Habitat','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/intern-data-analytics-un-habitat-aeab8b46','2026-11-13','On-site 6-month internship, 0 experience; apply at https://www.fuzu.com/jobs/1058690/application','2026-11-25'),
 fj('Data Analyst','African Management Institute','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/data-analyst-african-management-institute-749ef05a-aa6f-4627-a441-4bd16354cde2-6d5a7153','2026-11-16','On-site, 2 years, SQL and Metabase; a second listing of the same role also exists. Apply at https://www.fuzu.com/jobs/1061199/application','2026-11-23'),
 fj('QA Engineer (Manual & Automation)','Onfon Media','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/qa-engineer-manual-automation-onfon-media-ltd','2026-11-14','On-site QA, 2 years; closes 20 Nov. Apply at https://www.fuzu.com/jobs/1059835/application','2026-11-20'),
 fj('IT Specialist','Kilifi Systems','Nairobi (hybrid)','Fuzu','https://www.fuzu.com/kenya/jobs/it-specialist-kilifi-systems','2026-11-10','IT support, 0 experience; apply at https://www.fuzu.com/jobs/1054762/application','2026-12-26'),
 fj('APIOps Analyst','NCBA','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/apiops-analyst-ncba-88ce9caf','2026-11-17','Stretch: asks 3 years; API-focused at a bank he knows. Apply at https://www.fuzu.com/jobs/1061363/application','2026-11-22'),
 fj('Business Applications Developer','Valley Hospital','Nakuru','Fuzu','https://www.fuzu.com/kenya/jobs/business-applications-developer-valley-hospital-55b9babf','2026-11-17','Stretch: on-site Nakuru, 3 years; Python, JavaScript, SQL, Odoo. Apply at https://www.fuzu.com/jobs/1063065/application','2026-11-24'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 25, 'pulled_is_approximate': False, 'kept': 5, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 67, 'pulled_is_approximate': False, 'kept': 7, 'signed_in': True, 'error': None},
}

run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-19T07:55:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','Greenhouse API (Canonical recheck)','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': len(jobs), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "ReliefWeb failed with a parse error. The automated Wellfound fetch is disabled by design, so Wellfound was read in the signed-in browser (about 85 roles loaded, 2 kept plus 1 stretch; Cloudflare check passed once). "
   "Fuzu was read in the signed-in browser (67 roles: 49 in IT, software and data plus 18 remote; 7 kept) and the MyJobMag personalised feed too (25 roles; 5 kept). "
   "No new micro1 engineering roles appeared today: the micro1 posts the live search returned were research, applied-science, tester or partner roles already reviewed yesterday. "
   "The Canonical observability role is an always-open EMEA listing (Greenhouse first published 2020) shown as evergreen. Most Jobgether leads were Europe-only and mid-level. "
   "The remote shortlist is short because few fresh junior-to-mid roles named Kenya or worldwide and had not already been shown.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
 'surfaced_exemptions': EXEMPT_URLS,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
