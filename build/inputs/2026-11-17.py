# Builds data/runs/2026-11-17.json from the live search output plus hand-verified review notes.
import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-17.json'))
D = '2026-11-17'
dr = live['dropped']
sh_sources = []
for name, s in live['sources'].items():
    err = s.get('error')
    ok = s['ok']
    pulled, fresh, kept = s['pulled'], s['fresh'], s['kept']
    if name == 'Wellfound':
        # Signed-in browser pass replaced the failed automated fetch.
        ok, pulled, fresh, kept, err = True, 19, 19, 1, None
    sh_sources.append({'name': name, 'ok': ok, 'pulled': pulled, 'fresh': fresh, 'kept': kept, 'error': err})
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 20, 'fresh': 1, 'kept': 1, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 25, 'fresh': 6, 'kept': 6, 'error': None})

jobs = [
 dict(rank=1, tier='top',
      url='https://wellfound.com/jobs/5086124-full-stack-typescript-developer',
      title='Full-stack TypeScript Developer', company='AnswerReel',
      location_as_stated='"Remote (Everywhere)"; "Hires remotely in Everywhere"; "Location: Remote, anywhere in the world." (Wellfound)',
      posted='2026-11-16',
      salary_as_shown='$30-$60 per hour',
      experience_asked='No years stated. Must have shipped production apps with Next.js and TypeScript, be comfortable writing SQL and Postgres functions (not just using an ORM), write clear pull requests, and work asynchronously from a written spec.',
      found_via='Signed-in Wellfound browser pass',
      verified=f'Wellfound posting opened via signed-in browser pass and r.jina.ai reader, live {D} (wellfound.com returns 403 to curl)',
      fit='A worldwide remote TypeScript, React and Postgres contract, close to his React, TypeScript and PostgreSQL work, with hourly pay shown.',
      gaps='It is a contractor role paid by agreed scope and hours, not a salary. It asks for shipped production Next.js apps and for writing Postgres functions, which goes beyond using an ORM.'),
 dict(rank=2, tier='top',
      url='https://flexisaf.zohorecruit.com/jobs/Careers/440366000015521201/AI-Engineering-Training-and-Internship-Program',
      title='AI Engineering Training and Internship Program', company='FlexiSAF Edusoft Limited',
      location_as_stated='"This is a remote position." (Zoho). Jobgether tags the offer as available from Africa, Sub-Saharan Africa, EMEA, Nigeria. Zoho country and city fields are empty. The posting is also open to "anyone interested in upskilling". SIWES or NYSC category interns are expected on-site for that placement.',
      posted='2026-11-12',
      salary_as_shown='Unpaid internship (no stipend)',
      experience_asked='Zoho lists work experience as 0-1 year. Requirements include strong Python, a basic understanding of LLMs and prompt engineering, familiarity with LangChain or willingness to learn quickly, APIs (REST, GraphQL), and familiarity with Java and Spring Boot. Applications now are for the January to April 2027 cohort.',
      found_via='Jobgether public API',
      verified=f'Zoho Recruit public Job_Openings API and career page, live {D}',
      fit='A remote, Africa-tagged programme in Python, LLMs, RAG, LangChain and APIs, which is close to his current AI and backend work.',
      gaps='It is an unpaid internship for the January to April 2027 cohort, with no stipend. It is a training programme rather than a paid engineering job, and it also asks for familiarity with Java and Spring Boot. SIWES and NYSC placements are on-site.'),
]

def drop(url, title, company, loc, reason, code, **kw):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code)
    d.update(kw); return d

