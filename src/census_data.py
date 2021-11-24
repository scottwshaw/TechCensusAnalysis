import matplotlib.pyplot as plt
import numpy as np
import pandas as pandas
import re
import seaborn as sns

def synonym(word):
    synonyms = {
        'TypeScript':'Typescript',
        'Azure devops':'Azure DevOps',
        'Self-hosted Gitlab': 'GitLab',
        'Gitlab Pipelines': 'GitLab',
        'GitLab CI':'GitLab',
        'Gitlab':'GitLab',
        'BitBucket':'Bitbucket',
        'Bitbucket Pipelines':'Bitbucket',
        'BitBucket Pipeline':'Bitbucket',
        'Golang':'Go lang',
        'GoLang':'Go lang',
        'FireStore':'FireBase',
        'cypress':'Cypress',
        'nodejs':'Node.js',
        '':'No response',
        '.':'No response',
        'terraform':'Terraform',
        'Migrating from AWS CodeCommit': 'AWS CodeCommit',
        'Migrating from: AWS CodeCommit': 'AWS CodeCommit',
        'aurora': 'Aurora',
        'Aurora Serverless': 'Aurora',
        'Aurora (nonserverless)': 'Aurora',
        'postgres)': 'PostgreSQL'
    }
    return synonyms.get(word.strip(),word)
    
def map_dora_category(metric, category):
    map = {
        'cycle_time': {
            'Less than one hour': 'Elite',
            'Less than one day': 'Elite',
            'Between one day and one week': 'High',
            'Between one week and one month': 'Medium',
            'Between one month and six months': 'Low',
            'More than six months': 'Low',
            'We aren\'t yet in production': 'N/A'},
        'deploy_freq': {
            'On demand(multiple deploys per day)': 'Elite',
            'Between once per hour and once per day': 'Elite',
            'Between once per day and once per week': 'High',
            'Between once per week and once per month': 'Medium',
            'Between once per month and once every six months': 'Low',
            'Fewer than once every six months': 'Low',
            'We aren\'t yet in production': 'N/A'},
        'failure_rate': {
            'Less than 15%': 'elite-high-med',
            '16 - 30%': '',
            '31-45%': '',
            '45 - 60%': 'Low',
            'More than 60%': '',
            'We aren\'t yet in production': 'N/A'},
        'time_to_restore': {
            'Less than one hour': 'Elite',
            'Less than one day': 'high-med',
            'Between one day and one week': '' ,
            'Between one week and one month': 'Low',
            'Between one month and six months': '',
            'More than six months': '',
            'We aren\'t yet in production': 'N/A'}}
    return map.get(metric, {}).get(category, '')

def expand_results_by_weights(results,weightss):
    expanded = []
    for (result,size) in zip(results,weightss):
        expanded = expanded + [result] * int(float(size))
    return expanded

def decompose_and_expand_by_weights(results,weights):
    expanded = []
    for (compound_result,size) in zip(results,weights):
        # results_list = map(lambda x: synonym(x), re.split('; |;|, |,', compound_result.strip()))
        results_list = map(synonym, re.split('; |;|, |,', compound_result.strip()))
        for(result) in results_list:
            expanded = expanded + [result] * int(float(size))
    return expanded

def expand_frame_by_weights(results, weights):
    expanded_results = pandas.DataFrame()
    for column in results.columns:
        expanded_results[column] = expand_results_by_weights(results[column].tolist(),weights)
    return expanded_results

def box_plot_weighted(results, weights, xlabels):
    expanded_results = expand_frame_by_weights(results, weights)
    plt.figure(figsize=[11,5])
    sns.boxplot(data=expanded_results, orient="h")
    plt.xticks([-2, 0, 2], xlabels)
    plt.show()

def histogram_weighted_tech(results, weights):
    # replace blanks with NA to be dropped later
    clean_results = results.applymap(synonym)
    for column in clean_results.columns:
        expanded_results = decompose_and_expand_by_weights(clean_results[column], weights)
        unique_values, counts = np.unique(expanded_results, return_counts=True)
        a = pandas.DataFrame(list(zip(unique_values, counts)), columns=['Value','Count'])
        a.sort_values(by='Count',ascending=True).plot.barh(y='Count',x='Value')
        plt.title(column)
        plt.show()

