# from google.colab import auth
# auth.authenticate_user()
import gspread
import numpy as np
import pandas as pandas
import seaborn as sns
import matplotlib.pyplot as plt

chars_to_num = {'1. Strongly disagree':-2, '2':-1, '3. Neither agree not disagree':0, '4':1, '5. Strongly agree':2, '':0}
defaults_to_num = {'1. Not applied':-2, '2':-1, '3. Partially applied':0, '4':1, '5. Fully applied':2, '':0}
def to_short_labels(long_label):
    short_labels = {
        'Timestamp':'time', 
        'Email Address':'email', 
        'Account':'account', 
        'Team':'team', 
        'Number of TWers actively developing code':'twers',
        'Number of non-TW developers actively developing code':'nontwers', 
        'City':'city', 
        'What type of engagement is this?':'type',
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
        'How often do we deploy code?':'deploy_freq',
        'What percentage of changes either result in degraded service or subsequently require remediation (e.g., lead to service impairment or outage, require a hotfix, a rollback, a fix-forward, or a patch)?':'failure_rate',
        'How long does it generally take to restore service when a service incident occurs(e.g. unplanned outage, service impairment)?':'time_to_restore',
        'Any other comments about practices?':'defaults_comments',
        'Type of application':'app_type',
        'Frontend Framework':'frontend_framework',
        'Version Control':'source_control',
        'Artefacts':'artefact_repo',
        'CI/CD':'',
        'Programming Language':'',
        'Storage':'',
        'Persistence':'',
        'Logging/Monitoring':'',
        'Cloud Platform':'',
        'Provisioning and Deployment':'',
        'Container hosting':'',
        'Miscellaneous':''}
    return short_labels[long_label]

def data_from_google_sheet(sheet_url):
    gc = gspread.oauth()
    census_data = gc.open_by_url(sheet_url)
    sheet = census_data.get_worksheet(0)
    data = sheet.get_all_values()
    tslvec = np.vectorize(to_short_labels)
    return pandas.DataFrame(data=data[1:],columns=tslvec(data[0]))


def plot_histogram(series):
    # Make default histogram of sepal length
    # sns.distplot(series, bins=5)
    # plt.xlim(-3,3)
    plt.show()

def expand_results_by_team_size(results,team_sizes):
    expanded = []
    for (result,size) in zip(results,team_sizes):
        expanded = expanded + [result] * int(float(size))
    return expanded

def box_plot(results):
    sns.boxplot(data=results, orient="h")
    plt.show()

def box_plot_weighted(results, team_sizes, xlabels):
    expanded_results = pandas.DataFrame()
    # team_sizes.iloc[2] = 1 # total hack
    for column in results.columns:
        expanded_results[column] = expand_results_by_team_size(results[column].tolist(),team_sizes)
    plt.figure(figsize=[11,5])
    sns.boxplot(data=expanded_results, orient="h")
    plt.xticks([-2, 0, 2], xlabels)
    plt.show()

def chars_defaults_correlation(chars, defaults):
    combined_frame = pandas.concat([chars, defaults],axis=1)
    # Generate a mask for the upper triangle
    corr = combined_frame.corr()
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    plt.figure(figsize=[9,8])  
    sns.heatmap(corr, cmap=cmap, mask=mask)
    plt.subplots_adjust(left=.2, bottom=.26, right=None, top=None, wspace=None, hspace=None)
    plt.show()


sheet_url = 'https://docs.google.com/spreadsheets/d/136TnM1O6hNY7kGLgTcmMUwbdJ6UQF1pglQuNbny_pYQ/edit?usp=sharing'
d = data_from_google_sheet(sheet_url)
charsf = d.iloc[:,10:17].applymap(lambda x: chars_to_num[x])
sensible_defaults = d.iloc[:,18:26].applymap(lambda x: defaults_to_num[x])
# box_plot_weighted(charsf, d.iloc[:,4], ['strongly disagree','neither agree nor disagree', 'strongly agree'])
chars_defaults_correlation(charsf, sensible_defaults)
box_plot_weighted(charsf, d['twers'], ['strongly disagree','neither agree nor disagree', 'strongly agree'])
box_plot_weighted(sensible_defaults, d['twers'], ['Not applied','Partially applied', 'Fully applied'])










