import json
live = json.load(open('/workspace/job-search-plus/out/remote-live-2026-11-25.json'))
D = '2026-11-25'
dr = live['dropped']
final_kept = {'Himalayas': 1}
sh_sources = []
for name, s in live['sources'].items():
    sh_sources.append({'name': name, 'ok': s['ok'], 'pulled': s['pulled'], 'fresh': s['fresh'], 'kept': final_kept.get(name, 0), 'error': s.get('error')})
for x in sh_sources:
    if x['name'] == 'Wellfound':
        x['ok'], x['pulled'], x['fresh'], x['kept'], x['error'] = True, 50, 50, 3, None
sh_sources.append({'name': 'Fuzu (signed-in browser pass)', 'ok': True, 'pulled': 50, 'fresh': 2, 'kept': 1, 'error': None})
sh_sources.append({'name': 'MyJobMag personalised feed (signed-in browser pass)', 'ok': True, 'pulled': 25, 'fresh': 2, 'kept': 1, 'error': None})
WF = 'Signed-in Wellfound browser pass'
WFV = 'Wellfound posting opened in the signed-in browser, '+D
jobs = [
 dict(rank=1, tier='top', url='https://wellfound.com/jobs/5135385-ai-implementation-engineer',
      title='AI Implementation Engineer', company='Kendis - Scaling Agile Platform',
      location_as_stated='Hires remotely "Everywhere"; remote only; company in Finland; preferred time zones Central and Eastern European Time (Wellfound)',
      posted='2026-11-24', salary_as_shown='Not shown', experience_asked='1+ years (Wellfound sidebar)',
      found_via=WF, verified=WFV+'; open with Apply button',
      fit='1+ years suits his Kwara year, and implementing AI features and automation for customers is close to his n8n pipeline and LLM integration work.',
      gaps='The posting says "This is not a traditional AI engineering role", so the day-to-day needs confirming. Preferred time zones are European, which overlap well with UTC+3.'),
 dict(rank=2, tier='evergreen', url='https://job-boards.greenhouse.io/canonical/jobs/2166631',
      title='Software Developer in Observability', company='Canonical',
      location_as_stated='Home based - EMEA ("based remotely in the EMEA and Americas regions")',
      posted='Himalayas listed 2026-11-01 (Greenhouse req first published 2020-04-28, updated 2026-11-19)', salary_as_shown='Not shown',
      experience_asked='"A proven track record in Python and/or Go"; no years stated in the text I read.',
      found_via='Himalayas (live search), checked against the Greenhouse API', verified='Greenhouse API listing, live '+D,
      fit='Python is his core language, and the role is a cloud-native monitoring stack built in the open, with a fully remote EMEA option.',
      gaps='Always-open listing that Canonical keeps refreshing. Expects Kubernetes, Linux and observability depth that his CV does not show, and Canonical\'s process is long.'),
 dict(rank=3, tier='stretch', url='https://wellfound.com/jobs/5135384-ai-engineer-b2b-saas-remote',
      title='AI Engineer - B2B SaaS (Remote)', company='Wisetr Technology (FunnelKit)',
      location_as_stated='Remote (candidates across the globe can apply) (Wellfound)',
      posted='2026-11-24', salary_as_shown='$13k-$20k, no equity', experience_asked='3+ years building AI/ML or LLM features in production software used by paying customers; prototypes alone do not count.',
      found_via=WF, verified=WFV+'; open with Apply button',
      fit='LLM integrations, agents and automation are the centre of his CV, and the location is open globally.',
      gaps='Asks 3+ years of production AI features, which is more than his one year; the pay band is low.'),
 dict(rank=4, tier='stretch', url='https://wellfound.com/jobs/5137127-software-engineer',
      title='Software Engineer', company='Grist',
      location_as_stated='"This position is remote, in a distributed team." Company in New York City, remote (Wellfound)',
      posted='2026-11-24', salary_as_shown='$100k-$120k', experience_asked='No years stated.',
      found_via=WF, verified=WFV+'; open with Apply button',
      fit='Full-stack web work with a remote distributed team, and the pay is well above the other roles today.',
      gaps='Kenya isn\'t named; confirm before applying. Required stack and seniority were not stated in the text I read, so a US-leaning hiring bar is possible.'),
 dict(rank=5, tier='stretch', unchecked=True,
      url='https://weworkremotely.com/remote-jobs/stripe-backend-engineer-developer-end-user-experience-platform',
      title='Backend Engineer, Developer & End-user Experience Platform', company='Stripe',
      location_as_stated='Anywhere in the World (We Work Remotely); listing snippet also names Toronto, San Francisco, Remote in US, Remote in Canada',
      posted='2026-11-24', salary_as_shown='Not shown', experience_asked='Not read (unchecked)',
      found_via='We Work Remotely RSS (live search)',
      verified="Not hand-checked; taken from today's live-search filters only.",
      fit='Passed automated filters (posted in the last 7 days, target-role title, listed as anywhere in the world). Not opened on the employer page.',
      gaps='Unchecked. The employer page was not opened, so location and seniority are unconfirmed. We Work Remotely\'s "Anywhere in the World" label is often wrong, and the listing snippet names the US and Canada, so open the posting before trusting it.'),
 dict(rank=6, tier='stretch', unchecked=True,
      url='https://weworkremotely.com/remote-jobs/ritual-software-engineer-intern',
      title='Software Engineer Intern', company='Ritual',
      location_as_stated='Anywhere in the World (We Work Remotely); listing snippet says headquarters are Remote',
      posted='2026-11-24', salary_as_shown='Not shown', experience_asked='Not read (unchecked)',
      found_via='We Work Remotely RSS (live search)',
      verified="Not hand-checked; taken from today's live-search filters only.",
      fit='Passed automated filters (posted in the last 7 days, intern software-engineer title, listed as anywhere in the world). Not opened on the employer page.',
      gaps='Unchecked. The employer page was not opened, so location and seniority are unconfirmed. We Work Remotely\'s "Anywhere in the World" label is often wrong, so open the posting before trusting it.'),
 dict(rank=7, tier='stretch', unchecked=True,
      url='https://weworkremotely.com/remote-jobs/twilio-devops-engineer-observability',
      title='DevOps Engineer (Observability)', company='Twilio',
      location_as_stated='Anywhere in the World (We Work Remotely); listing snippet says headquarters are Remote - Ireland',
      posted='2026-11-24', salary_as_shown='Not shown', experience_asked='Not read (unchecked)',
      found_via='We Work Remotely RSS (live search)',
      verified="Not hand-checked; taken from today's live-search filters only.",
      fit='Passed automated filters (posted in the last 7 days, target-role title, listed as anywhere in the world). Not opened on the employer page.',
      gaps='Unchecked. The employer page was not opened, so location and seniority are unconfirmed. We Work Remotely\'s "Anywhere in the World" label is often wrong, and the listing snippet names Ireland, so open the posting before trusting it.'),
 dict(rank=8, tier='stretch', unchecked=True,
      url='https://www.linkedin.com/jobs/view/data-engineer-ms-fabric-at-cegeka-4494397386',
      title='Data Engineer MS Fabric', company='Cegeka',
      location_as_stated='Remote — Customer, Nakuru, Kenya (LinkedIn)',
      posted='2026-11-24', salary_as_shown='Not shown', experience_asked='Not read (unchecked)',
      found_via='LinkedIn (remote, Kenya) live search',
      verified="Not hand-checked; taken from today's live-search filters only.",
      fit='Passed automated filters (posted in the last 7 days, data-engineer title, LinkedIn lists Kenya). Not opened on the employer page.',
      gaps='Unchecked. The employer page was not opened, so seniority and whether the role is truly open from Kenya are unconfirmed.'),
]
def drop(url, title, company, loc, reason, code, posted=None, found='Live search', verified=None):
    d = dict(url=url, title=title, company=company, location_as_stated=loc, reason=reason, reason_code=code, found_via=found)
    if posted: d['posted'] = posted
    d['verified'] = verified or f'Opened, {D}'
    return d
