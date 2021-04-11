"""
Retrieves the number of active COVID-19 cases in the Philippines per city/municipality

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

# Modifiable, depending on the time of testing the data set
# Same day, set days = 0, the next day, set days = 1
# Can also be used for other previous date
today_ref = dt.date(dt.today() - td(days=1))
today = today_ref.strftime("%Y%m%d")

case_info = 'DOH COVID Data Drop_ ' + today + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

# Making sure that those cases with NCR and ROF as region of residence will also use the same for province
missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)

# Filling other NA values
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'UNKNOWN REGION'})
df_case_info = df_case_info.fillna({'ProvRes': 'UNKNOWN PROVINCE - ' + df_case_info['RegionRes']})
df_case_info = df_case_info.fillna({'CityMunRes': 'UNKNOWN CITY - ' + df_case_info['ProvRes']})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

if __name__ == '__main__':
    today_dt = (dt.now() - td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    today_df = df_case_info[(df_case_info['RemovalType'] == 'ACTIVE')]
    today_active = pd.pivot_table(today_df, index=['CityMunRes', 'ProvRes'], aggfunc='size')
    today_active_df = pd.DataFrame(today_active).reset_index()
    today_active_df.columns = ['City/Municipality', 'Province', 'Number of Active Cases']

    sorted_df = today_active_df.sort_values(by='Number of Active Cases', ascending=False)
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df.to_excel('DOH COVID-19 Active Cases - ' + today_dt.strftime('%Y%m%d') + '.xlsx')