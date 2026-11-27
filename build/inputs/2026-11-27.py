import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-27.json'))
D = '2026-11-27'
dr = live['dropped']
final_kept = {'Himalayas': 1}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
sh_sources.append({'name': 'Wellfound (signed-in browser pass)', 'ok': True, 'pulled': 960, 'fresh': 7, 'kept': 1, 'error': None})
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 657, 'fresh': 6, 'kept': 2, 'error': 'Search parameters ignored; read 4 of 5 pages of the software tag page (56 jobs)'})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 50, 'fresh': 2, 'kept': 0, 'error': None})
WF = 'Wellfound browser pass (signed in, 27 Nov)'
WFV = 'Wellfound posting page opened, ' + D
jobs = [
 dict(rank=1, tier='stretch', url='https://himalayas.app/companies/syd-life-ai/jobs/ai-research-engineer',
      title='AI Research Engineer', company='Syd Life AI',
      location_as_stated='Open to candidates from all countries (Himalayas); hiring timezones UTC-11 to UTC+14',
      posted='2026-11-23', salary_as_shown='$30K - $80K per year (contractor)',
      experience_asked='Himalayas lists Mid-level; no years read.',
      found_via='Himalayas (live search)', verified='Himalayas posting page fetched, ' + D + '; apply before 2026-12-22',
      fit='Open worldwide and LLM-focused (fine-tuning, evaluation, coding agents), close to his LLM and agent work.',
      gaps='Research-level skills (SFT, LoRA, distillation, PPO, study design) he has not shown; contractor, not salaried. Ben already applied to a different Syd Life AI role on 24 Nov.'),
 dict(rank=2, tier='stretch', url='https://wellfound.com/jobs/5138116-software-engineer',
      title='Software Engineer', company='GC works',
      location_as_stated='Hires remotely "Everywhere"; remote only; company in Miami; visa sponsorship available (Wellfound)',
      posted='Wellfound "Posted: yesterday" (2026-11-26)', salary_as_shown='$110k-$160k plus 1-2% equity', experience_asked='3+ years.',
      found_via=WF, verified=WFV,
      fit='JS/TS, React/Next.js, Node or Python and Postgres match his stack; first remote engineer building internal tools, and the pay is well above other roles today.',
      gaps='Asks 3+ years and Ben has about one; a US construction client with no stated time-zone rule, so confirm overlap before applying.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
dropped = [
 drop('https://weworkremotely.com/remote-jobs/celonis-applied-ai-value-consultant','Applied AI Value Consultant','Celonis','We Work Remotely: Anywhere in the World; text: "Candidates must be currently legally authorized to work in Canada" and TN status','Needs Canadian work authorisation and 3-5 years of consulting.','location',posted='2026-11-22',found='We Work Remotely (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-trusted-agentic-development','Backend Engineer, Trusted Agentic Development','GitLab','We Work Remotely: Anywhere in the World; text: "Intermediate Backend Engineer ... based in Poland"','Based in Poland and focused on Rust, Ruby and Go validation tooling.','location',posted='2026-11-23',found='We Work Remotely (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://wellfound.com/jobs/4897619-full-stack-developer-ai-saas','Full-Stack Developer - AI SaaS','Tecavy','Hires remotely "Everywhere"; preferred timezone Pacific Time; visa sponsorship not available','Pays INR 5-9 lakh a year and prefers Pacific Time; asks 2+ years.','requirement',posted='Wellfound "Posted: yesterday"',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5137998-backend-engineer-data-pipelines','Backend Engineer, Data Pipelines','Adanos Software','Header "Berlin - Remote"; body says hybrid with an office in Berlin','Hybrid in Berlin, not remote; asks 3+ years of Python backend.','location',posted='Wellfound "Posted: yesterday"',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5138205-full-stack-engineer-robot-fleet-dashboard-devdoot','Full-Stack Engineer, Robot Fleet Dashboard','World Trade Factory','Hires remotely "Everywhere"','Unpaid three-month internship with no stipend.','other',posted='Wellfound "Posted: today"',found=WF,verified=WFV),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-27.json'))
def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None,salary='Not shown'):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown=salary,fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
feed_jobs=[
 fj('Frontend Software Developer','Riset Software & Systems Ltd','Nairobi (on-site)','Fuzu','https://www.fuzu.com/kenya/jobs/frontend-software-developer-riset-software-systems-ltd-030f9ba6','2026-11-21','Entry level; React, JavaScript and REST match his CV.',deadline='2026-11-28'),
 fj('Graduate Trainee Programme-Engineering','Angaza','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/graduate-trainee-programme-engineering-angaza','2026-11-22','Open to graduates of the last 24 months with no more than 12 months of full-time work since graduating; his Kwara role is close to that limit, so check before applying. Needs Second Class Upper honours.',deadline='2026-11-29'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 50, 'pulled_is_approximate': False, 'kept': 0, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 657, 'pulled_is_approximate': True, 'kept': 2, 'signed_in': True, 'error': 'Search parameters were ignored; read 4 of 5 pages of the software tag page.'},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-27T08:30:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': sum(1 for j in jobs if j.get('unchecked')), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "Himalayas partly failed (2 of 17 requests: IncompleteRead). Jobgether returned 564 roles and 222 fresh, none kept. micro1 returned 74 roles and 12 fresh; 5 passed the filters but all had been shown before and none fits, so there are no new micro1 roles. "
   "Browser passes (signed in, 27 Nov): Wellfound loaded after an earlier Cloudflare block (960 remote-everywhere results seen, 1 kept: GC works; Tecavy, Adanos and World Trade Factory dropped); Fuzu (657 listings, search filters ignored, 4 of 5 pages of the software tag page read, 2 kept); MyJobMag personalised (first 50 read, 0 kept: the only tech role was a support role already in the Kenya section, and a Lead Mobile Engineer role is too senior). "
   "Celonis and GitLab roles from We Work Remotely were opened and dropped for Canadian work authorisation and a Poland base.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')

