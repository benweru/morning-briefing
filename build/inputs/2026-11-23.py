import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-23.json'))
D = '2026-11-23'
dr = live['dropped']
final_kept = {'Greenhouse': 1, 'We Work Remotely': 1}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
for x in sh_sources:
    if x['name'] == 'Greenhouse': x['name'] = 'Greenhouse'; x['kept'] = 2
    if x['name'] == 'WeWorkRemotely': x['kept'] = 1
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 983, 100, 1, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 701, 'fresh': 701, 'kept': 2, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 50, 'fresh': 50, 'kept': 3, 'error': None})
jobs = [
 dict(rank=1, tier='top', url='https://job-boards.greenhouse.io/canonical/jobs/8379825',
      title='Graduate Software Engineer, Open Source and Linux, Canonical Ubuntu', company='Canonical',
      location_as_stated='Home based - Worldwide (Greenhouse)',
      posted='2026-11-16', salary_as_shown='Not shown',
      experience_asked='Central application for 2026 and 2027 graduate software engineers; strong academic results; work in Python, Go, Rust, C/C++, JavaScript or Bash; interest in open source.',
      found_via='Greenhouse API (live search)',
      verified='Greenhouse job API, first published and updated 2026-11-16, live '+D,
      fit='Worldwide graduate programme that matches his 2026 degree, with Python on the list of languages.',
      gaps='Highly competitive. His earlier Canonical graduate application (Oct) was rejected on 14 Oct, so check whether the same team will review this one. Not in the applied log under this req number.'),
 dict(rank=2, tier='stretch', url='https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-python-ai-engineering-agent-foundations',
      title='Backend Engineer (Python), AI Engineering: Agent Foundations', company='GitLab',
      location_as_stated='Anywhere in the World (We Work Remotely); GitLab says some roles carry country-based eligibility, to be confirmed in the process',
      posted='2026-11-21', salary_as_shown='Not shown',
      experience_asked='Titled Intermediate Backend Engineer (Python). No years stated. Production Python APIs, LangGraph or LangChain agent work, REST and GraphQL, on-call rota.',
      found_via='We Work Remotely RSS (live search)', verified='We Work Remotely page opened, "Posted 1 day ago", '+D,
      fit='Python backend plus LLM agent flows (LangGraph) is close to his Kwara automation work and his own agent projects.',
      gaps='Intermediate level asking for production experience in a mature codebase and on-call duty; Kenya is not named; confirm country eligibility with GitLab before applying.'),
 dict(rank=3, tier='stretch', url='https://job-boards.eu.greenhouse.io/sportygroup/jobs/5030656101',
      title='Applied AI Engineer (LLM)', company='Sporty Group',
      location_as_stated='EMEA (Greenhouse); remote-first, core hours 10am-3pm local time',
      posted='2026-11-20', salary_as_shown='Not shown',
      experience_asked='3+ years in software engineering, ML engineering or applied AI.',
      found_via='Greenhouse API (live search)', verified='Greenhouse EU board page opened, '+D,
      fit='EMEA remote role building LLM systems, in the same area as his LLM integrations at Kwara and his fine-tuned Hermes 2 Pro capstone.',
      gaps='Asks 3+ years, which is more than he has on paper; the role is applied ML with production focus.'),
 dict(rank=4, tier='stretch', url='https://wellfound.com/jobs/5133317-qa-engineer-clone',
      title='Junior Software Engineer', company='Syd Life AI',
      location_as_stated='Remote only; "Hires remotely: Everywhere" (Wellfound); no Kenya-specific rule shown',
      posted='2026-11-22', salary_as_shown='$25k-$40k',
      experience_asked='2+ years. React and React Native, with Node.js later.',
      found_via='Signed-in Wellfound browser pass', verified='Wellfound page opened in the signed-in browser, "Posted yesterday", '+D+'. The URL slug says QA Engineer but the page shows Junior Software Engineer.',
      fit='React and React Native are on his CV, and the pay band is stated.',
      gaps='Contract with no visa sponsorship; asks 2+ years; the URL slug does not match the title, so confirm the right posting when you open it.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
dropped = [
 drop('https://jobs.micro1.ai/post/32f53086-51ef-4e17-8865-0b8f0bf8a6fa','GPU Programming Software Engineer','micro1','Remote (global)','CUDA, WebGPU, GLSL and C++ specialist role; not his stack.','stack',posted='2026-11-20',found='micro1 job portal API'),
 drop('https://jobs.micro1.ai/post/76b0e621-b4f4-4fa4-bd7b-c4fe96f96610','CUDA Engineering Expert','micro1','Remote (global)','CUDA and C++ expert role; not his stack.','stack',posted='2026-11-20',found='micro1 job portal API'),
 drop('https://jobgether.com/offer/6b01ffca1870ab7f4cb18d39-junior-ace-software-engineer','Junior ACE Software Engineer','Best and Less Travel','Remote from Egypt, Africa, Middle East, EMEA (Jobgether)','Autodesk Revit add-ins in C# and .NET; the same listing is copied under several company names.','stack',posted='2026-11-21',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6b00a05b8acd9c1f9b351f0e-junior-ai-engineer','Junior AI Engineer','Cypher Coders','Remote from Egypt, Africa, Middle East, EMEA (Jobgether)','Asks a minimum 2 years of AI/ML with computer vision and Revit skills; copied under several company names.','requirement',posted='2026-11-20',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6aff78ce8acd9c1f9b2efe03-junior-python-developer','Junior Python Developer','European Dynamics','Europe, EU, Greece (Jobgether)','Limited to Greece and the EU.','location',posted='2026-11-19',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6b01c7601870ab7f4cb0c6d8-junior-software-engineer-angular-node.js---op02304','Junior Software Engineer (Angular, Node.js)','Dev.Pro','Europe, EU, EMEA, Poland (Jobgether)','Listed for Poland and the EU only.','location',posted='2026-11-21',found='Jobgether (live search)'),
 drop('https://wellfound.com/jobs/5133313-operations-manager-clone','AI Research Engineer','Syd Life AI','Remote, Everywhere (Wellfound)','Research engineering role asking 2+ years; the URL slug shows Operations Manager but the page shows AI Research Engineer.','experience',posted='2026-11-22',found='Signed-in Wellfound browser pass'),
 drop('https://wellfound.com/jobs/5127245-generative-ai-engineer','Generative AI Engineer','autonent','Remote, Everywhere; preferred time zones China and Japan (Wellfound)','2+ years of Python; INR 50,000-70,000 and preferred East Asian time zones.','location',posted='2026-11-21',found='Signed-in Wellfound browser pass'),
 drop('https://wellfound.com/jobs/5105659-full-stack-ai-engineer','Full Stack AI Engineer','Digit88','Remote header, but description says Bangalore hybrid (Wellfound)','Description says Bangalore hybrid; asks 4+ or 5+ years.','experience',posted='2026-11-20',found='Signed-in Wellfound browser pass'),
 drop('https://wellfound.com/jobs/5130495-quant-engineer-part-time-clone','Software Engineer (Part-time)','Noether Meridian','Remote, Everywhere (Wellfound)','Quant research part-time contract with C++ and no pay shown.','stack',posted='2026-11-22',found='Signed-in Wellfound browser pass'),
 drop('https://wellfound.com/jobs/4424702-software-developer-intern-clone','Agentic Software Developer - Intern','Utilyze','Remote, Everywhere (Wellfound)','Unpaid internship aimed at academic credit.','other',posted='2026-11-23',found='Signed-in Wellfound browser pass'),
 drop('https://arc.dev/remote-jobs/j/pzxx6zf855','Full-Stack Developer','Arc Exclusive','Worldwide (Arc)','Arc lists it as Senior-level freelance.','experience',posted='2026-11-16',found='Arc.dev (live search)'),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-23.json'))

def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown='Not shown',fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
FZ='https://www.fuzu.com/kenya/job?filters[country_id]=1&filters[job_id]='
feed_jobs=[
 fj('Graduate Trainee Programme-Engineering','Angaza','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/graduate-trainee-programme-engineering-angaza','2026-11-19','Builds, tests and ships SaaS features; open to computer science, software engineering and IT degrees.',also=[dict(source='Fuzu',url=FZ+'1067555&filters[term]=Graduate%20Trainee%20Programme-Engineering',company='Angaza',posted='2026-11-22',deadline='2026-11-29')]),
 fj('Junior AI Product Development Specialist','KiliMax Software','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/junior-ai-product-development-specialist-kilimax-software','2026-11-19','Junior AI product role, 0-3 years. Ben applied to KiliMax on 20 Nov.',applied=True),
 fj('ICT Officer II','The Public Procurement Regulatory Authority (PPRA)','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/ict-officer-ii-the-public-procurement-regulatory-authority-ppra','2026-11-18','Codes, debugs and tests small application modules under senior developers; government role.'),
 fj('Frontend Software Developer','Riset Software & Systems Ltd','Nairobi','Fuzu',FZ+'1067521&filters[term]=Frontend%20Software%20Developer','2026-11-21','Full-time permanent; experience listed as 0 months.','2026-11-28'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 50, 'pulled_is_approximate': True, 'kept': 3, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 701, 'pulled_is_approximate': False, 'kept': 2, 'signed_in': True, 'error': None},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-23T08:30:00+03:00',
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
   "Himalayas (incomplete read), LinkedIn (429 rate limit) and ReliefWeb (timeout) failed in the automated search, and the automated Wellfound fetch is disabled by design. "
   "Browser passes (signed in, 23 Nov): Wellfound (983 results, about 100 cards read, 1 shortlisted), Fuzu (701 jobs; keyword searches: software developer 93, python 16, react 3, AI engineer 7, full stack 2; 2 kept) and the MyJobMag personalised feed (about 50 roles, 3 kept). "
   "Jobgether returned 510 roles and 210 fresh; none were shortlisted because the Africa-tagged Junior ACE and Junior AI Engineer listings are copies of one Revit/.NET or computer-vision post under many company names, and the rest were Europe-only. "
   "micro1 returned 65 roles; the new ones are GPU, CUDA and machine-learning research roles that don't fit his stack, so none were shortlisted.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
