import pandas as pd
import numpy as np
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
last_week = (today - td(days=7))

case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)
# Fill those rows with no values in RemovalType as "Active" and in RegionRes as "Unknown Region"

missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region', 'ProvRes': 'Unknown '

                                                                                                       'Province'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()
df_case_info['DateRepConf'] = pd.to_datetime(df_case_info['DateRepConf'], yearfirst=True)


# Getting the number of cases per day (for the past one week)
last_week_dt = dt.now() - td(days=8)
yesterday_dt = dt.now() - td(days=1)
filtered_data = df_case_info[(df_case_info['DateRepConf'] >= last_week_dt) & (df_case_info['DateRepConf'] <= yesterday_dt)]
filtered_data_confirmed = pd.pivot_table(filtered_data, index='ProvRes', aggfunc='size')
filtered_data_all = pd.pivot_table(filtered_data, index='ProvRes', columns='RemovalType', aggfunc='size')
filtered_data_all['CONFIRMED'] = filtered_data_confirmed
filtered_data_all = filtered_data_all.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
filtered_data_all = filtered_data_all.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
filtered_data_all.to_excel('DOH COVID-19 Cases Per Province (Last One Week) - ' + yesterday + '.xlsx')
