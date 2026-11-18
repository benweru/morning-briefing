# Builds data/runs/2026-11-18.json from the live search output plus hand-verified review notes.
import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-18.json'))
D = '2026-11-18'
dr = live['dropped']
final_kept = {'Greenhouse': 1, 'micro1': 3}
sh_sources = []
for name, s in live['sources'].items():
    err = s.get('error')
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'],
                       'kept': final_kept.get(name, 0), 'error': err})
# Signed-in browser pass replaced the failed automated fetch (~7:44 AM EAT).
for x in sh_sources:
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 85, 85, 1, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 482, 'fresh': 7, 'kept': 7, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 25, 'fresh': 4, 'kept': 4, 'error': None})

MICRO1_VER = f'micro1 public job-portal API (prod-api.micro1.ai) lists it and the jobs.micro1.ai post page returns HTTP 200, live {D}'
# One-day exemption: these four URLs are new, but company+title matches earlier
# applications or briefings. listed on the run as surfaced_exemptions so today's
# publish keeps them; the shared filter is unchanged for days without the field.
EXEMPT_URLS = [
    'https://job-boards.greenhouse.io/canonical/jobs/8379825',
    'https://jobs.micro1.ai/post/e5a0105a-1535-4ea8-97ff-d6ff43441e42',
    'https://jobs.micro1.ai/post/14f2ea89-1bc3-4cdb-b43a-d26a8d755c00',
    'https://jobs.micro1.ai/post/cf351411-3ea6-400b-ae57-369d9b2884c5',
]

jobs = [
 dict(rank=1, tier='top',
      url='https://wellfound.com/jobs/5085687-full-stack-engineer-new-grad',
      title='Full Stack Engineer (New Grad)', company='Yara',
      location_as_stated='"Onsite or remote"; "Hires remotely in Everywhere"; job location New York City and San Francisco (Wellfound)',
      posted='2026-11-17',
      salary_as_shown='$100k-$180k',
      experience_asked='No years required. Wellfound says it is for people graduating this year or who finished within the last 18 months. A CS degree, a bootcamp with real projects, or a body of work is accepted; it asks for working TypeScript, Python or Go, something deployed and maintained, and LLM-powered side projects that go past a chat wrapper (tool-calling, agents, evals). Visa sponsorship is not available.',
      found_via='Signed-in Wellfound browser pass',
      verified=f'Wellfound posting opened via signed-in browser pass and r.jina.ai reader, live {D}; Wellfound showed "Posted: 1 day ago" (wellfound.com returns 403 to curl)',
      fit='A remote-everywhere, full-time new-grad full-stack role with TypeScript or Python and LLM or agent side projects, which matches his CS degree (August 2026, within the 18-month window) and his stack. Salary is shown.',
      gaps='This is a Yara Network application: one application is matched across partner companies, not a role at Yara itself. Visa sponsorship is not available. It is listed as onsite or remote in New York City and San Francisco, while also hiring remotely Everywhere. Interviews may include a one- or two-day work trial.'),
 dict(rank=2, tier='top',
      url='https://job-boards.greenhouse.io/canonical/jobs/8379825',
      title='Graduate Software Engineer, Open Source and Linux, Canonical Ubuntu', company='Canonical',
      location_as_stated='"Home based - Worldwide" (Greenhouse). "This is a Globally remote role."',
      posted='2026-11-16',
      salary_as_shown='Not shown',
      experience_asked='Graduate role for the 2026 and 2027 intakes. Asks for an undergraduate degree in Computer Science or another STEM discipline, an exceptional academic track record from high school and university, confidence in one of Python, Rust, C/C++, Golang, JavaScript or Java, experience with Ubuntu or another Linux distribution, personal projects beyond the curriculum, and the ability to travel internationally twice a year for company events of up to two weeks.',
      found_via='Greenhouse API (Canonical board)',
      verified=f'Greenhouse job API and job-board page (HTTP 200), live {D}; first published 2026-11-16',
      fit='A worldwide-remote graduate engineering programme that suits a recent CS graduate with Python and JavaScript experience and personal projects.',
      gaps='Possibly a repost of the Canonical graduate role that turned Ben down on 14 Oct; published 16 Nov. The bar is explicit: an exceptional academic record and a competitive process. He also applied to a different Ubuntu Software Engineer posting on 19 October.'),
 dict(rank=3, tier='top',
      url='https://jobs.micro1.ai/post/e5a0105a-1535-4ea8-97ff-d6ff43441e42',
      title='Software Engineer - Backend', company='micro1',
      location_as_stated='"Remote (global)" (micro1 job-portal listing)',
      posted='2026-11-11',
      salary_as_shown='$50-$100 per hour (micro1 portal)',
      experience_asked='No years shown. Skills listed: Python3, Java, Rust, algorithms, basic C++, TypeScript, bug fixing, feature implementation, codebase refactoring and performance optimization.',
      found_via='micro1 job-portal API (priority source)',
      verified=MICRO1_VER,
      fit='A remote backend contract with hourly pay shown and a Python and TypeScript skills list that matches his CV.',
      gaps='It is a contract paid hourly, not a salary, and micro1 screens with an AI interview. The skills list also names Java, Rust and C++, which are outside his CV. He applied to similar micro1 software engineer roles on 22 and 23 October.'),
 dict(rank=4, tier='top',
      url='https://jobs.micro1.ai/post/14f2ea89-1bc3-4cdb-b43a-d26a8d755c00',
      title='Software Engineer', company='micro1',
      location_as_stated='"Remote (global)" (micro1 job-portal listing)',
      posted='2026-11-11',
      salary_as_shown='$50-$100 per hour (micro1 portal)',
      experience_asked='No years shown. Same skills list as the Backend listing: Python3, Java, Rust, algorithms, basic C++, TypeScript, bug fixing, feature implementation, codebase refactoring and performance optimization.',
      found_via='micro1 job-portal API (priority source)',
      verified=MICRO1_VER,
      fit='A general remote software engineering contract with hourly pay shown and Python and TypeScript in the skills list.',
      gaps='Hourly contract with an AI interview, and the same Java, Rust and C++ skills as the Backend listing. It looks like a sibling of the Backend post, so one application may be enough.'),
 dict(rank=5, tier='top',
      url='https://jobs.micro1.ai/post/cf351411-3ea6-400b-ae57-369d9b2884c5',
      title='ML Engineer', company='micro1',
      location_as_stated='"Remote (global)" (micro1 job-portal listing)',
      posted='2026-11-16',
      salary_as_shown='$60-$120 per hour (micro1 portal)',
      experience_asked='No years shown. The only skill listed is Machine Learning; the listing is tagged AI / machine learning.',
      found_via='micro1 job-portal API (priority source)',
      verified=MICRO1_VER,
      fit='A remote ML engineering contract with the highest hourly range of the micro1 roles, close to his LLM and PyTorch work.',
      gaps='The listing gives almost no detail, so the real bar is unknown. It is an hourly contract with an AI interview, and he applied to micro1 Junior Machine Learning Engineer on 13 November.'),
]

