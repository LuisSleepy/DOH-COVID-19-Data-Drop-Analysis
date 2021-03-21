"""
Retrieves the number of new confirmed COVID-19 cases in the Philippines per city/municipality
and compare it to the previous day

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
    # Get the number of cases in the previous day
    prev_dt = (dt.now() - td(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    prev_df = df_case_info[(df_case_info['DateRepConf'] == prev_dt)]
    prev_confirmed_cases = pd.pivot_table(prev_df, index=['CityMunRes', 'ProvRes'], aggfunc='size')
    prev_confirmed_cases_df = pd.DataFrame(prev_confirmed_cases).reset_index()
    prev_confirmed_cases_df.columns = ['City/Municipality', 'Province', prev_dt.strftime("%Y%m%d") + ' Addl Cases']

    # Get the latest additional number of cases
    pres_dt = (dt.now() - td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    pres_df = df_case_info[(df_case_info['DateRepConf'] == pres_dt)]
    pres_confirmed_cases = pd.pivot_table(pres_df, index=['CityMunRes', 'ProvRes'], aggfunc='size')
    pres_confirmed_cases_df = pd.DataFrame(pres_confirmed_cases).reset_index()
    pres_confirmed_cases_df.columns = ['City/Municipality', 'Province', pres_dt.strftime("%Y%m%d") + ' Addl Cases']

    # Combine the two series, the previous one and the latest one
    combined_df = pd.merge(prev_confirmed_cases_df, pres_confirmed_cases_df, on=['City/Municipality', 'Province'])
    combined_df['Change in Percentage'] = combined_df.apply(
        # Calculates the change (in percentage) of additional cases per city/municipality
        lambda x: ((x[pres_dt.strftime("%Y%m%d") + ' Addl Cases'] - x[prev_dt.strftime("%Y%m%d") + ' Addl Cases']) /
                 x[pres_dt.strftime("%Y%m%d") + ' Addl Cases']), axis=1
    )

    # Arrange the rows by the number of latest additional cases by descending order
    sorted_df = combined_df.sort_values(by=[pres_dt.strftime("%Y%m%d") + ' Addl Cases'], ascending=False)
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df.to_excel('DOH COVID-19 Cases - ' + pres_dt.strftime("%Y%m%d") + "- Additional Cases.xlsx")