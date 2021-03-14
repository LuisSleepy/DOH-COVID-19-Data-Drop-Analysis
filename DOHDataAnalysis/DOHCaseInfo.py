"""
DOH COVID-19 Data Drop Overall Analysis

This program can determine the number of COVID-19 cases in the Philippines based on health status and residence.
Currently prioritizing the data drop of the previous day with respect to current day.

Author:
Jan Luis Antoc
BS Computer Engineering
De La Salle University - Manila
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Currently no way to automate the download of the DOH COVID-19 Data Drop each day
today = datetime.date(datetime.today())
yesterday = (today - timedelta(days=1)).strftime("%Y%m%d")

# Testing on the same day of the data drop release
# case_info = 'DOH COVID Data Drop_ ' + today.strftime("%Y%m%d") + ' - 04 Case Information.csv'
case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

# Making sure that those cases with NCR and ROF as region of residence will also use the same for province
missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)

# Filling other NA values
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region',
                                    'ProvRes': 'Unknown Province', 'CityMunRes': 'Unknown City'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

if __name__ == '__main__':
    print(yesterday + "\n")
    print('Number of Cases with no Date of Onset of Illness:', len(df_case_info[df_case_info['DateOnset'].isna()]))
    print('Number of Deaths with no Date of Death:', len(df_case_info[(df_case_info['RemovalType'] == 'DIED')
                                                                      & (df_case_info['DateDied'].isna())]))
    print('Number of Recoveries with no Date of Recovery:', len(df_case_info[(df_case_info['RemovalType']
                                                                              == 'RECOVERED') &
                                                                             df_case_info['DateRecover'].isna()]))
    print('Number of Cases with no Date of Confirmation: ', len(df_case_info[df_case_info['DateRepConf'].isna()]))

    # Caution: These average days below might not be accurate as no
    days_positive = df_case_info['DateResultRelease'] - df_case_info['DateSpecimen']
    days_positive = days_positive / np.timedelta64(1, 'D')
    print('Average days of getting a positive result:', days_positive.mean())
    days_confirmed = df_case_info['DateRepConf'] - df_case_info['DateSpecimen']
    days_confirmed = days_confirmed / np.timedelta64(1, 'D')
    print('Average days of confirming a positive case:', days_confirmed.mean())

    # Automation of retrieving the number of COVID-19 cases per region
    confirmed_cases = pd.pivot_table(df_case_info, index='RegionRes', aggfunc='size')
    all_cases_region = pd.pivot_table(df_case_info, index='RegionRes', columns='RemovalType', aggfunc='size')
    all_cases_region['CONFIRMED'] = confirmed_cases
    all_cases_region = all_cases_region.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
    all_cases_region = all_cases_region.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
    all_cases_region.to_excel('DOH COVID-19 Cases Per Region - ' + yesterday + '.xlsx')

    # Automation of retrieving the number of COVID-19 cases per province
    confirmed_cases = pd.pivot_table(df_case_info, index='ProvRes', aggfunc='size')
    all_cases_province = pd.pivot_table(df_case_info, index='ProvRes', columns='RemovalType', aggfunc='size')
    all_cases_province['CONFIRMED'] = confirmed_cases
    all_cases_province = all_cases_province.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
    all_cases_province = all_cases_province.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
    all_cases_province.to_excel('DOH COVID-19 Cases Per Province - ' + yesterday + '.xlsx')

    # Checking the number of cases per city
    # No total confirmed cases row yet, only active, died, and recovered
    confirmed_cases = pd.pivot_table(df_case_info, index=['ProvRes', 'CityMunRes'], aggfunc='size')
    all_cases_city = pd.pivot_table(df_case_info, index=['ProvRes', 'CityMunRes'], columns='RemovalType',
                                    aggfunc='size')
    all_cases_city['CONFIRMED'] = confirmed_cases
    all_cases_city = all_cases_city.fillna({'ACTIVE': 0, 'DIED': 0, 'RECOVERED': 0, 'CONFIRMED': 0})
    all_cases_city = all_cases_city.astype({'ACTIVE': 'int64', 'DIED': 'int64', 'RECOVERED': 'int64'})
    all_cases_city.to_excel('DOH COVID-19 Cases Per City - ' + yesterday + '.xlsx')

    '''
    Succeeding line of codes are for the data visualization of total confirmed cases, recoveries, and deaths
    '''

    # Graphing the number of cases per day based on confirmation day
    confirmed_series = df_case_info.pivot_table(index=df_case_info['DateRepConf'], aggfunc='size')

    # The number of recoveries and deaths are based on the date of removal.
    deaths = pd.pivot_table(df_case_info, index='DateDied', columns='RemovalType', aggfunc='size')
    recoveries = pd.pivot_table(df_case_info, index='DateRecover', columns='RemovalType', aggfunc='size')

    # Looking if there are errors in data (e.g. recovered patient but has a date of death)
    print("Recovered but with date of death:", df_case_info.loc[(df_case_info['RemovalType'] == 'RECOVERED') &
                                                                (~ df_case_info['DateDied'].isna())])
    print("Active but with date of death:", df_case_info.loc[(df_case_info['RemovalType'] == 'ACTIVE') &
                                                             (~ df_case_info['DateDied'].isna())])
    print("Dead but with date of recovery:", df_case_info.loc[(df_case_info['RemovalType'] == 'DIED') &
                                                              (~ df_case_info['DateRecover'].isna())])

    confirmed_frame = {'Confirmed': confirmed_series}
    confirmed_reported_df = pd.DataFrame(confirmed_frame)

    deaths_frame = {'Deaths': deaths['DIED']}
    deaths_reported_df = pd.DataFrame(deaths_frame)

    recoveries_frame = {'Recoveries': recoveries['RECOVERED']}
    recoveries_reported_df = pd.DataFrame(recoveries_frame)

    confirmed_reported_df['Daily Average'] = \
        confirmed_reported_df['Confirmed'].expanding(min_periods=1).mean().round(0)

    confirmed_reported_df['7-Day Moving Average'] = \
        confirmed_reported_df['Confirmed'].rolling(window=7).mean().round(0)

    deaths_reported_df['Daily Average'] = deaths_reported_df['Deaths'].expanding(min_periods=1).mean().round(0)
    deaths_reported_df['7-Day Moving Average'] = deaths_reported_df['Deaths'].rolling(window=7).mean().round(0)

    recoveries_reported_df['Daily Average'] = \
        recoveries_reported_df['Recoveries'].expanding(min_periods=1).mean().round(0)
    recoveries_reported_df['7-Day Moving Average'] = \
        recoveries_reported_df['Recoveries'].rolling(window=7).mean().round(0)

    confirmed_figure = go.Figure()
    deaths_figure = go.Figure()
    recoveries_figure = go.Figure()

    confirmed_figure.add_trace(
        go.Bar(x=confirmed_reported_df.index, y=confirmed_reported_df['Confirmed'], name='Confirmed')
    )
    confirmed_figure.add_trace(
        go.Scatter(x=confirmed_reported_df.index, y=confirmed_reported_df['Daily Average'], name='Daily Average')
    )
    confirmed_figure.add_trace(
        go.Scatter(x=confirmed_reported_df.index, y=confirmed_reported_df['7-Day Moving Average'],
                   name='7-Day Moving Average', line=dict(color='orange'))
    )

    deaths_figure.add_trace(
        go.Bar(x=deaths_reported_df.index, y=deaths_reported_df['Deaths'], name='Deaths')
    )
    deaths_figure.add_trace(
        go.Scatter(x=deaths_reported_df.index, y=deaths_reported_df['Daily Average'], name='Daily Average')
    )
    deaths_figure.add_trace(
        go.Scatter(x=deaths_reported_df.index, y=deaths_reported_df['7-Day Moving Average'],
                   name='7-Day Moving Average', line=dict(color='orange'))
    )

    recoveries_figure.add_trace(
        go.Bar(x=recoveries_reported_df.index, y=recoveries_reported_df['Recoveries'], name='Recoveries')
    )
    recoveries_figure.add_trace(
        go.Scatter(x=recoveries_reported_df.index, y=recoveries_reported_df['Daily Average'], name='Daily Average')
    )
    recoveries_figure.add_trace(
        go.Scatter(x=recoveries_reported_df.index, y=recoveries_reported_df['7-Day Moving Average'],
                   name='7-Day Moving Average', line=dict(color='orange'))
    )

    confirmed_figure.show()
    deaths_figure.show()
    recoveries_figure.show()