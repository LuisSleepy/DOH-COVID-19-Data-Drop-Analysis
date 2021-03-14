"""
Checks for the lack of information regarding date of onset of illness and date of specimen collection of confirmed
COVID-19 cases in the Philippines

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

# Assumes checking the data drop the next day after latest posting date
yesterday = (dt.today() - td(days=1)).strftime("%Y%m%d")

case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'
df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 19], low_memory=False)

missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region', 'ProvRes': 'Unknown '

                                                                                                       'Province'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

# No date of onset of illness
number_of_no_onset = df_case_info['DateOnset'].isna().sum()
print("Initial count of cases with no date of onset of illness:",  number_of_no_onset)
df_case_info = df_case_info[df_case_info['DateOnset'].isna()]
no_onset = pd.pivot_table(df_case_info, index='ProvRes', aggfunc='size')
no_onset = no_onset.sort_values(ascending=False)
no_onset.to_csv('DOH COVID-19 Cases with No Date of Onset of Illness ' + yesterday + '.csv')

# No date of onset of illness and also no date of specimen collection
number_no_onset_no_specimen = (df_case_info['DateOnset'].isna() & df_case_info['DateSpecimen'].isna()).sum()
print("No date of onset of illness and no date of specimen collection:", number_no_onset_no_specimen)

# Replacing date of onset of illness with date of specimen collection
df_case_info['DateOnset'] = df_case_info['DateOnset'].mask(pd.isnull, df_case_info['DateSpecimen'])
number_of_no_onset = df_case_info['DateOnset'].isna().sum()
print("Revised count of cases with no date of illness:",  number_of_no_onset)

# Final cases listed in the csv file are those with no date of onset of illness and no date of specimen collection
df_case_info = df_case_info[df_case_info['DateOnset'].isna()]
no_dates = pd.pivot_table(df_case_info, index='ProvRes',  aggfunc='size')
no_dates = no_dates.sort_values(ascending=False)
no_dates.to_csv('DOH COVID-19 Cases with No Date of Onset of Illness (Absolute) ' + yesterday + '.csv')