import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-20.json'))
D = '2026-11-20'
dr = live['dropped']
final_kept = {'micro1': 1, 'We Work Remotely': 1}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
for x in sh_sources:
    if x['name'] == 'WeWorkRemotely': x['kept'] = 1
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 80, 80, 2, None
    if x['name'] == 'Jobgether':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 110, 110, 1, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 45, 'fresh': 45, 'kept': 6, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 25, 'fresh': 25, 'kept': 4, 'error': None})
jobs = [
 dict(rank=1, tier='top', url='https://jobs.micro1.ai/post/d4080820-66c9-48b1-a29a-b8b1752b8e79',
      title='AI Agent Tester', company='micro1',
      location_as_stated='Remote (global) (micro1 job portal)',
      posted='2026-11-16', salary_as_shown='$25-$45/hour (micro1 portal)',
      experience_asked='Generalist role. Skills listed on the portal: ChatGPT, AI agents, attention to detail, following instructions, screen recording, mobile. The job page is built in the browser and shows only the title to a plain fetch, so the full description was not readable.',
      found_via='micro1 job portal API (live search)',
      verified=f'micro1 portal API listing and job page opened, {D}; apply link: https://jobs.micro1.ai/post/d4080820-66c9-48b1-a29a-b8b1752b8e79',
      fit='Hands-on testing of AI agents, like the agent and automation work he already does, and in the same family as the micro1 evaluator role he applied to.',
      gaps='Task-based contract at an hourly rate, not a salary. The description was not readable, so check scope, hours and the AI interview step on the page before applying.'),
 dict(rank=2, tier='evergreen', url='https://job-boards.greenhouse.io/canonical/jobs/6707669',
      title='Junior Ubuntu Software Engineer', company='Canonical',
      location_as_stated='Home based - Worldwide (Greenhouse); "remote roles open in every time zone"',
      posted='Greenhouse req first published 2025-11-07, updated 2026-08-05 (Jobgether shows 30+ days ago)',
      salary_as_shown='Not shown',
      experience_asked='Junior career path for new graduates and early-career engineers; degree in CS or STEM; experience with Rust, Go, Python, Flutter or C/C++; open source passion.',
      found_via='Jobgether (signed-in browser pass), checked on the Greenhouse API',
      verified=f'Greenhouse job API, live {D}',
      fit='Worldwide junior engineering role that explicitly welcomes new graduates, with Python on the list.',
      gaps='Always-open listing, so it is evergreen only. Canonical rejected his graduate application on 14 Oct and he applied to a separate Ubuntu Software Engineer req on 19 Oct. Strong academic track record is asked for.'),
 dict(rank=3, tier='stretch', url='https://wellfound.com/jobs/5106048-founding-engineer-agentbus',
      title='Founding Engineer, AgentBus', company='Stays Up',
      location_as_stated='Remote (Everywhere), San Francisco (Wellfound); "Hires remotely in Everywhere"',
      posted='2026-11-20', salary_as_shown='$100k-$140k',
      experience_asked='No years stated. Wants someone who uses coding agents daily and has built things in the open; stack is TypeScript and Go.',
      found_via='Signed-in Wellfound browser pass',
      verified=f'Wellfound page opened, "Posted: today", {D}; apply at https://staysup.io/apply (no account needed)',
      fit='Builds an open-source tool for running Claude Code and Codex agents, which matches his daily use of AI coding assistants and his own bots.',
      gaps='Founding-engineer scope at a team of 1-10, and the core is Go, which is not on his CV. They want visible open-source work; his best projects are private or not CV-worthy. Visa sponsorship and relocation are not available.'),
 dict(rank=4, tier='stretch', url='https://wellfound.com/jobs/5106013-ai-computer-science-engineer',
      title='AI Computer Science Engineer', company='drytis',
      location_as_stated='Remote only, hires in Israel, Africa, Egypt and the Philippines (Wellfound)',
      posted='2026-11-20', salary_as_shown='$4.26-$17/hour',
      experience_asked='Wellfound tag says no experience required, but the text asks for proven mid-level full-stack experience, React and TypeScript, PHP and Laravel, and prompt engineering with LLM APIs.',
      found_via='Signed-in Wellfound browser pass',
      verified=f'Wellfound page opened, "Posted: today", {D}',
      fit='React, TypeScript and LLM API work match his CV, and Africa is named.',
      gaps='Part-time contract with a wide hourly range; Laravel is coursework-level only; the text and the experience tag disagree.'),
 dict(rank=5, tier='stretch', url='https://weworkremotely.com/remote-jobs/elvoro-ai-creative-engineer-social-media',
      title='AI Creative Engineer (Social Media)', company='Elvoro',
      location_as_stated='Remote, Worldwide; "Anywhere in the World" (We Work Remotely)',
      posted='2026-11-18', salary_as_shown='Not shown ("To be agreed")',
      experience_asked='Professional experience maintaining large production codebases; advanced Python; REST and OAuth 2.0 integrations; FFmpeg or MoviePy; Google Cloud Storage; daily use of AI coding agents.',
      found_via='We Work Remotely RSS (live search)', verified=f'We Work Remotely page opened, "Posted 2 days ago", apply before 2026-12-18, {D}',
      fit='Python plus many API integrations and daily use of Claude Code and Cursor, with a founder-led team.',
      gaps='Asks for advanced Python and large production codebases, more than about a year of experience, and for creative and video-processing skills he has not shown. Project-based contract with only a plan to go full time.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
dropped = [
 drop('https://jobs.micro1.ai/post/8dd58c0e-78c8-44b4-a8e3-0bfbfc1f765f','Machine Learning Researcher','micro1','Remote (global)','Specialist-tier research role at $60-$120/hour; the portal lists only "Machine Learning" and the page shows no description, so a fit cannot be confirmed.','requirement',posted='2026-11-16',found='micro1 job portal API'),
 drop('https://jobs.micro1.ai/post/f65f4c3c-34b6-48bd-96bd-5f274f7dcd09','Applied Scientists - Machine Learning','micro1','Remote (global)','Specialist-tier applied-science role at $60-$120/hour; no description shown, and it is a research role beyond his experience.','experience',posted='2026-11-16',found='micro1 job portal API'),
 drop('https://jobgether.com/offer/6aff78dd8acd9c1f9b2f0119-junior-ai-engineer','Junior AI Engineer','Commerciaux d\'elite','Remote from Egypt, Africa, Middle East, EMEA; "Cairo Preferred" (Jobgether)','Word-for-word copies are listed under Forest Stewardship Council U.S. and Vivid Money, so it looks like an aggregator repost; asks 2+ years of AI/ML, computer vision and Revit.','requirement',posted='2026-11-20',found='Jobgether (signed-in browser pass)'),
 drop('https://jobgether.com/offer/6ae358b8d6c8b081a79126cd-react-native-developer','React Native Developer','Parvana (recruiter)','Tagged Africa and EMEA, but description says "Location: South Africa"','Description restricts the role to South Africa; asks 2-4 years of React Native; 12-month contract.','location',posted='about 2026-10-29',found='Jobgether (signed-in browser pass)',verified='Seen in the signed-in browser pass, 2026-11-20'),
 drop('https://jobgether.com/offer/6aa858aeb563ea142ea8e87f-junior-php-software-engineer','Junior PHP Software Engineer','RichBrains','Remote from Anywhere (Jobgether)','Posted 30+ days ago, so outside the 7-day window; PHP and MySQL only, and PHP is coursework-level for him.','stale',posted='30+ days ago',found='Jobgether (signed-in browser pass)'),
 drop('https://wellfound.com/jobs/4689852-pern-stack-developer-intern','PERN Stack Developer Intern','Lupira','Remote (Everywhere) (Wellfound)','Unpaid 4-month internship ("Stipend: Unpaid"); applications by email to the founder.','other',posted='2026-11-19',found='Signed-in Wellfound browser pass'),
 drop('https://wellfound.com/jobs/4302012-ai-engineer','Ai engineer','drytis','Remote (Everywhere), US time zones preferred (Wellfound)','Asks 3+ years and prefers US time zones; $4.28-$17.15/hour contract.','experience',posted='2026-11-19',found='Signed-in Wellfound browser pass',verified='Seen in the signed-in browser pass, 2026-11-20'),
 drop('https://wellfound.com/jobs/4868453-backend-developer-claude-powered-remote','Backend Developer (Claude-powered, Remote)','ISFY','Remote (Everywhere) (Wellfound)','Posted about a month ago; asks 3+ years; $18k-$30k.','stale',posted='about 2026-10-20',found='Signed-in Wellfound browser pass',verified='Seen in the signed-in browser pass, 2026-11-20'),
 drop('https://wellfound.com/jobs/5086022-agentic-ai-engineer','Agentic AI Engineer','VASHISTHA CONSULTING GROUP','Remote (Everywhere), Indian firm (Wellfound)','Asks 3-10 years; INR 30L-45L plus equity.','experience',posted='2026-11-19',found='Signed-in Wellfound browser pass',verified='Seen in the signed-in browser pass, 2026-11-20'),
 drop('https://himalayas.app/companies/asg-company/jobs/associate-developer','Associate Developer','ASG Company','Himalayas tag: Worldwide','The description says "exclusive only to Filipino locals" and "anywhere in the Philippines"; asks 2 years of Java, JavaScript and C#.','location',posted='2026-11-11',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://job-boards.greenhouse.io/canonical/jobs/6222476','Software Engineer - Python - Container Images','Canonical','Home based - EMEA, Americas, APAC (Greenhouse)','Experienced-engineer role (CI/CD and container DevOps depth, seniority set by ability to lead juniors); Greenhouse updated 2026-08-25.','experience',posted='2026-08-25',found='Himalayas (live search), checked on the Greenhouse API'),
 drop('https://himalayas.app/companies/spotify/jobs/fullstack-engineer-subscriptions','Fullstack Engineer - Subscriptions','Spotify','Himalayas country list includes Kenya; description: EMEA, Central European and GMT time zones','Posted 2026-07-28; Java 17, GraphQL, gRPC and on-call; mid-level.','stale',posted='2026-07-28',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/gitlab-com/jobs/intermediate-fullstack-engineer-subscription-lifecycle','Intermediate Fullstack Engineer, Subscription Lifecycle','GitLab','Remote, AMEA (Himalayas page)','Posted 2026-11-03, outside the 7-day window; intermediate-level Ruby on Rails and Vue with billing flows and an incident rota.','stale',posted='2026-11-03',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/notably/jobs/full-stack-engineer','Full Stack Engineer','Notably','Himalayas lists Kenya, but the description wants Europe or US Eastern time','Asks 3 years; candidates outside Europe or US Eastern time "will not be considered".','location',posted='2026-09-23',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/flying-bisons/jobs/freelance-backend-developer','Freelance Backend Developer','Flying Bisons','Himalayas country list includes Kenya','Posted 2026-08-30; asks 2+ years of PHP and Symfony and Polish at B2+ level.','requirement',posted='2026-08-30',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/clera/jobs/automation-engineer-dealership-integrations-software-engineer','Automation Engineer, Dealership Integrations','Clera','Himalayas: open to all countries, but the description says on-site','Description is on-site with no location, duties or requirements given.','other',posted='2026-11-20',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/banco-plata-s-a-institucion-de-banca-multiple/jobs/risk-data-analyst-integrated-risk-management','Risk Data Analyst','Banco Plata','Himalayas: open to all countries','Posted 2026-10-19; asks 3 years of risk and credit analysis.','experience',posted='2026-10-19',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://himalayas.app/companies/lingaro/jobs/rgm-data-analyst','RGM Data Analyst','Lingaro','Himalayas country list includes Kenya','Posted 2026-10-01; FMCG pricing and price-elasticity analytics, not his focus.','stack',posted='2026-10-01',found='Himalayas API (live search)',verified='Himalayas page read, 2026-11-20'),
 drop('https://remoteOK.com/remote-jobs/remote-software-engineer-ai-tooling-supabase-1137793','Software Engineer AI Tooling','Supabase','Worldwide (RemoteOK)','Must have 5+ years of professional software engineering experience.','experience',posted='2026-11-13',found='RemoteOK API (live search)'),
 drop('https://remoteOK.com/remote-jobs/remote-seo-full-stack-engineer-treatwell-1137805','SEO Full Stack Engineer','Treatwell','Worldwide (RemoteOK)','Mid or senior level; Java and Spring Boot backend with Kubernetes.','experience',posted='2026-11-18',found='RemoteOK API (live search)'),
 drop('https://weworkremotely.com/remote-jobs/fin-forward-deployed-engineer','Forward Deployed Engineer','Fin','Anywhere in the World (We Work Remotely)','Proof of eligibility to work in the United States is required; on-site customer travel.','location',posted='2026-11-19',found='We Work Remotely RSS (live search)'),
 drop('https://arc.dev/remote-jobs/j/pzxx6zf855','Full-Stack Developer','Arc Exclusive','Worldwide (Arc)','Arc lists it as Senior-level freelance.','experience',posted='2026-11-16',found='Arc.dev (live search)',verified='Arc listing page read, 2026-11-20'),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-20.json'))

def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown='Not shown',fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
FZ='https://www.fuzu.com/kenya/job/computers-software-development?'
feed_jobs=[
 fj('Graduate Trainee Programme-Engineering','Angaza','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/graduate-trainee-programme-engineering-angaza','2026-11-19','Graduate programme for CS and IT graduates; experience not stated.'),
 fj('Junior AI Product Development Specialist','KiliMax Software','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/junior-ai-product-development-specialist-kilimax-software','2026-11-19','Junior AI product role, 0-3 years.'),
 fj('ICT Officer II','The Public Procurement Regulatory Authority (PPRA)','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/ict-officer-ii-the-public-procurement-regulatory-authority-ppra','2026-11-18','Builds small application modules; experience not shown.'),
 fj('Associate Programmer - Graduate Training Programme','Tamu Group (Tera Carbon Kenya)','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/associate-programmer-graduate-training-programme-tamu-group','2026-11-13','0-2 years, fresh graduates welcome. Ben emailed this application on 16 Nov.',applied=True),
 fj('Back End Engineer','d.light SOLAR','Nairobi','Fuzu',FZ+'page=3&filters[job_id]=1060150','2026-11-16','2-3 years of Java and Spring Boot. Ben submitted this application on 16 Nov.','2026-11-23',applied=True),
 fj('Data Analyst','African Management Institute','Nairobi','Fuzu',FZ+'page=4&filters[job_id]=1061199','2026-11-16','2-4 years. The same role is listed again, posted 17 Nov, on-site, apply by 24 Nov (no ID captured).','2026-11-23'),
 fj('Intern - Data analytics','UN-Habitat','Nairobi','Fuzu',FZ+'page=4&filters[job_id]=1058690','2026-11-13','On-site 6-month internship; no experience needed.','2026-11-25'),
 fj('QA Specialist','Kinnovarone','Remote (open to applicants in Kenya)','Fuzu',FZ+'page=3&filters[job_id]=1062504','2026-11-17','Fixed term; 2-3 years of QA.','2026-12-30'),
 fj('Business Applications Developer','Valley Hospital','Nakuru (on-site)','Fuzu',FZ+'page=2&filters[job_id]=1063065','2026-11-17','Stretch: 3+ years of Python, JavaScript, SQL and Odoo.','2026-11-24'),
 fj('APIOps Analyst','NCBA','Nairobi (on-site)','Fuzu',FZ+'page=3&filters[job_id]=1061363','2026-11-17','Stretch: 3-5 years.','2026-11-22'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 25, 'pulled_is_approximate': True, 'kept': 4, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 45, 'pulled_is_approximate': False, 'kept': 6, 'signed_in': True, 'error': None},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-20T08:30:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','Jobgether (signed-in browser pass)','Greenhouse API (Canonical recheck)','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': len(jobs), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "Remotive and LinkedIn failed (SSL errors), ReliefWeb failed with a parse error and the Jobgether API closed the connection, so those four returned nothing to the automated search. The automated Wellfound fetch is disabled by design. "
   "Browser passes (signed in, 20 Nov): Jobgether (about 110 listings reviewed from four searches, 1 kept), Wellfound (about 80 of 992 results loaded, 2 shortlisted; Cloudflare check cleared by itself), Fuzu (45 jobs in IT, software and data, 6 kept) and the MyJobMag personalised feed (about 25 listings, 4 kept). "
   "micro1 returned 67 roles, 4 of them new; the AI Agent Tester role is on the shortlist and the two machine-learning research roles are in the dropped list because no description was readable. "
   "Most Himalayas and Jobgether leads were mid-level, limited to Europe or the US, or posted weeks ago; the shortlist is short because few fresh junior-to-mid roles named Kenya or worldwide and had not been shown before.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
 'surfaced_exemptions': ['https://jobs.micro1.ai/post/d4080820-66c9-48b1-a29a-b8b1752b8e79'],
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
