"""
Retrieves COVID-19 cases
"""

import pandas as pd
from datetime import datetime as dt, timedelta as td, date as d

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

# Automation of retrieving the number of COVID-19 cases in the chosen region recorded in the past 12 weeks
# all_confirmed = df_case_info.pivot_table(index='DateRepConf', aggfunc='size')
# all_cases = df_case_info.pivot_table(index='DateRepConf', columns='RemovalType', aggfunc='size')
# all_cases['CONFIRMED'] = all_confirmed

# For all provinces
all_confirmed = df_case_info.pivot_table(index='DateRepConf', aggfunc='size')
all_cases = df_case_info.pivot_table(index='DateRepConf', columns='RemovalType', aggfunc='size')
all_cases['CONFIRMED'] = all_confirmed
all_cases = all_cases.reset_index()
all_cases.insert(0, 'ProvRes', 'All', allow_duplicates=False)
all_cases = all_cases.set_index(['ProvRes', 'DateRepConf'])

# Getting cases for each province
prov_confirmed = df_case_info.pivot_table(index=['ProvRes', 'DateRepConf'], aggfunc='size')
prov_cases = df_case_info.pivot_table(index=['ProvRes', 'DateRepConf'], columns='RemovalType', aggfunc='size')
prov_cases['CONFIRMED'] = prov_confirmed
prov_cases = prov_cases.append(all_cases)
prov_cases = prov_cases.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
prov_cases = prov_cases.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})

prov_cases.to_csv("Daily COVID-19 Cases of All Provinces - " + yesterday + ".csv")