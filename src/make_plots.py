import census_data as cd

# Q2
# sheet_url = 'https://docs.google.com/spreadsheets/d/136TnM1O6hNY7kGLgTcmMUwbdJ6UQF1pglQuNbny_pYQ/edit?usp=sharing'
#
# Q3
sheet_url = 'https://docs.google.com/spreadsheets/d/16njXPlGy2u3hlmA4WJFB64ZVeBx5_b3fxfmv9_ViPGc/edit?usp=sharing'
d = cd.data_from_google_sheet(sheet_url)
charsf = d.iloc[:,10:17].applymap(lambda x: cd.chars_to_num[x])
sensible_defaults = d.iloc[:,18:26].applymap(lambda x: cd.defaults_to_num[x])
tech = d.iloc[:,32:45].applymap(lambda x: str(x))
cd.histogram_weighted_tech(tech, d['twers'])
cd.histogram_unweighted_team_compositions(d.iloc[:,4:6])
cd.histogram_weighted_team_compositions(d.iloc[:,4:6])
cd.chars_defaults_correlation_plot(charsf, sensible_defaults)
cd.box_plot_weighted(charsf, d['twers'], ['strongly disagree','neither agree nor disagree', 'strongly agree'])
cd.box_plot_weighted(sensible_defaults, d['twers'], ['Not applied','Partially applied', 'Fully applied'])