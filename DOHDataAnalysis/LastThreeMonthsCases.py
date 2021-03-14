"""
Retrieves the COVID-19 cases in a province in the Philippines in the past 12 weeks

Author:
Jan Luis Antoc
BS Computer Engineering
De La Salle University - Manila
"""

import pandas as pd
from datetime import datetime as dt, timedelta as td

province = {

}
# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

today = dt.date(dt.today())
yesterday = (today - td(days=1)).strftime("%Y%m%d")

case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'
df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 19], low_memory=False)

missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region', 'ProvRes': 'Unknown '

                                                                                                       'Province'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()
# Checks for all recorded provincial residences
provinces = sorted(df_case_info['ProvRes'].unique())

# Display the corresponding number for each provincial residence
for i in range(86):
    print(i, ": ", provinces[i])

prov_num = -1

print("")
# Check for the validity of the chosen province via numbering
while prov_num < 0 or prov_num > 85:
    try:
        prov_num = int(input("Choose a valid provincial residence number: "))
    except ValueError:
        print("Enter an integer from 0 to 85 inclusive.")

# Get only the cases coming from the chosen province
chosen_prov = provinces[prov_num]
df_case_info = df_case_info[df_case_info['ProvRes'] == chosen_prov]

# Get the cases that were only recorded in the past 12 weeks
three_months = (dt.now() - td(days=84)).replace(hour=0, minute=0, second=0, microsecond=0)
df_case_info = df_case_info[df_case_info['DateRepConf'] >= three_months]

# Automation of retrieving the number of COVID-19 cases in the chosen region recorded in the past 12 weeks
confirmed = df_case_info.pivot_table(index='DateRepConf', aggfunc='size')
all_cases = df_case_info.pivot_table(index='DateRepConf', columns='RemovalType', aggfunc='size')
all_cases['CONFIRMED'] = confirmed
all_cases = all_cases.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
all_cases = all_cases.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
print(all_cases)
print(all_cases.info())
all_cases.to_csv(chosen_prov + " COVID-19 Cases - Last 12 Weeks.csv")