def drop(url, title, company, loc, reason, code, **kw):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code)
    d.update(kw); return d

dropped = [
 drop('https://arc.dev/remote-jobs/j/q06ri678ca', 'Freelance Developer WW-PT', 'Not shown (Arc listing)',
      'Worldwide (Arc.dev collector label)',
      'The Arc job URL redirected to the generic remote-jobs index, so the posting could not be confirmed as open.',
      'closed', posted='2026-11-17', found_via='Arc.dev', verified=f'arc.dev job URL redirected to /remote-jobs, {D}'),
 drop('https://jobs.micro1.ai/post/8dd58c0e-78c8-44b4-a8e3-0bfbfc1f765f', 'Machine Learning Researcher', 'micro1',
      '"Remote (global)" (micro1 job-portal listing)',
      'Specialist research role ($60-$120 per hour, skill listed: Machine Learning), not a junior engineering role.',
      'experience', posted='2026-11-16', salary_as_shown='$60-$120 per hour (micro1 portal)', found_via='micro1 job-portal API',
      verified=f'micro1 job-portal API, live {D}'),
 drop('https://jobs.micro1.ai/post/f65f4c3c-34b6-48bd-96bd-5f274f7dcd09', 'Applied Scientists - Machine Learning', 'micro1',
      '"Remote (global)" (micro1 job-portal listing)',
      'Specialist applied-science role ($60-$120 per hour), not a junior engineering role.',
      'experience', posted='2026-11-16', salary_as_shown='$60-$120 per hour (micro1 portal)', found_via='micro1 job-portal API',
      verified=f'micro1 job-portal API, live {D}'),
 drop('https://jobs.micro1.ai/post/d4080820-66c9-48b1-a29a-b8b1752b8e79', 'AI Agent Tester', 'micro1',
      '"Remote (global)" (micro1 job-portal listing)',
      'Generalist testing task ($25-$45 per hour; skills: ChatGPT, screen recording, attention to detail), not an engineering role.',
      'stack', posted='2026-11-16', salary_as_shown='$25-$45 per hour (micro1 portal)', found_via='micro1 job-portal API',
      verified=f'micro1 job-portal API, live {D}'),
 drop('https://jobgether.com/offer/6afd0e0b8acd9c1f9b22e409-software-engineer', 'Software Engineer', 'SingleStore',
      'Europe, European Union, EMEA, Portugal (Jobgether)', 'Portugal-based role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-18', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afd0dfa8acd9c1f9b22e016-mid-level-web-developer-luxury-brands', 'Mid-Level Web Developer | Luxury Brands', 'Talent Shore',
      'Africa, Sub-Saharan Africa, EMEA, South Africa (Jobgether)', 'Jobgether level is Mid-level (2-5 years) and the tags point to South Africa; Kenya is not named.',
      'experience', posted='2026-11-18', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afc81428acd9c1f9b1f96ed-software-engineer-mid-1', "Software Engineer Mid 1", "Nando's UK & IRE",
      'Europe, EMEA, United Kingdom (Jobgether)', 'UK and Ireland role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afbf4e78acd9c1f9b1d2264-junior-software-qa-engineer--etr--serbia', 'Junior Software QA Engineer- ETR- Serbia', 'Cisco',
      'Europe, EMEA, Serbia (Jobgether)', 'Serbia-based QA role; Kenya is not named.',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afcd5b58acd9c1f9b219c47-data-ai-product-engineer', 'Data & AI Product Engineer', 'AMS SOLUTIONS',
      'Europe, European Union, EMEA, Spain (Jobgether)', 'Spain-based role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afcd5b58acd9c1f9b219bed-ai-forward-deployment-engineer', 'AI Forward Deployment Engineer', 'Sphera',
      'Europe, Asia, European Union, South Asia, EMEA, APAC, Poland, India (Jobgether)', 'Poland and India country list without Kenya. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afc3b028acd9c1f9b1e13ef-ai-engineer', 'Ai Engineer', 'ITCAN Technology and Digital Marketing',
      'Asia, Middle East, EMEA, APAC, United Arab Emirates (Jobgether)', 'UAE-based role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afc2cf28acd9c1f9b1e0577-ai-engineer', 'Ai Engineer', 'MoonTech',
      'Asia, Middle East, EMEA, APAC, United Arab Emirates (Jobgether)', 'UAE-based role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-17', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://jobgether.com/offer/6afadb5c8acd9c1f9b18024f-software-engineer---application-api-protection', 'Software Engineer - Application & API Protection', 'Akamai Technologies',
      'Asia, Middle East, EMEA, APAC, Israel (Jobgether)', 'Israel-based role; Kenya is not named. Jobgether level: Mid-level (2-5 years).',
      'location', posted='2026-11-16', found_via='Jobgether public API', verified=f'Jobgether API listing, {D}'),
 drop('https://www.linkedin.com/jobs/view/security-software-engineer-%2420-hr-remote-at-crossing-hurdles-4489554239', 'Security Software Engineer | $20/hr Remote', 'Crossing Hurdles',
      'Remote, Kenya (LinkedIn)', 'The posting asks for 5+ years of professional software engineering and expert-level security skills (CWE, CVE); it is an AI-trainer contract at $20 per hour.',
      'experience', posted='2026-11-13', salary_as_shown='$20.00/hr (LinkedIn)', experience_asked='5+ years of professional software engineering experience',
      found_via='LinkedIn (remote, Kenya)', verified=f'LinkedIn public job page opened, {D}'),
 drop('https://www.linkedin.com/jobs/view/qa-engineer-at-sitemate-4491515141', 'QA Engineer', 'Sitemate',
      'Remote, Kenya (LinkedIn)', 'QA-only role, outside the software, backend, full-stack or AI targets.',
      'stack', posted='2026-11-16', found_via='LinkedIn (remote, Kenya)', verified=f'LinkedIn listing in live search, {D}'),
 drop('https://www.linkedin.com/jobs/view/request-for-proposal-agentic-ai-system-partner-discovery-design-build-and-handover-for-wazzii-at-girl-effect-4489760627',
      'Request for Proposal: Agentic AI System Partner (WAZZII)', 'Girl Effect',
      'Remote, Kenya (LinkedIn)', 'A request for proposals aimed at partner organisations, not a job for an individual.',
      'other', posted='2026-11-16', found_via='LinkedIn (remote, Kenya)', verified=f'LinkedIn listing in live search, {D}'),
 drop('https://www.linkedin.com/jobs/view/crop-forecasting-data-analyst-at-sotik-group-4489094400', 'Crop Forecasting & Data Analyst', 'Sotik Group',
      'Remote, Sotik, Bomet, Kenya (LinkedIn)', 'Crop-forecasting data analyst role based around Sotik, not a software or AI engineering target.',
      'stack', posted='2026-11-12', found_via='LinkedIn (remote, Kenya)', verified=f'LinkedIn listing in live search, {D}'),
]

