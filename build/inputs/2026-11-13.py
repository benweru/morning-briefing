# Builds data/runs/2026-11-13.json from the live search output plus hand-verified review notes.
import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-13.json'))
D = '2026-11-13'
WF_ERR = 'Not checked: automated fetch is disabled on purpose and the signed-in browser pass did not run today'
sh_sources = []
for name, s in live['sources'].items():
    err = s.get('error')
    if name == 'Wellfound': err = WF_ERR
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': s['kept'], 'error': err})
jobs = [
 dict(rank=1, tier='top', url='https://himalayas.app/companies/workster-jobs/jobs/ai-llm-engineer-remote-in-emea',
      title='AI LLM Engineer - Remote in EMEA', company='Workster Jobs (recruiter; client not named)',
      location_as_stated='"Remote opportunity for candidates based in the EMEA region"', posted='2026-11-12',
      salary_as_shown='Not shown', experience_asked='Professional experience in software engineering or ML; no years stated (Himalayas tags it Mid-level)',
      found_via='Himalayas API', verified=f'Himalayas API listing and full description, live {D} (himalayas.app pages return 403 to curl)',
      fit='LLM features, RAG, prompt and evaluation work plus backend APIs, which is the core of his current AI automation role.',
      gaps='A recruiter post with the client unnamed. Himalayas time-zone tags look wrong (UTC-10 to UTC-3), so confirm UTC+3 is fine before applying.'),
 dict(rank=2, tier='top', url='https://jobs.micro1.ai/post/14f2ea89-1bc3-4cdb-b43a-d26a8d755c00',
      title='Software Engineer', company='micro1',
      location_as_stated='No location restriction on the micro1 portal listing (collector label: Remote, global)', posted='2026-11-11',
      salary_as_shown='$50-$100/hour (micro1 portal)', experience_asked='Not stated on the portal listing',
      found_via='micro1 public job portal API', verified=f'micro1 portal API, live {D} (jobs.micro1.ai returns 403 to curl)',
      fit='Python and TypeScript bug fixing, feature work and refactoring, all in his day-to-day stack.',
      gaps='Hourly contract, not a salaried job. micro1 is still waiting on his AI interview (reminder sent Nov 12), so finish that first.'),
 dict(rank=3, tier='top', url='https://jobs.micro1.ai/post/e5a0105a-1535-4ea8-97ff-d6ff43441e42',
      title='Software Engineer - Backend', company='micro1',
      location_as_stated='Worldwide (Himalayas tag); no restriction on the micro1 portal listing', posted='2026-11-11',
      salary_as_shown='$50-$100/hour (micro1 portal)', experience_asked='Not stated on the portal listing',
      found_via='Himalayas API, confirmed on micro1 portal API', verified=f'micro1 portal API, live {D}',
      fit='Backend-leaning version of the same Python/TypeScript contract work; matches his API and backend experience.',
      gaps='Hourly contract; same micro1 AI interview applies. The skills list also names Java, Rust and C++, which he has not used professionally.'),
 dict(rank=4, tier='top', url='https://jobs.micro1.ai/post/f773a48d-1b5f-4bb6-8b56-a6d72f3fb9c5',
      title='Software Engineer - Open Source Contributions', company='micro1',
      location_as_stated='No location restriction on the micro1 portal listing (collector label: Remote, global)', posted='2026-11-10',
      salary_as_shown='$50-$100/hour (micro1 portal)', experience_asked='Not stated on the portal listing',
      found_via='micro1 public job portal API', verified=f'micro1 portal API, live {D}',
      fit='Open-source bug fixes and features in Python/TypeScript; his public GitHub projects are relevant evidence.',
      gaps='May overlap with the micro1 "Software Engineer (GitHub Contributor)" role he applied to on Oct 23; check before applying again.'),
 dict(rank=5, tier='stretch', url='https://jobgether.com/offer/6af5334b1b1a9ee7d669632b-mid-level-fullstack-engineer-typescript-node-react',
      title='Mid-level Fullstack Engineer (Typescript, Node, React)', company='SoSafe',
      location_as_stated='"Remote from: Portugal, Europe, European Union, EMEA" (Jobgether)', posted='2026-11-12',
      salary_as_shown='Not shown', experience_asked='Mid-level (2-5 years); "proven track record of professional full-stack development using Typescript + React"',
      found_via='Jobgether public API', verified=f'Jobgether offer page opened {D} via a reader (curl gets 403); SoSafe careers page not opened',
      fit='TypeScript, Node and React on an identity and access team, with AI-assisted tooling welcome; close to his React/TypeScript work.',
      gaps="Kenya isn't named; confirm before applying (the tags lean Europe/Portugal). Asks for 2-5 years against his roughly one, plus CI/CD and observability depth."),
 dict(rank=6, tier='stretch', url='https://jobs.micro1.ai/post/7fc07dfa-1d0e-4795-b8b2-805d3d41a48a',
      title='Junior Machine Learning Engineer', company='micro1',
      location_as_stated='Worldwide (Himalayas tag); no restriction on the micro1 portal listing', posted='2026-11-12',
      salary_as_shown='$60-$120/hour (micro1 portal)', experience_asked='Junior (title); not stated in years',
      found_via='Himalayas API, confirmed on micro1 portal API', verified=f'micro1 portal API, live {D}',
      fit='Junior-level ML contract; his data science certificate and LLM work give him a start.',
      gaps='ML engineering is beyond his main CV focus (applied LLM and automation); hourly contract; micro1 AI interview still pending.'),
 dict(rank=7, tier='evergreen', url='https://job-boards.greenhouse.io/canonical/jobs/6222476',
      title='Software Engineer - Python - Container Images', company='Canonical',
      location_as_stated='Home Based - Americas; Home Based - APAC; Home based - EMEA', 
      posted='Jobicy listed 2026-11-12 (Greenhouse req first published 2024-08-30, updated 2026-08-25)',
      salary_as_shown='Not shown', experience_asked='"Your skills range from those of a Graduate to a mid-senior Software Engineer"; Bachelor\'s in CS or similar',
      found_via='Jobicy API', verified=f'Greenhouse API, live {D}',
      fit='Graduate-friendly Python role building Ubuntu container images and CI/CD automation, open in EMEA.',
      gaps='Always-open listing. Asks for Docker/Kubernetes and Linux packaging depth. Canonical rejected his Graduate SWE application on Oct 14 and his Ubuntu SWE application from Oct 19 is still open.'),
]
def drop(url, title, company, loc, reason, code, **kw):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code)
    d.update(kw); return d