dropped = [
 drop('https://bdx.wd1.myworkdayjobs.com/EXTERNAL_CAREER_SITE_GERMANY/job/DEU-Heidelberg---Tullastrasse/Junior-Software-Developer-AI---Digital-Solutions_R-560157-1',
      'Junior Software Developer AI & Digital Solutions', 'Becton, Dickinson and Company (listed on Jobgether as Summit)',
      'Workday: location "DEU Heidelberg - Tullastrasse", country Germany, career site EXTERNAL_CAREER_SITE_GERMANY, remoteType Remote, hiring organization "2520 Becton Dickinson Management GmbH & Co KG". The posting says "Primary Work Location DEU Heidelberg - Tullastrasse" and describes a culture of face-to-face collaboration. Jobgether described the offer as available from Europe, European Union, EMEA, Germany.',
      'Germany-based BD role on the Germany Workday career site, with a Heidelberg primary work location; Kenya is not named on the employer page.',
      'location', posted='2026-11-16',
      salary_as_shown='\u20ac53,200-\u20ac81,100 EUR Annual (Workday)',
      experience_asked='Early-career 6-month contract; foundational software skills, exposure to React and TypeScript or Python, APIs and AI-assisted development. No years stated.',
      found_via='Jobgether public API (Summit listing)',
      verified=f'Workday CXS API, live {D} (canApply true)'),
 drop('https://jobgether.com/offer/6afba0548acd9c1f9b1b496b-junior-software-developer-ai-digital-solutions',
      'Junior Software Developer AI & Digital Solutions', 'BD',
      'Europe, European Union, EMEA, Germany (Jobgether, from the live search)',
      'The Jobgether offer URL returned HTTP 410 on 17 November, so the listing could not be confirmed as open. The same BD role remains on Workday and was reviewed separately.',
      'closed', posted='2026-11-17',
      found_via='Jobgether public API', verified=f'Jobgether offer page returned 410, {D}'),
 drop('https://arc.dev/remote-jobs/j/pzxx6zf855',
      'Full-Stack Developer', 'Not shown (Arc listing)',
      'Worldwide (Arc.dev collector label)',
      'The Arc job URL redirected to the generic remote-jobs index, and https://arc.dev/api/jobs/pzxx6zf855 returned 404, so the posting could not be confirmed as open.',
      'closed', posted='2026-11-16',
      found_via='Arc.dev', verified=f'arc.dev job URL redirected to /remote-jobs and the job API returned 404, {D}'),
 drop('https://careers.twtspain.com/jobs/8747012-ai-engineer-generative-ai-llms-ai-agents-remoto',
      'AI Engineer \u2013 Generative AI / LLMs / AI Agents \u2013 Remoto', 'The Whiteam',
      'Teamtailor page: "IT \u00b7 Bilbao \u00b7 Completamente remoto". Jobgether: "the offer is available from: Europe, European Union, EMEA, Spain".',
      'Spain / Bilbao remote role; Kenya is not named. Also asks for at least 3 years in artificial intelligence.',
      'location', posted='2026-11-16',
      experience_asked='M\u00ednimo 3 a\u00f1os de experiencia en Inteligencia Artificial; experience with generative AI, LLMs and AI agents.',
      found_via='Jobgether public API', verified=f'Teamtailor posting opened {D}'),
 drop('https://flexisaf.zohorecruit.com/jobs/Careers/440366000015521164/AI-Native-Python-Programming-Internship',
      'AI-Native Python Programming Internship', 'FlexiSAF Edusoft Limited',
      '"This is a remote position." (Zoho). Jobgether tags Africa, Sub-Saharan Africa, EMEA, Nigeria. Also open to "anyone interested in upskilling".',
      'Unpaid beginner-to-advanced Python training internship for the January to April 2027 cohort, at the same employer as the AI Engineering programme that was shortlisted.',
      'other', posted='2026-11-12',
      salary_as_shown='Unpaid internship (no stipend, except Youth Corp Members)',
      experience_asked='Zoho lists work experience as Fresher. Open to SIWES, NYSC, post-NYSC, students, or anyone upskilling.',
      found_via='Jobgether public API', verified=f'Zoho Recruit public Job_Openings API and career page, live {D}'),
 drop('https://flexisaf.zohorecruit.com/jobs/Careers/440366000015521110/AI-Native-Backend-Development-Intern',
      'AI Native Backend Development Intern', 'FlexiSAF Edusoft Limited',
      '"This is a remote position." (Zoho). Jobgether tags Africa, Sub-Saharan Africa, EMEA, Nigeria.',
      'Unpaid training internship focused on Java and Spring/Quarkus backends for the January to April 2027 cohort, not a paid engineering role.',
      'other', posted='2026-11-12',
      salary_as_shown='Unpaid internship (no stipend, except Youth Corp Members)',
      experience_asked='Zoho lists work experience as Fresher. Basic working knowledge of Java; Spring, Flyway and Quarkus are not mandatory for beginners.',
      found_via='Jobgether public API', verified=f'Zoho Recruit public Job_Openings API and career page, live {D}'),
 drop('https://flexisaf.zohorecruit.com/jobs/Careers/440366000015521072/AI-Native-Frontend-Development-Intern',
      'AI Native Frontend Development Intern', 'FlexiSAF Edusoft Limited',
      '"This is a remote position." (Zoho). Jobgether tags Africa, Sub-Saharan Africa, EMEA, Nigeria.',
      'Unpaid beginner frontend training internship (HTML, CSS, JavaScript; React not mandatory) for the January to April 2027 cohort, not a paid engineering role.',
      'other', posted='2026-11-12',
      salary_as_shown='Unpaid internship (no stipend, except Youth Corp Members)',
      experience_asked='Zoho lists work experience as Fresher.',
      found_via='Jobgether public API', verified=f'Zoho Recruit public Job_Openings API and career page, live {D}'),
 drop('https://job-boards.greenhouse.io/qualio/jobs/8204705003',
      'Full Stack Engineer (Remote Ireland)', 'Qualio',
      'Greenhouse location "Ireland"; office "EU". The team is "all-remote, and currently distributed across North America, Europe and Australia."',
      'Ireland / EU remote hire; Kenya is not in the team footprint. Also asks for 3+ years of professional software development.',
      'location', posted='2026-11-16',
      experience_asked='3+ years of professional software development experience; Python, Node.js, RDBMS and NoSQL, AWS.',
      found_via='Jobgether public API', verified=f'Greenhouse job-board API, live {D}'),
 drop('https://careers.twtspain.com/jobs/8745939-technical-analyst-python-ia-100-remoto-espana-sector-bancario',
      'Technical Analyst Python + IA - 100% Remoto (Espa\u00f1a) - Sector bancario', 'The Whiteam',
      'Teamtailor page: "IT \u00b7 Espa\u00f1a \u00b7 Completamente remoto". Jobgether: "the offer is available from: Europe, European Union, EMEA, Spain".',
      'Spain-only remote role; Kenya is not named. Also asks for at least 3 years in similar roles.',
      'location', posted='2026-11-16',
      experience_asked='Al menos 3 a\u00f1os de experiencia en funciones similares; Python and AI integration, with agents, MCPs and LangGraph valued.',
      found_via='Jobgether public API', verified=f'Teamtailor posting opened {D}'),
]

