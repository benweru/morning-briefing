import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-24.json'))
D = '2026-11-24'
dr = live['dropped']
final_kept = {'Greenhouse': 1}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
for x in sh_sources:
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 95, 8, 0, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 60, 'fresh': 2, 'kept': 2, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 26, 'fresh': 2, 'kept': 2, 'error': None})
jobs = [
 dict(rank=1, tier='stretch', url='https://job-boards.eu.greenhouse.io/sportygroup/jobs/5041600101',
      title='Full-Stack Engineer Central Engineering', company='Sporty Group',
      location_as_stated='EMEA (Greenhouse); remote-first',
      posted='2026-11-23', salary_as_shown='Not shown',
      experience_asked='No years stated in the posting text (the application form has a years-of-experience question). Asks for experience shipping and operating full-stack web apps in production, more than one of Python, TypeScript and Node.js, Docker, AWS, Kubernetes and CI/CD, and MySQL in production.',
      found_via='Greenhouse API (live search)', verified='Greenhouse EU board page opened, '+D,
      fit='Python, TypeScript and React match his stack, and the work (taking internal prototypes to production with tests, CI/CD and security) is close to his Kwara API and automation work.',
      gaps='Asks for production operation of Docker, AWS and Kubernetes and MySQL, and an observability and security baseline, which is more than his one year shows. He applied to Sporty Group\'s Applied AI Engineer (LLM) role earlier today, so a second application is his call.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
WF = 'Signed-in Wellfound browser pass'
WFV = 'Listed in the signed-in Wellfound browser pass, '+D+'. Posting not re-opened (box has no signed-in browser); experience asked was not read.'
dropped = [
 drop('https://jobs.micro1.ai/post/a0ad851b-9953-4630-a348-334ce7f4234f','AI Project Associate','micro1','Remote (global)','Posted as an undergraduate talent network with no immediate opening; it is aimed at current students with 1-3 years to graduation and Ben has graduated.','requirement',posted='2026-11-20',found='micro1 job portal API',verified='micro1 page opened, job schema read, '+D),
 drop('https://jobs.micro1.ai/post/3caa66c3-ef7a-42d6-be2d-1b0b7dc778cf','AI Product Tester (Consumer Safety & Security)','micro1','Remote (global)','Consumer cybersecurity product-testing and feedback role (scam detection, privacy, written reports); not an engineering role.','stack',posted='2026-11-23',found='micro1 job portal API'),
 drop('https://jobs.micro1.ai/post/6fc50b18-0fef-4c66-b934-2aa38cc794fa','AI Agent Tester - Real-World Tasks (Europe)','micro1','Remote (global); title says Europe','Same Europe-focused agent-testing task type Ben skipped on 20 Nov (Europe-only, errands on personal accounts).','location',posted='2026-11-23',found='micro1 job portal API'),
 drop('https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-trusted-agentic-development','Backend Engineer, Trusted Agentic Development','GitLab','Anywhere in the World (We Work Remotely), but the page says "This job is GeoLocked: Poland"','Locked to Poland; Kenya not eligible. Intermediate level.','location',posted='2026-11-23',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-ruby-ai-engineering-ai-catalog','Backend Engineer (Ruby), AI Engineering: AI Catalog','GitLab','Anywhere in the World (We Work Remotely), but the page says "This job is GeoLocked: United Kingdom"','Locked to the UK; Kenya not eligible.','location',posted='2026-11-21',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/dropbox-full-stack-product-software-engineer','Full Stack Product Software Engineer','Dropbox','Anywhere in the World (We Work Remotely); pay range given for Poland','Asks 5+ years and on-call rotation.','experience',posted='2026-11-23',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/smartsheet-software-engineer-ii-full-stack-remote-eligible','Software Engineer II - Full Stack (Remote Eligible)','Smartsheet','Anywhere in the World (We Work Remotely)','Posting says "Legally eligible to work in the U.S."; 2+ years in each of full stack, Java/Kotlin/TypeScript and cloud.','location',posted='2026-11-21',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/twilio-developer-success-engineer-p2','Developer Success Engineer, P2','Twilio','Remote; must work East Coast business hours','East Coast hours do not suit UTC+3; asks 2+ years of coding in a support, solutions or software role.','location',posted='2026-11-21',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/gusto-inc-software-engineer-financial-data-payments','Software Engineer, Financial Data & Payments','Gusto','Anywhere in the World (We Work Remotely)','Asks 10+ years of experience.','experience',posted='2026-11-21',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/descript-software-engineer-product','Software Engineer, Product','Descript','Anywhere in the World (We Work Remotely)','Asks 5+ years building and shipping customer-facing products.','experience',posted='2026-11-23',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://weworkremotely.com/remote-jobs/tailscale-billing-engineer','Billing Engineer','Tailscale','Anywhere in the World (We Work Remotely)','Asks for deep SaaS billing knowledge, proven integrations with billing platforms, Go and technical leadership; senior in scope.','experience',posted='2026-11-21',found='We Work Remotely RSS (live search)',verified='We Work Remotely page opened, '+D),
 drop('https://jobgether.com/offer/6b02ee8d1870ab7f4cb5403a-frontend-engineer-react-next.js','Frontend Engineer (React / Next.js)','99Brightminds','Africa, Middle East, Northern Africa, EMEA, Egypt (Jobgether)','Jobgether lists Mid-level (2-5 years); the Jobgether page returned 403 to the box, so it could not be opened. Needs a browser re-check before it can be shortlisted.','other',posted='2026-11-22',found='Jobgether (live search)',verified='Not opened: Jobgether returned 403, '+D),
 drop('https://himalayas.app/companies/syd-life-ai/jobs/junior-software-engineer','Junior Software Engineer','Syd Life AI','Worldwide (Himalayas)','Already shown in yesterday\'s briefing from Wellfound (same role); asks 2+ years.','other',posted='2026-11-23',found='Himalayas API (live search)'),
 drop('https://himalayas.app/companies/elvoro/jobs/ai-app-developer-chatgpt-claude-grok-connectors-elvoro-ltd','AI App Developer (ChatGPT, Claude & Grok Connectors) - Elvoro Ltd','Elvoro','Remote, Global (Himalayas)','One-time freelance fixed-project contract with pay "To be agreed"; Ben already applied to Elvoro on 20 Nov (AI Creative Engineer).','other',posted='2026-11-22',found='Himalayas API (live search)'),
 drop('https://himalayas.app/companies/featherless-ai/jobs/ai-researcher-multilingual-data-7080086955','AI Researcher - Multilingual Data','Featherless AI','Worldwide (Himalayas)','Language-model research and data role (as are the two Featherless ML Engineer posts); not his stack.','stack',posted='2026-11-24',found='Himalayas API (live search)'),
 drop('https://jobgether.com/offer/6b00ae2d8acd9c1f9b355517-junior-ai-engineer','Junior AI Engineer','Morcali Recruitment en Bemiddeling','Africa, Middle East, Northern Africa, EMEA, Egypt (Jobgether)','Copy of the Revit and computer-vision Junior AI Engineer post dropped yesterday (listed under several company names).','requirement',posted='2026-11-20',found='Jobgether (live search)'),
 drop('https://wellfound.com/jobs/5137127-software-engineer','Software Engineer','Grist','Remote, Everywhere (Wellfound)','Wellfound shows $100k-$120k, posted today. Experience asked was not read in the browser pass, so it cannot be shortlisted until re-checked in the signed-in browser.','other',posted='2026-11-24',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5135540-ai-robotics-engineer-clone','Mobile React Native Engineer','World Trade Factory','Remote, Everywhere (Wellfound)','Posted today. React Native fits his CV, but experience asked and pay were not read; the URL slug says AI Robotics Engineer, so the posting must be re-checked in the signed-in browser.','other',posted='2026-11-24',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5135385-ai-implementation-engineer','AI Implementation Engineer','Kendis','Remote, Everywhere (Wellfound)','Posted yesterday. Close to his automation and LLM work, but experience asked and pay were not read; re-check in the signed-in browser before shortlisting.','other',posted='2026-11-23',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5135384-ai-engineer-b2b-saas-remote','AI Engineer B2B SaaS','Wisetr Technology','Remote, Everywhere (Wellfound)','Posted yesterday, $13k-$20k. Experience asked was not read; re-check in the signed-in browser before shortlisting.','other',posted='2026-11-23',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5127245-generative-ai-engineer','Generative AI Engineer','autonent','Remote, Everywhere; preferred time zones China and Japan (Wellfound)','Dropped yesterday for 2+ years of Python, INR 50,000-70,000 pay and East Asian time zones; same posting.','location',posted='2026-11-21',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5127264-python-developer','Python Developer','WafyNet','Remote, Everywhere (Wellfound)','INR 25,000-30,000 pay (about USD 300 a month at most); experience asked was not read.','other',posted='2026-11-21',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5105659-full-stack-ai-engineer','Full Stack AI Engineer','Digit88','Remote header, but description says Bangalore hybrid (Wellfound)','Dropped yesterday: Bangalore hybrid and 4+ or 5+ years.','experience',posted='2026-11-20',found=WF,verified=WFV),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-24.json'))

def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown='Not shown',fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
feed_jobs=[
 fj('Frontend Software Developer','Riset Software & Systems Ltd','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/frontend-software-developer-riset-software-systems-ltd-030f9ba6','2026-11-21','Entry level; React, JavaScript and REST API integration, which match his CV.','2026-11-28'),
 fj('Business Applications Developer','Valley Hospital','Nakuru (on-site)','Fuzu','https://www.fuzu.com/kenya/jobs/business-applications-developer-valley-hospital-55b9babf','2026-11-17','Asks 3+ years in software development or application support and hospital, insurance or ERP experience; deadline is today.','2026-11-24'),
 fj('Junior AI Product Development Specialist','KiliMax Software','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/junior-ai-product-development-specialist-kilimax-software','2026-11-19','Junior AI product role, 0-3 years. Ben applied to KiliMax on 20 Nov.',applied=True),
 fj('DevOps Engineer','Talent Match Africa','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/devops-engineer-talent-match-africa','2026-11-23','Weak fit: DevOps focus rather than his backend and AI work.'),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 26, 'pulled_is_approximate': False, 'kept': 2, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 60, 'pulled_is_approximate': True, 'kept': 2, 'signed_in': True, 'error': None},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-24T08:30:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','We Work Remotely (page checks)','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': len(jobs), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "ReliefWeb failed in the automated search (parse error) and the automated Wellfound fetch is disabled by design. "
   "Only one role is shortlisted today because the other candidates failed on opening the posting: the two GitLab backend roles and the other We Work Remotely roles are locked to one country, ask 5+ years, require US work eligibility or East Coast hours. "
   "Browser passes (signed in, 24 Nov): Wellfound (about 95 results, 8 kept; none shortlisted because experience asked was not read and the box has no signed-in browser to re-open them, so they are listed under Dropped for a re-check), Fuzu (about 60 jobs, 2 kept) and the MyJobMag personalised feed (26 on the first page, 2 kept). "
   "Jobgether returned 510 roles and 210 fresh; none were shortlisted because the Africa-tagged ones were a copy of the Revit and computer-vision post or could not be opened, and the rest were Europe-only. "
   "micro1 returned 68 roles; the new ones include an undergraduate talent network post, a consumer-security tester and a Europe-only agent tester, so none were shortlisted.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