# micro1 Software Engineer / Backend / Open Source and Canonical Container Images match earlier
# applications or briefings by company+title (briefing_lib.already_surfaced), so they are not shown.
SURFACED_TITLES = {'Software Engineer', 'Software Engineer - Backend', 'Software Engineer - Open Source Contributions',
                   'Software Engineer - Python - Container Images'}
jobs = [j for j in jobs if j['title'] not in SURFACED_TITLES]
for i, j in enumerate(jobs, 1): j['rank'] = i
dropped = [
 drop('https://jobgether.com/offer/6af4c2ac1b1a9ee7d6673189-junior-ai-engineer','Junior AI Engineer','CENSUS',
      '"Location: Remote in Europe." "Europe-based candidates are prioritised."','Remote in Europe only; Kenya not eligible.','location',
      posted='2026-11-11', experience_asked='At least 1 year hands-on AI/ML, internships count', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af3712a1b1a9ee7d6606124-full-stack-engineer-backend-heavy','Full Stack Engineer (Backend Heavy)','QuantumLoopAi',
      '"Fully remote from India, aligned to UK business hours"','India-based only; 2-3 yrs Node/TypeScript.','location', posted='2026-11-10', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af37f361b1a9ee7d6609a7a-ai-solutions-engineer---agents-automation---north-macedonia','AI Solutions Engineer - Agents & Automation - North Macedonia','HeadQuarters',
      'Remote from: North Macedonia, Europe, EMEA','North Macedonia hire; 3+ yrs.','location', posted='2026-11-10', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af605f7081ddfee5002540b-remote-ai-engineer','Remote AI Engineer','Huzzle.com',
      'Remote from: North Macedonia, Europe, EMEA','North Macedonia hire; 3+ yrs.','location', posted='2026-11-12', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af63e2e081ddfee500348a6-jr-226156-azure-ai-foundry-engineer','JR-226156 Azure AI Foundry Engineer','Customertimes Corp',
      '"Remote (European and United States time zones)"','EU/US time zones; 2+ yrs Azure AI Foundry with an agent in production.','location', posted='2026-11-12', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af355021b1a9ee7d65fd180-full-stack-engineer','Full Stack Engineer','Feefo',
      'Remote from: United Kingdom, Europe, EMEA','UK-tagged; 3-5 yrs Java/Spring Boot.','location', posted='2026-11-10', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af3712a1b1a9ee7d6606112-backend-developer','Backend Developer','Pulse Games',
      'Remote from: Turkey, Asia, Middle East, EMEA','Turkey-tagged; 3 yrs with mobile game teams.','location', posted='2026-11-10', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af37f241b1a9ee7d6609635-full-stack-data-analyst','Full Stack Data Analyst','Fabulous',
      'Remote from: Tunisia, Africa, Northern Africa, EMEA','4+ yrs data science/analytics; Tunisia-tagged.','experience', posted='2026-11-10', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://www.linkedin.com/jobs/view/software-engineer-ai-tooling-at-jobgether-4489090730','Software Engineer - AI Tooling','Jobgether (for a partner company)',
      'Kenya; "work from anywhere in the world"','At least 5 years of professional software engineering.','experience', posted='2026-11-12', found_via='LinkedIn (Remote, Kenya search)', verified=f'LinkedIn guest job page, {D}'),
 drop('https://himalayas.app/companies/micro1/jobs/software-engineer-electron-js-5954044927','Software Engineer (Electron.js)','micro1',
      'Location: Remote','3+ yrs production Electron.js desktop apps.','experience', posted='2026-11-07', found_via='Himalayas API', verified=f'Himalayas API, {D}; not on the micro1 portal API'),
 drop('https://himalayas.app/companies/operationsarmy/jobs/accounting-ai-analyst-kenya-remote','Accounting AI Analyst | Kenya | Remote','OperationsArmy',
      'Kenya; shifts between 8:00 AM and 8:00 PM EST','AI data-labelling and accounting QA, not engineering; US-hours shifts.','other', posted='2026-11-10', found_via='Himalayas API', verified=f'Himalayas API, {D}'),
 drop('https://himalayas.app/companies/hivex/jobs/fullstack-developer-react-node-js-9559398791','FullStack Developer (react + node.js)','Hivex',
      'Worldwide (Himalayas tag)','He applied to Hivex\'s Junior+ Full Stack Developer role on Nov 2; likely the same opening.','other', posted='2026-11-01', found_via='Himalayas API'),
 drop('https://jobgether.com/offer/6af525041b1a9ee7d6691fb1-tech-generalist-software-engineer','Tech Generalist (Software Engineer)','Capchase',
      'Remote from: Estonia, Hungary, Bulgaria, Romania and other listed countries (Jobgether)','4+ yrs production TypeScript/Node; Kenya not in the country list.','experience', posted='2026-11-12', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://jobgether.com/offer/6af3e1c81b1a9ee7d6629308-software-engineer---database---bitnomial','Software Engineer - Database - Bitnomial','Kraken',
      'Remote from: Cyprus, United Arab Emirates, Lithuania and other listed countries (Jobgether)','3+ yrs with Haskell, Rust or C++.','experience', posted='2026-11-11', salary_as_shown='$96K - $192K / year', found_via='Jobgether public API', verified=f'Jobgether offer page, {D}'),
 drop('https://weworkremotely.com/remote-jobs/karat-software-engineer-interviewer','Software Engineer Interviewer','Karat',
      'Anywhere in the World; "we hire worldwide and rotate which countries we recruit in"','3+ yrs as a software engineer; task-paid contractor.','experience', posted='2026-11-06', found_via='We Work Remotely RSS', verified=f'We Work Remotely page, {D}'),
 drop('https://himalayas.app/companies/g2i-inc/jobs/backend-developer-g2i-talent-pool','Backend Developer - G2i Talent Pool','G2i Inc.',
      '"Eligibility may vary depending on your location"','A talent pool, not an opening; Kenya not confirmed.','location', posted='2026-11-06', found_via='Himalayas API', verified=f'Himalayas API, {D}'),
]
news = {'groups': [
 {'id': 'ai', 'stories': [
  dict(title='Google releases Gemini 4 Hydrogen for fast coding and agent work', summary='Rolling out across the Gemini API, AI Studio and the Gemini app; priced at $1.50 per million input tokens and $7.50 per million output tokens across a 1M-token context.', why='A cheaper, fast model aimed at the agent workflows he builds.', source='Google', date='2026-11-12', url='https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/'),
  dict(title='Salesforce open-sources SOV-Transcribe-1 speech model', summary='Open-weight ASR model with 4 billion active parameters (26 billion total), released on Hugging Face under Apache 2.0.', why='A self-hostable transcription option for voice-agent and automation projects.', source='Hugging Face blog', date='2026-11-12', url='https://huggingface.co/blog/salesforce-sovereign-intelligence/sov-transcribe-1'),
  dict(title='Perplexity releases Decider v1.3 classification models', summary='Decider and Decider Flash v1.3 add exact text-span extraction and Apache-2.0 weights; Perplexity reports 91.6% mean accuracy across 63 query-classification tasks.', why='Routing and classification models like this are building blocks for agent pipelines.', source='Unite.AI', date='2026-11-12', url='https://www.unite.ai/perplexity-releases-decider-v1-3-models-with-text-span-extraction/'),
 ]},
 {'id': 'startups', 'stories': [
  dict(title='Kindo raises $30M to manage enterprise AI agents', summary='Crosspoint Capital and Forgepoint Capital co-led the round, bringing total funding to $57.6 million; revenue grew about 800% year over year in 2026.', why='Agent governance is a growing hiring area next to his automation work.', source='PR Newswire', date='2026-11-12', url='https://www.prnewswire.com/news-releases/kindo-secures-57-6-million-to-expand-enterprise-control-over-ai-agent-actions-and-reduce-costs-302937058.html'),
  dict(title='Rox raises $100M at a $1.3B valuation for sales AI agents', summary='Series B co-led by General Catalyst and March Capital, part of a day that also saw Fractile raise $720 million.', why='Well-funded agent startups are the ones likely to hire automation engineers.', source='Tech Startups', date='2026-11-12', url='https://techstartups.com/2026/11/12/startup-funding-news-today-november-12-2026-fractile-uforce-agile-robots-imprint-more/'),
  dict(title='Axle raises $9M to add AI agents to investment-bank software', summary='Eniac and Bonfire Ventures led the round; the money goes into AI agents for corporate-access teams.', why='Another early-stage agent company building in finance, close to his fintech background.', source='The Next Web', date='2026-11-12', url='https://thenextweb.com/news/axle-9m-ai-agents-investment-banks-corporate-access'),
  dict(title="Huang's exit tests Nvidia's African AI bet", summary="Jensen Huang resigned as Nvidia CEO; partner Cassava's rollout could cost up to $720 million for 12,000 GPUs, with Kenya part of the expansion plan.", why='Local GPU capacity in Kenya would shape AI jobs and tools in Nairobi.', source='TechCabal', date='2026-11-12', url='https://techcabal.com/2026/11/12/jensen-huang-exit-puts-nvidia-africa-test/'),
 ]},
 {'id': 'hiring', 'stories': [
  dict(title='Indeed: US tech job postings up from a year ago in Q3', summary='Overall US postings rose 3.1% year over year to October 23; every tech category is up, led by software development, and software wage growth hit 2.9% in September.', why='A modest recovery in tech hiring, though still below early-2020 levels.', source='Indeed Hiring Lab', date='2026-11-12', url='https://hiringlab.indeed.com/2026/11/12/2026-q3-us-tech-labor-market-update/'),
 ]},
 {'id': 'kenya', 'stories': [
  dict(title='Airtel Money opens wallet-to-bank transfers via PesaLink', summary='Through a partnership with IPSL, Airtel Money users can send money to accounts at 30 banks, Saccos and microfinance institutions.', why='More interoperability in Kenyan payments, the space his fintech work touches.', source='Business Daily', date='2026-11-11', url='https://www.businessdailyafrica.com/bd/markets/currencies/airtel-money-mobile-to-bank-transfers-open-via-pesalink-5667226'),
  dict(title='Treasury proposes seizing unclaimed crypto and stablecoins', summary='Idle digital assets would join shares and bank accounts that the Unclaimed Financial Assets Authority can take over.', why='Signals how Kenya plans to regulate digital assets held by fintech users.', source='Business Daily', date='2026-11-12', url='https://www.businessdailyafrica.com/bd/economy/treasury-seeks-to-seize-idle-cryptos-5668938'),
  dict(title='Kenya opens SecureKE sovereign security operations centre at Konza', summary='KoTDA and Kenyan firm SecureKE set up the SOC about 65 km southeast of Nairobi to serve government and private organisations.', why='New local security work and demand for engineers who can automate monitoring.', source='TechCabal', date='2026-11-12', url='https://techcabal.com/2026/11/12/%f0%9f%91%a8%f0%9f%8f%bf%f0%9f%9a%80techcabal-daily-ghanas-big-5g-promise/'),
 ]},
]}
dr = live['dropped']
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-13T10:20:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Greenhouse API (Canonical recheck)', 'MyJobMag and LinkedIn (via Local Search Bot)'],
             'news': ['Google', 'Hugging Face blog', 'Unite.AI', 'PR Newswire', 'Tech Startups', 'The Next Web', 'TechCabal', 'Indeed Hiring Lab', 'Business Daily']},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': len(jobs), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, "
      f"{dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. Of the closely reviewed roles, three micro1 Software Engineer contracts and Canonical's Python Container Images role were left off because they match roles he has already applied to or seen. "
      "Most Jobgether leads were Europe-only once the posting was opened. Wellfound was not checked (it needs the signed-in browser pass) and ReliefWeb failed with a parse error. "
      "Jobicy's dates look like bump dates, so its listings were rechecked at the source.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped', sum(len(g['stories']) for g in news['groups']), 'stories')
