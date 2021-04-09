import census_data as cd
import read_sheets as rs
import datetime as dt

# Q2
# DATA_SHEET_URL = 'https://docs.google.com/spreadsheets/d/136TnM1O6hNY7kGLgTcmMUwbdJ6UQF1pglQuNbny_pYQ/edit?usp=sharing'
#
# Q3
# DATA_SHEET_URL = 'https://docs.google.com/spreadsheets/d/16njXPlGy2u3hlmA4WJFB64ZVeBx5_b3fxfmv9_ViPGc/edit?usp=sharing'
# CHARACTERISTICS_COLUMNS = slice(10,17)
# SENSIBLE_DEFAULTS_COLUMNS = slice(18,26)
# TECH_STACK_COLUMNS = slice(32,45)
# DORA_COLUMNS = slice(26,30)
# TEAM_COMPOSITION_COLUMNS = slice(4,6)
# 2021Q1
DATA_SHEET_URL= 'https://docs.google.com/spreadsheets/d/1WT0RoIAyPoC54iewnqirUKJMcMHHTuRBxi1L7k-NPH0/edit?usp=sharing'
HISTORY_SHEET_URL= 'https://docs.google.com/spreadsheets/d/1w_KmO4-Krhi5vzTFYT3z69pmSJUE8l2nfbh5imZpPuc/edit?usp=sharing'
CHARACTERISTICS_COLUMNS = slice(12,19)
SENSIBLE_DEFAULTS_COLUMNS = slice(20,28)
TECH_STACK_COLUMNS = slice(33,49)
DORA_COLUMNS = slice(28,32)
TEAM_COMPOSITION_COLUMNS = [4,7]
# d = rs.data_from_google_sheet(DATA_SHEET_URL)
# charsf = d.iloc[:,CHARACTERISTICS_COLUMNS].applymap(lambda x: rs.chars_to_num[x])
# sensible_defaults = d.iloc[:,SENSIBLE_DEFAULTS_COLUMNS].applymap(lambda x: rs.defaults_to_num[x])
# tech = d.iloc[:,TECH_STACK_COLUMNS].applymap(lambda x: str(x))
# cd.histogram_unweighted_team_compositions(d.iloc[:,TEAM_COMPOSITION_COLUMNS])
# cd.histogram_weighted_team_compositions(d.iloc[:,TEAM_COMPOSITION_COLUMNS])
# cd.histogram_weighted_enablement_series(d['type'],d['twers'])
# cd.chars_defaults_correlation_plot(charsf, sensible_defaults)
# cd.box_plot_weighted(charsf, d['twers'], ['strongly disagree','neither agree nor disagree', 'strongly agree'])
# cd.box_plot_weighted(sensible_defaults, d['twers'], ['Not applied','Partially applied', 'Fully applied'])
# cd.histogram_weighted_tech(tech, d['twers'])
# cd.print_dora_metrics(d.iloc[:,DORA_COLUMNS],d['twers'])
h = rs.history_from_google_sheet(HISTORY_SHEET_URL)
cd.plot_default_history(h)