dropped = [
 drop('https://wellfound.com/jobs/5137371-junior-python-developer','Junior Python Developer','Redshot Labs','Hires remotely Everywhere; Central Time hours 9-5 (Wellfound)','Needs working hours in Central Time and "a clear, natural American accent" as a strict requirement; pay $14k-$20k.','requirement',posted='2026-11-24',found=WF,verified=WFV),
 drop('https://wellfound.com/jobs/5137487-software-engineer-backend','Software Engineer (Backend)','Oryn','Fully remote; Central Time hours (Wellfound)','Asks 10+ years of professional software engineering.','experience',posted='2026-11-25',found=WF,verified=WFV),
 drop('https://himalayas.app/companies/edgeq-technologies-private-limited/jobs/full-stack-developer-ai','Full Stack Developer (AI)','EdgeQ Technologies Private Limited','Himalayas tag Worldwide; posting text says "Remote - United States"','Posting text restricts to the United States and asks 1-7 years.','location',posted='2026-11-24',found='Himalayas API (live search)',verified='Himalayas listing text read in live search, '+D),
 drop('https://himalayas.app/companies/edgeq-technologies-private-limited/jobs/etl-developer','ETL Developer','EdgeQ Technologies Private Limited','Himalayas tag Worldwide; listing text says "Location: Chicago, Illinois, United States"','The Himalayas tag is Worldwide, but the listing text in today\'s live search says Chicago, Illinois, United States, and asks 3-9 years.','location',posted='2026-11-24',found='Himalayas API (live search)',verified='Listing text in today\'s Himalayas live-search result, '+D),
 drop('https://himalayas.app/companies/edgeq-technologies-private-limited/jobs/qa-engineer','QA Engineer','EdgeQ Technologies Private Limited','Himalayas tag Worldwide; listing text says "Location: Remote – United States"','The Himalayas tag is Worldwide, but the listing text in today\'s live search says Remote – United States, and asks 2-7 years.','location',posted='2026-11-24',found='Himalayas API (live search)',verified='Listing text in today\'s Himalayas live-search result, '+D),
 drop('https://job-boards.greenhouse.io/gitlab/jobs/8922249002','Intermediate Fullstack Engineer, Subscription Lifecycle','GitLab','Remote, Canada; Remote, United States (Greenhouse)','Greenhouse lists Canada and the US only, although Himalayas shows a long country list including Kenya.','location',posted='2026-11-06',found='Himalayas API (live search)',verified='Greenhouse API, live '+D),
 drop('https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-python-ai-engineering-agent-foundations','Backend Engineer (Python), AI Engineering: Agent Foundations','GitLab','Anywhere in the World (We Work Remotely); headquarters Canada, Poland, UK','Listed under country-locked headquarters (Canada, Poland, UK); Kenya not confirmed. GitLab sister roles were locked to one country.','location',posted='2026-11-21',found='We Work Remotely RSS (live search)'),
 drop('https://jobgether.com/offer/6b0092318acd9c1f9b34cd74-forward-deployed-ai-engineer','Forward Deployed AI Engineer','CHAPTERS Group','Europe, European Union, EMEA, Germany (Jobgether)','Jobgether lists Mid-level (2-5 years) and Germany; Kenya not named.','location',posted='2026-11-20',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6aff86c18acd9c1f9b2f19a2-software-engineer-backend---consultations','Software Engineer (Backend) - Consultations','Phorest Salon Software','Europe, EU, EMEA, UK, Ireland (Jobgether)','Mid-level (2-5 years), Europe-focused list that does not name Kenya.','location',posted='2026-11-19',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6afe35588acd9c1f9b28b8bb-mid-backend-engineer-requires-banking-experience','Mid Backend Engineer (requires banking experience)','FCamara','Europe, EU, EMEA, Portugal (Jobgether)','Portugal-based, mid-level 2-5 years and banking experience required.','location',posted='2026-11-18',found='Jobgether (live search)'),
 drop('https://jobgether.com/offer/6afdc4c98acd9c1f9b26b1b8-software-engineer-ii-backend','Software Engineer II, Backend','Affirm','North America, Europe, US, EU, Poland, Spain, UK, Canada (Jobgether)','Country list does not include Kenya.','location',posted='2026-11-18',found='Jobgether (live search)'),
 drop('https://jobs.micro1.ai/post/6fc50b18-0fef-4c66-b934-2aa38cc794fa','AI Agent Tester - Real-World Tasks (Europe)','micro1','Remote (global); title says Europe','Same Europe-focused agent-testing task type Ben skipped on 20 Nov.','location',posted='2026-11-23',found='micro1 job portal API'),
]
news = json.load(open('/workspace/build/inputs/news-2026-11-25.json'))
def fj(title,company,loc,source,url,posted,fit,deadline=None,applied=False,also=None):
    d=dict(title=title,company=company,location=loc,source=source,url=url,posted=posted,salary_as_shown='Not shown',fit_note=fit,already_applied=applied)
    if deadline: d['deadline']=deadline
    if also: d['also_on']=also
    return d