def histogram_weighted_team_compositions(team_sizes):
    expanded_data = expand_frame_by_weights(team_sizes, team_sizes['twers'])
    sns.histplot(data=expanded_data['twers'].apply(int)).set(xlabel='number of TW coders on the team',ylabel='number of TWers')
    plt.show() 
    ratio = pandas.to_numeric(expanded_data['nontwers']).round().astype(int)/expanded_data['twers'].astype(int)
    sns.histplot(data=ratio).set(xlabel='ratio of nonthoughtworks coders to TW coders (nonTWers/TWers)', ylabel='number of TWers')  
    plt.show()

def histogram_weighted_enablement_series(enablement_series, weights):
    expanded_series =  expand_results_by_weights(enablement_series, weights)
    sns.histplot(data=list(map(int,expanded_series))).set(xlabel='degree of enablement',ylabel='number of TWers')
    plt.show()

def histogram_weighted_complexity_series(series, weights):
    expanded_series =  expand_results_by_weights(series, weights)
    sns.histplot(data=list(map(int,expanded_series))).set(xlabel='technical complexity',ylabel='number of TWers')
    plt.xlim((1,10))
    plt.xticks([1,3,5,7,10],["hello world in excel","3","5","7","apollo moon landing"])
    plt.show()

def histogram_unweighted_team_compositions(team_sizes):
    sns.histplot(data=team_sizes['twers'].astype(int)).set(xlabel='number of TW coders on the team',ylabel='number of teams')
    plt.show() 
    ratio = pandas.to_numeric(team_sizes['nontwers']).round().astype(int)/pandas.to_numeric(team_sizes['twers']).round().astype(int)
    sns.histplot(data=ratio).set(xlabel='ratio of nonthoughtworks coders to TW coders (nonTWers/TWers)', ylabel='number of teams')  
    plt.show()

def chars_defaults_correlation_plot(chars, defaults):
    # Don't know if the normalisation step is necessary or if corr() does that anyway.  Just in case.
    combined_frame = pandas.concat([chars, defaults],axis=1).apply(lambda x: (x-x.mean())/(x.max()-x.min()), axis=0)
    corr = combined_frame.corr()
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    mask = np.triu(np.ones_like(corr, dtype=np.bool))     # Generate a mask for the upper triangle
    plt.figure(figsize=[9,8])  
    sns.heatmap(corr, cmap=cmap, mask=mask)
    plt.subplots_adjust(left=.2, bottom=.26, right=None, top=None, wspace=None, hspace=None)
    plt.show()

def print_dora_metrics(metrics, weights):
    expanded_metrics = expand_frame_by_weights(metrics, weights)
    for column in metrics.columns:
        expanded_metrics[column] = expanded_metrics[column].apply(lambda x: map_dora_category(column,x))
        category, count = np.unique(expanded_metrics[column], return_counts=True)
        total = sum(count)
        normed_count = count/total
        print("\n")
        print(column)
        for x in zip(category,normed_count):
            print(x)

def plot_history_regression(defaults, facet_name):
    defaults["Date"] = defaults.index
    melted_df = pandas.melt(defaults, id_vars="Date", var_name=facet_name, value_name="score")
    melted_df["score"] = melted_df["score"].astype(float)
    melted_df["Date"] = melted_df["Date"].apply(lambda x: x.timestamp())
    sns.lmplot(x="Date", y="score", data=melted_df, hue=facet_name, ci=30)
    plt.xticks(np.unique(melted_df["Date"]), np.datetime_as_string(defaults.index, unit='M'))
    plt.show()

def plot_history_regression_since(defaults, facet_name, earliest_date_string):
    earliest_date = pandas.Timestamp(earliest_date_string)
    defaults["Date"] = defaults.index
    defaults_since = defaults.loc[defaults["Date"] >= earliest_date]
    melted_df = pandas.melt(defaults_since, id_vars="Date", var_name=facet_name, value_name="score")
    melted_df["score"] = melted_df["score"].astype(float)
    melted_df["Date"] = melted_df["Date"].apply(lambda x: x.timestamp())
    sns.lmplot(x="Date", y="score", data=melted_df, hue=facet_name, ci=30)
    plt.xticks(np.unique(melted_df["Date"]), np.datetime_as_string(defaults_since.index, unit='M'))
    plt.show()

def weighted_means(team_sizes, defaults):
    fdef = defaults.astype(float)
    fts = team_sizes.astype(float)
    results = fdef.T.dot(fts).div(fts.sum())
    return results








