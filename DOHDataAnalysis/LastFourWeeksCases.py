"""
DOH COVID-19 Data Drop Analysis on the Number of New Cases in the Last Week

This program can determine the number of new COVID-19 cases in the Philippines in the past four weeks based on
health status and residence. Tests the latest data drop the previous day.

Author:
Jan Luis Antoc
BS Computer Engineering
De La Salle University - Manila
"""

import pandas as pd
from datetime import datetime as dt, timedelta as td

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# The csv file from DOH updated every day at 10:00 AM (Philippine Standard Time)
# I encounter error in downloading the file directly since it comes from Google Drive
today = dt.date(dt.today())
yesterday = (today - td(days=1)).strftime("%Y%m%d")

case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

# Mapping NCR and ROF regional residence as their provincial residence
missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)

# Filling other NA values
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'UNKNOWN REGION'})
df_case_info = df_case_info.fillna({'ProvRes': 'UNKNOWN PROVINCE - ' + df_case_info['RegionRes']})
df_case_info = df_case_info.fillna({'CityMunRes': 'UNKNOWN CITY - ' + df_case_info['ProvRes']})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

# Iteration for getting the number of cases per week (up to last four weeks)
iteration = 0
start_num_days = 7
end_num_days = 1
dataframes = []

while iteration < 4:
    start = (dt.now() - td(days=start_num_days)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_str = start.strftime('%Y%m%d')
    end = (dt.now() - td(days=end_num_days)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_str = end.strftime('%Y%m%d')
    filtered_data = df_case_info[(df_case_info['DateRepConf'] >= start) & (df_case_info['DateRepConf'] <=
                                                                           end)]
    filtered_data_confirmed = pd.pivot_table(filtered_data, index='ProvRes', aggfunc='size')
    filtered_data_all = pd.pivot_table(filtered_data, index='ProvRes', columns='RemovalType', aggfunc='size')
    filtered_data_all['CONFIRMED'] = filtered_data_confirmed
    filtered_data_all = filtered_data_all.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
    filtered_data_all = filtered_data_all.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
    filtered_data_all_df = pd.DataFrame(filtered_data_all).reset_index()
    filtered_data_all_df.columns = ['PROVINCE', 'ACTIVE-' + start_str + "-" + end_str, 'DIED-' + start_str + "-" +
                                    end_str, 'RECOVERED-' + start_str + "-" + end_str, 'CONFIRMED-' + start_str + "-" +
                                    end_str]

    dataframes.append(filtered_data_all_df)
    iteration += 1
    start_num_days += 7
    end_num_days += 7

second_last_weeks_df = pd.merge(dataframes[0], dataframes[1], on=['PROVINCE'])
fourth_third_weeks_df = pd.merge(dataframes[2], dataframes[3], on=['PROVINCE'])
all_four_weeks_df = pd.merge(second_last_weeks_df, fourth_third_weeks_df, on=['PROVINCE'])

all_four_weeks_df.to_excel('DOH COVID-19 Cases in the Last Four Weeks-' + yesterday + '-.xlsx')