news = {'groups': [
 {'id': 'ai', 'stories': [
  dict(title='Vercel releases eve 1.0, an open-source framework for production agents',
       summary='On 17 November Vercel announced eve 1.0 as generally available after a June public preview, with 230+ releases since, approval controls for agent actions, and an open-source Workflow SDK that lets an agent resume from its last completed step after a crash.',
       why='He builds agent and automation workflows, and durable execution plus approval controls are the production concerns he runs into.',
       source='Vercel', date='2026-11-17', url='https://vercel.com/blog/eve-is-now-generally-available'),
  dict(title='Microsoft launches Copilot SDK 2.0 for building agents',
       summary='On 17 November, at Ignite, Microsoft announced the Microsoft Copilot SDK (previously the GitHub Copilot SDK), with a runtime that hosts many isolated sessions in one process, available in TypeScript, Python, Go, .NET, Java and Rust.',
       why='A TypeScript and Python SDK for building agents is directly usable with his stack.',
       source='Microsoft Command Line', date='2026-11-17', url='https://commandline.microsoft.com/microsoft-copilot-sdk-2-0-github/'),
  dict(title='Replit launches Missions, coordinated agent swarms for large goals',
       summary='On 17 November Replit said Missions lets a team define an outcome and budget while a swarm of agents plans, builds, tests and iterates; Replit says it built an in-house monitoring platform in 2 days within a $3,000 budget.',
       why='It shows where agentic coding tools are heading, and Replit states the budget and boundaries are set by the user.',
       source='Replit', date='2026-11-17', url='https://replit.com/blog/introducing-replit-missions'),
  dict(title='MBZUAI releases six fully open K2-Horizon models from 0.9B to 375B',
       summary='On 17 November AI Weekly reported that MBZUAI released K2-Horizon, six models from a 0.9B dense network to a 375B-A23B mixture-of-experts flagship, with intermediate checkpoints and data pipelines; the 375B and 36B models currently ship weights only.',
       why='Small open-weight models in GGUF and MLX formats are easy to run locally for the kind of LLM prototyping on his CV.',
       source='AI Weekly', date='2026-11-17', url='https://aiweekly.co/alerts/mbzuai-opens-k2-horizon-fleet-six-models-from-09b-to-375b'),
 ]},
 {'id': 'startups', 'stories': [
  dict(title='PROTEGEY raises pre-seed for a shared fraud intelligence network across Africa',
       summary='On 17 November African-Startups reported that PROTEGEY raised pre-seed funding from LvlUp Ventures and angel investors; it did not disclose the amount, valuation or first markets.',
       why='An early-stage African fintech building AI-based fraud and compliance tooling is the kind of company that hires API and integration engineers.',
       source='African-Startups', date='2026-11-17', url='https://african-startups.com/news/funding/protegey-raises-pre-seed-funding-to-build-shared-fraud-intelligence-network-across-africa/'),
  dict(title='Sudanese fintech Cashi raises $660k from Proparco',
       summary='On 17 November Disrupt Africa reported that Cashi raised US$660,000 from Proparco, its first investment in Sudan; the MyCashi wallet has 2.2 million registered users.',
       why='Another African payments company building around cash-heavy markets, which is context for fintech work.',
       source='Disrupt Africa', date='2026-11-17', url='https://disruptafrica.com/2026/11/17/sudanese-fintech-startup-cashi-raises-660k-from-proparco/'),
  dict(title='Nigeria-based Khaime raises $500,000 pre-seed for AI-agent commerce',
       summary='On 17 November Launch Base Africa listed Khaime among its deals: a $500,000 pre-seed led by Launch Africa Ventures for an agent-first commerce platform with an AI agent that handles chats and turns conversations into orders.',
       why='A funded African startup built around AI agents and chat channels such as WhatsApp, close to his automation work.',
       source='Launch Base Africa', date='2026-11-17', url='https://launchbaseafrica.com/2026/11/17/african-startup-deal-tracker-newest-deals-25/'),
 ]},
 {'id': 'kenya', 'stories': [
  dict(title='Payaza gets CBK authorisation to operate as a payment service provider in Kenya',
       summary='On 17 November Tuko reported that Payaza received Central Bank of Kenya authorisation as a payment service provider; the Nairametrics report says it covers gateway services such as card, mobile money and bank payments but not wallets or holding customer funds.',
       why='A new licensed payment gateway entering Kenya adds competition and possibly integration work in the payments space he knows.',
       source='Tuko', date='2026-11-17', url='https://www.tuko.co.ke/business-economy/capital-market/647002-payaza-enters-kenyas-digital-payments-market-securing-cbk-licence/'),
  dict(title="Kenya's payments rules are under review as new providers enter",
       summary='On 17 November The Standard Business, via The Online Kenyan, reported that M-PESA processed 46.41 billion transactions worth Sh41.68 trillion in the year to March 2026 and that the draft National Payment System Bill, 2026 aims to promote interoperability, competition and consumer protection.',
       why='The proposed bill could change licensing for the payment providers he may work for or integrate with.',
       source='The Online Kenyan (The Standard)', date='2026-11-17', url='https://www.theonlinekenyan.com/read/story/685922'),
 ]},
]}

