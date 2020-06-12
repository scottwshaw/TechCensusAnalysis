# from google.colab import auth
# auth.authenticate_user()
import gspread
# from oauth2client.client import GoogleCredentials
# gc = gspread.authorize(GoogleCredentials.get_application_default())
gc = gspread.oauth()

census_data = gc.open_by_url('https://docs.google.com/spreadsheets/d/136TnM1O6hNY7kGLgTcmMUwbdJ6UQF1pglQuNbny_pYQ/edit?usp=sharing')
sheet = census_data.get_worksheet(0)
data = sheet.get_all_values()
import numpy as np
d = np.array(data)
num_twers = d[1:,4]

chars = (project_influence,
 org_influence,
 senior_nps,
 junior_nps,
 cutting_edge,
 prod_responsible) = tuple(np.transpose(d[1:,10:16]))

to_num = {'1. Strongly disagree':-2, '2':-1, '3. Neither agree not disagree':0, '4':1, '5. Strongly agree':2, '':0}
convert = lambda x: to_num[x]
aconvert = np.vectorize(convert)
charsf = tuple(aconvert(c) for c in chars)
print(charsf)