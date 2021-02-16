"""
Actual number of COVID-19 cases per day based on Date of Onset of Illness and Date of Specimen Collection

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

# Temporary use the posting date
today = dt.date(dt.today()).strftime("%Y%m%d")

# Opening the .csv file
case_info = 'DOH COVID Data Drop_ ' + today + ' - 04 Case Information.csv'
df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

# print(df_case_info.head())
# print(df_case_info.info(verbose=True))
number_of_no_date_illness = df_case_info['DateOnset'].isna().sum()
print(number_of_no_date_illness)

# Replacing date of onset of illness with date of specimen collection
df_case_info['DateOnset'] = df_case_info['DateOnset'].mask(pd.isnull, df_case_info['DateSpecimen'])
# print(df_case_info.info(verbose=True))
number_of_no_date_illness = df_case_info['DateOnset'].isna().sum()
print(number_of_no_date_illness)