"""
Retrieves the number of new confirmed COVID-19 cases in the Philippines per city/municipality
in the last five days, including current date

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

# Testing the data drop on the same day of posting
today = dt.date(dt.today())
today = today.strftime("%Y%m%d")

case_info = 'DOH COVID Data Drop_ ' + today + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

# Making sure that those cases with NCR and ROF as region of residence will also use the same for province
missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)

# Filling other NA values
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region',
                                    'ProvRes': 'Unknown Province', 'CityMunRes': 'Unknown City'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

five_cases = []
five_cases_dates = []

if __name__ == '__main__':
    # Last five days, including current date
    for i in range(5):
        # Updates to be done in the next few weeks to optimize the automation
        today_dt = (dt.now() - td(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        filtered_data = df_case_info[(df_case_info['DateRepConf'] == today_dt)]

        confirmed_cases = pd.pivot_table(filtered_data, index=['ProvRes', 'CityMunRes'], aggfunc='size')
        all_cases_city = pd.pivot_table(filtered_data, index=['ProvRes', 'CityMunRes'], columns='RemovalType',
                                        aggfunc='size')
        all_cases_city['CONFIRMED'] = confirmed_cases
        all_cases_city = all_cases_city.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
        all_cases_city = all_cases_city.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
        today_dt = today_dt.strftime("%Y%m%d")

        all_cases_city.to_excel('DOH COVID-19 Cases -' + today_dt + '.xlsx')
