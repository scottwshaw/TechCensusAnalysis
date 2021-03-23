import gspread
import numpy as np
import pandas as pd

def to_short_labels(long_label):
    short_labels = {
        'Timestamp':'time', 
        'Username':'username', 
        'Email Address':'email',  
        'Account':'account',
        'Account Name':'account', 
        'Team':'team', 
        'Team name or designation within the account':'Team',
        'Number of TWers actively developing code':'twers',
        'Number of Australian TWers actively developing code':'twers',
        'Number of non-TW developers actively developing code':'nontwers', 
        'Are there ThoughtWorks developers outside Australia working on this team?':'distributed',
        'If this is a distributed project, how many offshore developers are there?':'numoffshore',
        'City':'city', 
        'What type of engagement is this?':'type',
        'How technically complex would you say this project is?':'complexity',
        'How long has this team been together (project duration)':'duration_to_date',
        'How long do you anticipate this project to last?':'future_duration',
        ' [We have influence over the technical decisions on our project]':'project_influence',
        ' [We have influence over technical decisions across the customer organisation]':'org_influence', 
        ' [We have a clear understanding of the technology direction/strategy for our client, and how what we are doing furthers that direction]':'business_purpose',
        ' [This is an engagement that I would recommend to a senior TW engineer to further their career]':'good_for_seniors',
        ' [This is an engagement that I would recommend to a junior TW engineer to learn fundamental skills]':'good_for_juniors',
        ' [The technology stack used on this engagement is state of the art]':'cutting_edge',
        ' [We are responsible for running production systems, including on-call support]':'prod_responsible',
        'Any other comments?':'project_comments',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Trunk-based development]':'trunk_based_dev',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Test-driven development]':'test_driven_dev',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Pair programming]':'pair_programming',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Build security in]':'build_security_in',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Fast automated build]':'fast_build',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Early and frequent deployment]':'early_freq_deploy',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Quality and debt effectively managed]':'debt_managed',
        'Please select all of the following practices that are followed on your team  (See https://docs.google.com/presentation/d/1-XEAso777d9Y6KJqLmesF5esMk9TFJUzEaDEheyF8hQ/edit?usp=sharing for a deeper explanation of these practices) [Done means production-ready]':'done_means_prod',
        'How long does it take to go from code commit to code successfully running in production?':'cycle_time',
        'How long does it take to go from code commit to code successfully running in production? ':'cycle_time',
        'How often do we deploy code?':'deploy_freq',
        'What percentage of changes either result in degraded service or subsequently require remediation (e.g., lead to service impairment or outage, require a hotfix, a rollback, a fix-forward, or a patch)?':'failure_rate',
        'How long does it generally take to restore service when a service incident occurs(e.g. unplanned outage, service impairment)?':'time_to_restore',
        'Any other comments about practices?':'defaults_comments',
        'Type of application':'app_type',
        'Frontend Framework':'frontend_framework',
        'Version Control':'source_control',
        'Artefacts':'artefact_repo',
        'CI/CD':'build_server',
        'Programming Language':'language',
        'Storage':'storage',
        'Persistence':'persistence',
        'Persistence (select all that apply.  e.g. if you\'re using RDS Postgres version, select both PostgreSQL and RDS)':'persistence',
        'Observability':'observability',
        'Logging/Monitoring':'logging',
        'Messaging':'messaging',
        'Identity':'identity',
        'Cloud Platform':'cloud_vendor',
        'Provisioning and Deployment':'infrastructure_provisioning',
        'Serverless Stuff':'serverless',
        'Container hosting':'container_hosting',
        'Miscellaneous':'misc'}
    return short_labels[long_label]

chars_to_num = {'1. Strongly disagree':-2, '2':-1, '3. Neither agree not disagree':0, '4':1, '5. Strongly agree':2, '':0}
defaults_to_num = {'1. Not applied':-2, '2':-1, '3. Partially applied':0, '4':1, '5. Fully applied':2, '':0}




def data_from_google_sheet(SHEET_URL):
    gc = gspread.oauth()
    census_data = gc.open_by_url(SHEET_URL)
    sheet = census_data.get_worksheet(0)
    data = sheet.get_all_values()
    tslvec = np.vectorize(to_short_labels)
    return pd.DataFrame(data=data[1:],columns=tslvec(data[0]))