news = {'groups': [
 {'id': 'ai', 'stories': [
  dict(title='OpenAI begins embedded assessments with four independent labs',
       summary='On 16 November OpenAI said it had signed agreements with Apollo Research, METR, Transluce and Goodfire for its first phase of embedded assessments, giving them deep access to internal models and systems to review alignment and safeguards.',
       why='Independent safety evaluations of frontier models are becoming a formal part of how labs work, which matters if he keeps building with those platforms.',
       source='OpenAI', date='2026-11-16',
       url='https://openai.com/index/our-first-phase-of-embedded-assessments'),
  dict(title='Hugging Face routes language-model inference through OpenRouter',
       summary='On 16 November Hugging Face said Inference Providers now send language-model requests through OpenRouter, which picks a provider by live price, speed and reliability and retries on failure, with no change to existing Hugging Face tokens or code.',
       why='He already works with LLM APIs and agents, so a single Hugging Face token that can route open-weight models across providers is a practical tooling change.',
       source='Hugging Face blog', date='2026-11-16',
       url='https://huggingface.co/blog/openrouter'),
  dict(title='OpenAI expands free ChatGPT access for academic researchers',
       summary='On 16 November OpenAI said it is expanding ChatGPT for Academic Researchers toward 200,000 researchers worldwide, with applications for 50,000 new ChatGPT Plus grants opening on 23 November, each covering the recipient and up to two collaborators.',
       why='The programme is a reminder of how widely Plus-tier model access is being distributed to research teams, including possible collaborators.',
       source='OpenAI', date='2026-11-16',
       url='https://openai.com/index/expanding-chatgpt-for-academic-researchers/'),
 ]},
 {'id': 'startups', 'stories': [
  dict(title='Corma raises $125 million Series A at a $1 billion valuation',
       summary='On 16 November TechCrunch reported that cybersecurity AI startup Corma raised a $125 million Series A at a $1 billion valuation led by NEA, three months after launch, bringing total funding to $185 million including Sequoia Capital, Khosla Ventures and Coatue.',
       why='Fast-growing AI-agent companies in security are still raising large rounds, which is the kind of firm that later hires automation and backend engineers.',
       source='TechCrunch', date='2026-11-16',
       url='https://techcrunch.com/2026/11/16/cybersecurity-ai-startup-corma-reaches-1b-valuation-in-about-3-months/'),
  dict(title='Yoco secures a $100 million credit facility for merchant cash advances',
       summary='On 16 November Disrupt Africa reported that South African fintech Yoco secured a US$100 million credit facility from Victory Park Capital to scale merchant cash advances, after advancing more than ZAR6.5 billion (US$395 million) to over 40,000 merchants since 2018.',
       why='African payments and merchant-credit platforms are still raising growth capital, which is close to the fintech work he already does.',
       source='Disrupt Africa', date='2026-11-16',
       url='https://disruptafrica.com/2026/11/16/sas-yoco-secures-100m-credit-facility-to-scale-merchant-cash-advances/'),
  dict(title='Kenyan startup Farmerlifeline wins a $50,000 Innovate Africa grant',
       summary='On 16 November Tech In Africa reported that Farmerlifeline Technologies, a Kenyan agritech startup, won the third Innovate Africa Challenge and a $50,000 implementation grant for solar-powered AI cameras that send SMS pest and disease alerts to farmers.',
       why='A Kenyan AI-in-agriculture winner is a local company to watch as it runs a six-month field deployment.',
       source='Tech In Africa', date='2026-11-16',
       url='https://www.techinafrica.com/kenyan-agritech-startup-farmerlifeline-technologies-wins-50000-innovate-africa-challenge-grant/'),
 ]},
 {'id': 'hiring', 'stories': [
  dict(title='US software developers aged 22 to 25 remain about a fifth below late 2022 levels',
       summary='A 15 November analysis of Stanford ADP payroll data, with figures to October 2026, found the employment index for US software developers aged 22 to 25 at 81.4, down almost a fifth since November 2022, while ages 41 to 49 stood at 120.2 and US developer job ads were 18% below February 2020.',
       why='Junior hiring is still tighter than mid-career hiring in the US data, which is why worldwide and Africa-open roles remain the better targets.',
       source='Datahub', date='2026-11-15',
       url='https://datahub.io/blog/junior-dev-hiring'),
 ]},
 {'id': 'kenya', 'stories': [
  dict(title='Safaricom says it is using AI against scams as M-PESA tops KES100 billion in half-year revenue',
       summary='On 16 November TechTrendsKE reported that Safaricom net income rose 35.9% to KES58.2 billion in the six months to September 2026, M-PESA passed KES100 billion in half-year revenue for the first time, and Group Chief Risk Officer Nicholas Mulila said the company is using AI to detect threats while pursuing AI certification by February.',
       why='Kenya\'s largest fintech platform is investing in AI for fraud and security, which sits next to the payments and automation work on his CV.',
       source='TechTrendsKE', date='2026-11-16',
       url='https://techtrendske.co.ke/2026/11/16/inside-safaricoms-fight-to-keep-customers-safe-in-the-age-of-ai-scams/'),
  dict(title='Safaricom is pushing M-PESA beyond payments into credit, savings and insurance',
       summary='On 15 November TechTrendsKE reported that in the six months to 30 September 2026 Safaricom recorded KSh7.1 billion in financial services revenue, up 55.3%, with 17.5 million credit customers, 3.4 million money market fund customers and 67,500 insurance policies, while M-PESA itself generated KSh100.1 billion, or 42.8% of total revenue.',
       why='M-PESA is being run as a distribution platform for credit and insurance, which is useful context for Kenyan fintech roles.',
       source='TechTrendsKE', date='2026-11-15',
       url='https://techtrendske.co.ke/2026/11/15/mpesa-financial-services-expansion/'),
  dict(title='Safaricom says refugee IDs can be used to register for SIM and M-PESA',
       summary='On 16 November ECONEWS reported that Safaricom\'s 2026 Sustainable Business Report lists recognition of refugee identification documents for SIM and M-PESA registration in Dadaab, Kakuma-Kalobeyei and urban areas, without giving a registration total.',
       why='Identity and onboarding rules in Kenyan mobile money are a recurring theme in local fintech work.',
       source='ECONEWS', date='2026-11-16',
       url='https://econews.co.ke/2026/11/16/refugee-access-mpesa-kenya/'),
 ]},
]}

