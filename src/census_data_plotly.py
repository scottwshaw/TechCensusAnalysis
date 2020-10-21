import gspread
import numpy as np
import pandas as pandas
import plotly.express as px

chars_to_num = {'1. Strongly disagree':-2, '2':-1, '3. Neither agree not disagree':0, '4':1, '5. Strongly agree':2, '':0}
defaults_to_num = {'1. Not applied':-2, '2':-1, '3. Partially applied':0, '4':1, '5. Fully applied':2, '':0}
def to_short_labels(long_label):
    short_labels = {
        'Timestamp':'time', 
        'Username':'username', 
        'Account':'account', 
        'Team':'team', 
        'Number of TWers actively developing code':'twers',
        'Number of non-TW developers actively developing code':'nontwers', 
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
        'How often do we deploy code?':'deploy_freq',
        'What percentage of changes either result in degraded service or subsequently require remediation (e.g., lead to service impairment or outage, require a hotfix, a rollback, a fix-forward, or a patch)?':'failure_rate',
        'How long does it generally take to restore service when a service incident occurs(e.g. unplanned outage, service impairment)?':'time_to_restore',
        'Any other comments about practices?':'defaults_comments',
        'Type of application':'app_type',
        'Frontend Framework':'frontend_framework',
        'Version Control':'source_control',
        'Artefacts':'artefact_repo',
        'CI/CD':'build_tool',
        'Programming Language':'language',
        'Storage':'storage',
        'Persistence':'persistence',
        'Observability':'observability',
        'Logging/Monitoring':'logging',
        'Cloud Platform':'cloud',
        'Provisioning and Deployment':'provisioning',
        'Serverless Stuff':'serverless',
        'Container hosting':'containers',
        'Miscellaneous':'misc'}
    return short_labels[long_label]

def data_from_google_sheet(sheet_url):
    gc = gspread.oauth()
    census_data = gc.open_by_url(sheet_url)
    sheet = census_data.get_worksheet(0)
    data = sheet.get_all_values()
    tslvec = np.vectorize(to_short_labels)
    return pandas.DataFrame(data=data[1:],columns=tslvec(data[0]))

def expand_results_by_weights(results,weightss):
    expanded = []
    for (result,size) in zip(results,weightss):
        expanded = expanded + [result] * int(float(size))
    return expanded

def decompose_and_expand_by_weights(results,weights):
    expanded = []
    for (compound_result,size) in zip(results,weights):
        results_list = compound_result.split(';')
        for(result) in results_list:
            print(result)
            expanded = expanded + [result] * int(float(size))
    return expanded

# def box_plot(results):
#     sns.boxplot(data=results, orient="h")
#     plt.show()

def expand_frame_by_weights(results, weightss):
    expanded_results = pandas.DataFrame()
    for column in results.columns:
        expanded_results[column] = expand_results_by_weights(results[column].tolist(),weightss)
    return expanded_results

def box_plot_weighted(results, weightss, xlabels):
    expanded_results = expand_frame_by_weights(results, weightss)
    fig = px.box(expanded_results)
    fig.show()

# def histogram_weighted_team_compositions(team_sizes):
#     expanded_data = expand_frame_by_weights(team_sizes, team_sizes['twers'])
#     sns.histplot(data=expanded_data['twers'].apply(int)).set(xlabel='number of TW coders on the team',ylabel='number of TWers')
#     plt.show() 
#     ratio = expanded_data['nontwers'].apply(int)/expanded_data['twers'].apply(int)
#     sns.histplot(data=ratio).set(xlabel='ratio of nonthoughtworks coders to TW coders (nonTWers/TWers)', ylabel='number of TWers')  
#     plt.show()

# def histogram_unweighted_team_compositions(team_sizes):
#     sns.histplot(data=team_sizes['twers'].apply(int)).set(xlabel='number of TW coders on the team',ylabel='number of teams')
#     plt.show() 
#     ratio = team_sizes['nontwers'].apply(int)/team_sizes['twers'].apply(int)
#     sns.histplot(data=ratio).set(xlabel='ratio of nonthoughtworks coders to TW coders (nonTWers/TWers)', ylabel='number of teams')  
#     plt.show()

# def chars_defaults_correlation_plot(chars, defaults):
#     combined_frame = pandas.concat([chars, defaults],axis=1)
#     # Generate a mask for the upper triangle
#     corr = combined_frame.corr()
#     cmap = sns.diverging_palette(220, 10, as_cmap=True)
#     mask = np.triu(np.ones_like(corr, dtype=np.bool))
#     plt.figure(figsize=[9,8])  
#     sns.heatmap(corr, cmap=cmap, mask=mask)
#     plt.subplots_adjust(left=.2, bottom=.26, right=None, top=None, wspace=None, hspace=None)
#     plt.show()