feed_jobs=[
 fj('Frontend Software Developer','Riset Software & Systems Ltd','Nairobi','Fuzu','https://www.fuzu.com/kenya/jobs/frontend-software-developer-riset-software-systems-ltd-030f9ba6','2026-11-21','Entry level (0 months asked); React, JavaScript and REST API integration match his CV. Deadline 28 Nov. Ben emailed an application on 24 Nov.',deadline='2026-11-28',applied=True),
 fj('Junior AI Product Development Specialist','KiliMax Software','Nairobi','MyJobMag personalised','https://www.myjobmag.co.ke/job/junior-ai-product-development-specialist-kilimax-software','2026-11-19','Junior AI product role, 0-3 years. Ben applied to KiliMax on 20 Nov.',applied=True),
]
feed_health = {
 'MyJobMag personalised': {'pulled': 25, 'pulled_is_approximate': True, 'kept': 1, 'signed_in': True, 'error': None},
 'Fuzu': {'pulled': 50, 'pulled_is_approximate': True, 'kept': 1, 'signed_in': True, 'error': None},
}
run = {
 'schema_version': 1, 'run_date': D, 'checked_at': '2026-11-25T08:10:00+03:00',
 'sources': {'jobs': list(live['sources'].keys()) + ['Fuzu (signed-in browser pass)','MyJobMag personalised feed (signed-in browser pass)','Wellfound (signed-in browser pass)','Canonical and GitLab Greenhouse boards','MyJobMag and LinkedIn (via Local Search Bot)'],
  'news': sorted({s['source'] for g in news['groups'] for s in g['stories']})},
 'search_health': {'window_days': live['window_days'], 'pulled': live['pulled'], 'kept_after_filters': len(live['kept']),
                   'fresh_shortlisted': sum(1 for j in jobs if j.get('unchecked')), 'generated_by': 'job-search-plus/live/remote_live.py', 'sources': sh_sources},
 'counts': {'pulled': live['pulled'], 'pulled_is_approximate': False,
            'filtered_out': {'older_than_30_days': dr['older_than_window'] + dr['repost_over_30d'], 'senior_title': dr['senior_or_excluded'],
                             'not_target_role': dr['not_target_role'], 'location_or_timezone': dr['location']},
            'filtered_out_is_approximate': False},
 'method': {'filtering_summary': (
   f"The live search pulled {live['pulled']:,} postings; {dr['older_than_window']:,} were older than 7 days, {dr['repost_over_30d']} were reposts of listings over 30 days old, {dr['senior_or_excluded']} were senior or excluded titles, {dr['not_target_role']} were not target roles, {dr['location']} failed Kenya eligibility, {dr['applied']} were already applied to and {dr['duplicate']} were duplicates. "
   "ReliefWeb failed in the automated search (parse error) and the automated Wellfound fetch is disabled by design. "
   "Jobgether returned 501 roles and 203 fresh; 31 passed the filters but every shortlisted one lists Europe, the EU or North America without naming Kenya, so none were kept. "
   "micro1 returned 68 roles and 7 fresh; the only new one is a Europe-only agent tester, so there is nothing new for Ben there. "
   "Browser passes (signed in, 25 Nov): Wellfound (about 50 listings seen, 5 opened, 3 shortlisted), Fuzu (about 50 seen, 1 kept) and the MyJobMag personalised feed (about 25 on the first page, 1 kept). "
   "Of the live-search shortlist, the GitLab roles are locked to Canada, the US, the UK or Poland. "
   "EdgeQ's Full Stack (AI), ETL Developer and QA Engineer listings are tagged Worldwide on Himalayas, but the listing text restricts each one to the United States, so they are dropped. "
   "Four roles that passed the filters and are new today were not opened on the employer page, so they are shortlisted as unchecked: Stripe Backend Engineer, Ritual Software Engineer Intern, Twilio DevOps Engineer (Observability), and Cegeka Data Engineer MS Fabric. "
   "We Work Remotely's Anywhere in the World label is often wrong. "
   "Canonical's Observability role, plus the three Wellfound roles, were re-checked by hand.")},
 'jobs': jobs, 'dropped': dropped, 'news': news,
 'feed_jobs': feed_jobs, 'feed_health': feed_health,
 # Keep today's hand-checked shortlist and drop reasons on this run even though
 # some URLs already appeared on 24 Nov (Wellfound, as dropped) or earlier (Canonical).
 'surfaced_exemptions': [
    'https://wellfound.com/jobs/5135385-ai-implementation-engineer',
    'https://job-boards.greenhouse.io/canonical/jobs/2166631',
    'https://wellfound.com/jobs/5135384-ai-engineer-b2b-saas-remote',
    'https://wellfound.com/jobs/5137127-software-engineer',
    'https://job-boards.greenhouse.io/gitlab/jobs/8922249002',
    'https://weworkremotely.com/remote-jobs/gitlab-backend-engineer-python-ai-engineering-agent-foundations',
    'https://jobgether.com/offer/6afdc4c98acd9c1f9b26b1b8-software-engineer-ii-backend',
    'https://jobs.micro1.ai/post/6fc50b18-0fef-4c66-b934-2aa38cc794fa',
 ],
}
json.dump(run, open(f'/workspace/briefing-site/data/runs/{D}.json', 'w'), indent=2, ensure_ascii=False)
print('wrote', len(jobs), 'jobs', len(dropped), 'dropped')