feed_jobs = [
 dict(title='Associate Programmer Graduate Training Programme', company='Tamu Group (Tera Carbon)',
      location='Nairobi', source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/associate-programmer-graduate-training-programme-tamu-group',
      posted='2026-11-13', deadline='2026-11-27', salary_as_shown='Not shown',
      fit_note='0-2 years graduate training programme.', already_applied=True),
 dict(title='Junior Software Developer', company='Bridge Talent Management',
      source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/junior-software-developer-bridge-talent',
      posted='2026-11-10', salary_as_shown='Not shown', already_applied=True),
 dict(title='IT Officer', company='Ignite Energy Access', location='Nairobi',
      source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/it-officer-ignite-energy-access',
      posted='2026-11-13', deadline='2026-11-27', salary_as_shown='Not shown',
      fit_note='First-line IT support role.', already_applied=False),
 dict(title='IT', company='OPPO Kenya',
      source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/it-oppo-kenya',
      posted='2026-11-11', deadline='2026-11-20',
      salary_as_shown='KSh 50,000-70,000/month (page inconsistent)', already_applied=True),
 dict(title='ICT Officer II Software Development', company='Digital Health Agency',
      source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/ict-officer-ii-software-development-digital-health-agency-dha',
      deadline='2026-12-01', salary_as_shown='Not shown', already_applied=True),
 dict(title='ICT Officer II Enterprise Infrastructure', company='Digital Health Agency',
      source='MyJobMag personalised',
      url='https://www.myjobmag.co.ke/job/ict-officer-ii-enterprise-infrastructure-digital-health-agency-dha',
      posted='2026-11-11', deadline='2026-12-01', salary_as_shown='Not shown',
      fit_note='Entry-grade ICT Officer II role in enterprise infrastructure.', already_applied=False),
 dict(title='Intern Data Analytics', company='UN-Habitat', location='Nairobi',
      source='Fuzu',
      url='https://www.fuzu.com/kenya/jobs/intern-data-analytics-un-habitat-aeab8b46',
      posted='2026-11-13', deadline='2026-11-25', salary_as_shown='Not shown',
      fit_note='On-site 6-month internship, 0 months experience, Power BI required. Same UN-Habitat internship Ben skipped on 16 November.',
      already_applied=True),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 25, 'pulled_is_approximate': True, 'kept': 6, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 20, 'pulled_is_approximate': True, 'kept': 1, 'signed_in': True, 'error': None},
}