feed_jobs = [
 dict(title='Forensic Technology & Data Analyst', company='Onfon Media', location='Nairobi', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/forensic-technology-data-analyst-onfon-media-ltd',
      posted='2026-11-14', deadline='2026-11-20', salary_as_shown='Not shown',
      fit_note='On-site fraud-detection data analytics role using queries, analytical models and AI-assisted tools. Different role from the Onfon DevOps, L3 Support and Forensic Investigations Assistant roles he applied to.',
      already_applied=False),
 dict(title='Business Applications Developer', company='Valley Hospital', location='Nakuru', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/business-applications-developer-valley-hospital-55b9babf',
      posted='2026-11-17', deadline='2026-11-24', salary_as_shown='Not shown',
      fit_note='On-site in Nakuru. Python, JavaScript, SQL, Odoo, PostgreSQL or MySQL, REST APIs and clinical and payer integrations.',
      already_applied=False),
 dict(title='Data Analyst', company='African Management Institute', location='Nairobi', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/data-analyst-african-management-institute-749ef05a-aa6f-4627-a441-4bd16354cde2-6d5a7153',
      posted='2026-11-16', deadline='2026-11-23', salary_as_shown='Not shown',
      fit_note='Data preparation, dashboards and reports for programme and commercial teams; Fuzu lists the same role twice.',
      already_applied=False,
      also_on=[dict(source='Fuzu', url='https://www.fuzu.com/kenya/jobs/data-analyst-african-management-institute-749ef05a-aa6f-4627-a441-4bd16354cde2-2e4651bc',
                    company='African Management Institute', posted='2026-11-17', deadline='2026-11-24')]),
 dict(title='APIOps Analyst', company='NCBA', location='Nairobi', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/apiops-analyst-ncba-88ce9caf',
      posted='2026-11-17', deadline='2026-11-22', salary_as_shown='Not shown',
      fit_note='On-site role supporting deployment, monitoring and maintenance of API services at a bank, close to his API and fintech work. Deadline is 4 days away.',
      already_applied=False),
 dict(title='QA Specialist, Web Applications and Integration', company='Kinnovarone', location='Remote, open to applicants in Kenya', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/qa-specialist-kinnovarone',
      posted='2026-11-17', deadline='2026-12-30', salary_as_shown='Not shown',
      fit_note='Remote full-time QA role testing web applications and API integrations; applies on the employer site.',
      already_applied=False),
 dict(title='QA Engineer (Manual & Automation)', company='Onfon Media', location='Nairobi', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/qa-engineer-manual-automation-onfon-media-ltd',
      posted='2026-11-14', deadline='2026-11-20', salary_as_shown='Not shown',
      fit_note='On-site QA role (functional, integration and regression testing).',
      already_applied=False),
 dict(title='Intern Data Analytics', company='UN-Habitat', location='Nairobi', source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/intern-data-analytics-un-habitat-aeab8b46',
      posted='2026-11-13', deadline='2026-11-25', salary_as_shown='Not shown',
      fit_note='Same UN-Habitat internship Ben skipped on 16 November.', already_applied=True),
 dict(title='Associate Programmer Graduate Training Programme', company='Tamu Group (Tera Carbon Kenya)', location='Nairobi', source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/associate-programmer-graduate-training-programme-tamu-group',
      posted='2026-11-13', salary_as_shown='Not shown',
      fit_note='0-2 years graduate training programme; applied 16 November.', already_applied=True),
 dict(title='ICT Officer II, Software Development', company='Digital Health Agency (DHA)', location='Nairobi', source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/ict-officer-ii-software-development-digital-health-agency-dha',
      posted='2026-11-11', deadline='2026-12-01', salary_as_shown='Not shown',
      fit_note='Applied 16 November.', already_applied=True),
 dict(title='IT Officer', company='Ignite Energy Access', location='Nairobi', source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/it-officer-ignite-energy-access',
      posted='2026-11-13', deadline='2026-11-27', salary_as_shown='Not shown',
      fit_note='Full-time IT officer role; first-line IT support.', already_applied=False),
 dict(title='Business Intelligence (BI) Analyst', company='Teleperformance Kenya', location='Nairobi', source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/business-intelligence-bi-analyst-teleperformance',
      posted='2026-11-13', salary_as_shown='Not shown',
      fit_note='Full-time, on-site BI analyst role; weak fit. No deadline shown (page says Expires: Not specified).', already_applied=False),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 25, 'pulled_is_approximate': True, 'kept': 4, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 482, 'pulled_is_approximate': True, 'kept': 7, 'signed_in': True, 'error': None},
}

