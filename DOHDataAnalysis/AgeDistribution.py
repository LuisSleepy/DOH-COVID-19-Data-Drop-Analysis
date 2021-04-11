"""
Age Distribution of COVID-19 Cases in the Philippines

This program determine the number of COVID-19 cases per age and/or age ranges.

Author:
Jan Luis Antoc
BS Computer Engineering
De La Salle University - Manila
"""

import pandas as pd
import sys
import numpy as np
from datetime import datetime as dt, timedelta as td

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
np.set_printoptions(threshold=sys.maxsize)

yesterday = (dt.date(dt.today()) - td(days=1)).strftime("%Y%m%d")
case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)

# Filling other NA values
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'UNKNOWN REGION'})
df_case_info = df_case_info.fillna({'ProvRes': 'UNKNOWN PROVINCE - ' + df_case_info['RegionRes']})
df_case_info = df_case_info.fillna({'CityMunRes': 'UNKNOWN CITY - ' + df_case_info['ProvRes']})
df_case_info = df_case_info.fillna({'Age': 'NO AGE SPECIFIED'})
df_case_info = df_case_info.fillna({'AgeGroup': 'NO AGE GROUP SPECIFIED'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

if __name__ == '__main__':
    aug_first = dt(year=2020, month=8, day=1, hour=0, minute=0, second=0, microsecond=0)
    aug_last = dt(year=2020, month=8, day=31, hour=0, minute=0, second=0, microsecond=0)

    aug_df = df_case_info[(df_case_info['DateRepConf'] >= aug_first) & (df_case_info['DateRepConf'] <= aug_last)]
    aug_age_group = pd.pivot_table(aug_df, index='AgeGroup', aggfunc='size')
    aug_age_group_df = pd.DataFrame(aug_age_group).reset_index()
    aug_age_group_df.columns = ['Age Group', 'August 2020 Count']
    aug_sum = aug_age_group_df['August 2020 Count'].sum()
    aug_age_group_df['August 2020 Distribution'] = (aug_age_group_df['August 2020 Count'] / aug_sum)

    mar_first = dt(year=2021, month=3, day=1, hour=0, minute=0, second=0, microsecond=0)
    mar_last = dt(year=2021, month=3, day=31, hour=0, minute=0, second=0, microsecond=0)

    mar_df = df_case_info[(df_case_info['DateRepConf'] >= mar_first) & (df_case_info['DateRepConf'] <= mar_last)]
    mar_age_group = pd.pivot_table(mar_df, index='AgeGroup', aggfunc='size')
    mar_age_group_df = pd.DataFrame(mar_age_group).reset_index()
    mar_age_group_df.columns = ['Age Group', 'March 2021 Count']
    mar_sum = mar_age_group_df['March 2021 Count'].sum()
    mar_age_group_df['March 2021 Distribution'] = mar_age_group_df['March 2021 Count'] / mar_sum

    combined_df = pd.merge(aug_age_group_df, mar_age_group_df, on=['Age Group'])
    zero_to_four = combined_df.iloc[0]
    five_to_nine = combined_df.iloc[9]
    combined_df.drop(labels=[0, 9], axis=0, inplace=True)

    new_combined_df = pd.DataFrame()
    new_combined_df = new_combined_df.append(zero_to_four, ignore_index=True)
    new_combined_df = new_combined_df.append(five_to_nine, ignore_index=True)
    new_combined_df = new_combined_df.append(combined_df, ignore_index=True)
    new_combined_df = new_combined_df.astype({'August 2020 Count' : 'int64', 'March 2021 Count' : 'int64'})

    new_combined_df.to_excel('DOH COVID-19 Cases per Age Group (August 2020 vs March 2021).xlsx')