run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-17T07:55:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + [
     'Fuzu (signed-in browser pass)',
     'MyJobMag personalised feed (signed-in browser pass)',
     'Wellfound (signed-in browser pass)',
     'Workday API (BD / Summit recheck)',
     'Ashby API (Kraken and Supabase recheck)',
     'Zoho Recruit public API (FlexiSAF)',
     'Greenhouse API (Qualio)',
     'Teamtailor (The Whiteam)',
     'micro1 portal API (recheck)',
     'MyJobMag and LinkedIn (via Local Search Bot)',
 ],
             'news': ['OpenAI', 'Hugging Face blog', 'TechCrunch', 'Disrupt Africa', 'Tech In Africa', 'Datahub', 'TechTrendsKE', 'ECONEWS']},
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
      "A signed-in browser pass of Wellfound pulled about 19 roles and kept 1 (the Wellfound feed hides jobs that are not Nairobi-eligible). "
      "Fuzu was checked in the signed-in browser (~20 pulled, 1 kept): Intern Data Analytics at UN-Habitat is the internship Ben skipped on 16 November. The pass also dropped UNEP Digital Policy and AI Researcher (unpaid policy internship) and Valley Hospital IT Intern (Nakuru). "
      "The MyJobMag personalised feed was also checked in the signed-in browser (~25 pulled, 6 kept): Tamu Group Associate Programmer Graduate Training Programme, Bridge Talent Junior Software Developer, OPPO Kenya IT, and Digital Health Agency ICT Officer II Software Development are already in the applied log; Ignite Energy Access IT Officer and Digital Health Agency ICT Officer II Enterprise Infrastructure are not. "
      "All nine kept micro1 roles were left off the shortlist because they match earlier micro1 applications or briefings under the already-surfaced company-and-title rule, including Software Engineer, Software Engineer - Backend, Software Engineer - Open Source Contributions, ML Engineer, Machine Learning Researcher, Applied Scientists, AI Agent Tester, Enterprise Client Partner, and Independent Consultant. "
      "Kraken's Software Engineer II - React Native - Consumer Growth role is open on Ashby (published 16 November, remote) but the country list is the United Kingdom plus Brazil, the UAE, Ireland, Peru, Sweden, Colombia, Argentina, Romania, Cyprus, Switzerland, Portugal, Lithuania, South Africa, Czech Republic, Canada, Hungary, Mexico, Chile, Poland, Spain and Bulgaria, without Kenya. The Ashby posting does not state a number of years; it asks for strong experience building production React Native and TypeScript apps. It was also left off because it matches an earlier Kraken Software Engineer listing under the company-and-title rule. "
      "Supabase's Software Engineer - AI Tooling role remains open worldwide on Ashby but still asks for 5+ years, and it was already dropped in yesterday's briefing. "
      "The Jobgether Summit listing for Junior Software Developer AI & Digital Solutions is a BD Workday role based in Heidelberg, Germany. The BD Jobgether duplicate returned HTTP 410. The Arc Full-Stack Developer listing could not be confirmed as open. The Whiteam AI Engineer and Technical Analyst roles are Spain-only and ask for at least 3 years. Qualio's Full Stack Engineer role is Ireland / EU and asks for 3+ years. "
      "The remote shortlist is shorter than the usual 6-10 because few fresh, junior-to-mid roles both stayed open, clearly included Kenya, and had not already been shown. "
      "Feed roles that are not already in the Kenya jobs or the applied log are listed under From your feeds.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped', sum(len(g['stories']) for g in news['groups']), 'stories')