run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-18T07:50:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + [
     'Fuzu (signed-in browser pass)',
     'MyJobMag personalised feed (signed-in browser pass)',
     'Wellfound (signed-in browser pass)',
     'Greenhouse API (Canonical recheck)',
     'micro1 portal API (recheck)',
     'MyJobMag and LinkedIn (via Local Search Bot)',
 ],
  'news': ['Vercel', 'Microsoft Command Line', 'Replit', 'AI Weekly', 'African-Startups', 'Disrupt Africa', 'Launch Base Africa', 'Tuko', 'The Online Kenyan']},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': len(jobs), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
     f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, "
     f"{dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
     "Himalayas failed with an IncompleteRead error and ReliefWeb failed with a parse error. "
     "A signed-in browser pass of Wellfound at about 7:44 AM EAT (remote-only, Worldwide; Wellfound hides jobs that are not Nairobi-eligible) pulled about 85 roles and kept 1 (Yara, Full Stack Engineer (New Grad)). Examples left out: Veilky (5+ years), GenX intern (unpaid, Germany students only), Lupira PERN intern (unpaid or unclear pay), and SeeClear (a task gig via micro1). "
     "Fuzu was checked in the signed-in browser (about 482 Kenya roles pulled, 7 kept). The MyJobMag personalised feed was checked in the signed-in browser (about 25 pulled, 4 kept). "
     "Canonical's new Graduate Software Engineer post is open worldwide on Greenhouse (first published 16 November). It is shown today under a one-day exemption from the company-and-title filter because the Greenhouse URL is new; it may be a repost of the graduate role that turned him down on 14 October. The micro1 portal lists three fitting engineering roles (Software Engineer - Backend, Software Engineer, ML Engineer), also shown today under a one-day exemption because the posting URLs are new; its Machine Learning Researcher, Applied Scientists and AI Agent Tester posts were dropped as research or non-engineering roles. "
     "Roles skipped by Ben's standing decisions (SoSafe, FlexiSAF, micro1 AI Safety, Ideactra, Nestify, Cursor, KDCI, Cellulant, SHMETER, Tana, Share, Scanwick, Heather) were left out. "
     "Most other Jobgether leads were Europe, UAE, Israel or South Africa only and mid-level (2-5 years). "
     "The remote shortlist is shorter than the usual 6-10 because few fresh, junior-to-mid roles both stayed open, clearly included Kenya, and had not already been shown. "
     "The Hiring market news group is left out: nothing verified was published in the last 48 hours. "
     "Feed roles that are not already in the Kenya jobs or the applied log are listed under From your feeds.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
 'surfaced_exemptions': EXEMPT_URLS,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped', sum(len(g['stories']) for g in news['groups']), 'stories')
