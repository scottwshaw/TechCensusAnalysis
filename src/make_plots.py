import census_data as cd
import read_sheets as rs
import pandas as pd
from config import *

d = rs.data_from_google_sheet(DATA_SHEET_URL)
charsf = d.iloc[:,CHARACTERISTICS_COLUMNS].applymap(lambda x: rs.chars_to_num[x])
sensible_defaults = d.iloc[:,SENSIBLE_DEFAULTS_COLUMNS].applymap(lambda x: rs.defaults_to_num[x])
tech = d.iloc[:,TECH_STACK_COLUMNS].applymap(lambda x: str(x))
cd.histogram_unweighted_team_compositions(d.iloc[:,TEAM_COMPOSITION_COLUMNS])
cd.histogram_weighted_team_compositions(d.iloc[:,TEAM_COMPOSITION_COLUMNS])
cd.histogram_weighted_enablement_series(d['type'],d['twers'])
cd.chars_defaults_correlation_plot(charsf, sensible_defaults)
cd.box_plot_weighted(charsf, d['twers'], ['strongly disagree','neither agree nor disagree', 'strongly agree'])
cd.box_plot_weighted(sensible_defaults, d['twers'], ['Not applied','Partially applied', 'Fully applied'])
cd.histogram_weighted_tech(tech, d['twers'])
cd.print_dora_metrics(d.iloc[:,DORA_COLUMNS],d['twers'])
print(cd.weighted_means(d['twers'],sensible_defaults))
print(cd.weighted_means(d['twers'],charsf))
dh = rs.history_from_google_sheet(DEFAULT_HISTORY_SHEET_URL)
cd.plot_history_regression(dh, "Sensible Default")
cd.plot_history_regression_since(dh, "Sensible Default", "2021-01-01T12")
ch = rs.history_from_google_sheet(CHAR_HISTORY_SHEET_URL)
cd.plot_history_regression(ch, "Project Characteristic")
cd.plot_history_regression_since(ch, "Project Characteristic","2021-01-01T12")
