import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# The csv file from DOH updated every day at 10:00 AM (Philippine Standard Time)
# I encounter error in downloading the file directly since it comes from Google Drive
yesterday = (datetime.date(datetime.today()) - timedelta(days=1)).strftime("%Y%m%d")
case_info = 'DOH COVID Data Drop_ ' + yesterday + ' - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)

missing_prov = df_case_info['ProvRes'].isna()
mapping_NCR_ROF = dict({'NCR': 'NCR', 'ROF': 'ROF'})
df_case_info.loc[missing_prov, 'ProvRes'] = df_case_info.loc[missing_prov, 'RegionRes'].map(mapping_NCR_ROF)
df_case_info = df_case_info.fillna({'RemovalType': 'ACTIVE', 'RegionRes': 'Unknown Region', 'ProvRes': 'Unknown Province'})
df_case_info['RemovalType'] = df_case_info['RemovalType'].str.upper()

filtered_data = df_case_info[(df_case_info['ProvRes'] == 'DAVAO DEL SUR')]
confirmed = filtered_data.pivot_table(index='DateRepConf', aggfunc='size')
active = df_case_info[(df_case_info['RemovalType'] == 'ACTIVE')]
active = active.pivot_table(index='DateRepConf', aggfunc='size')

# Take note: The figure for Active cases showcases how many of the confirmed cases each day are still considered
# active cases
confirmed_frame = {'Confirmed': confirmed}

filtered_df = pd.DataFrame(confirmed_frame)
filtered_df['Active'] = active
filtered_df = filtered_df.fillna(0)
filtered_df = filtered_df.astype({'Active': 'int64'})
# filtered_df = pd.DataFrame(confirmed_frame, active_frame)

filtered_df['Confirmed Daily Average'] = filtered_df['Confirmed'].expanding(min_periods=1).mean().round(0)
filtered_df['Confirmed 7-Day Moving Average'] = filtered_df['Confirmed'].rolling(window=7).mean().round(0)

filtered_df['Active Daily Average'] = filtered_df['Active'].expanding(min_periods=1).mean().round(0)
filtered_df['Active 7-Day Moving Average'] = filtered_df['Active'].rolling(window=7).mean().round(0)

confirmed_figure = go.Figure()
active_figure = go.Figure()

confirmed_figure.add_trace(
    go.Bar(x=filtered_df.index, y=filtered_df['Confirmed'], name='Confirmed')
)

confirmed_figure.add_trace(
    go.Scatter(x=filtered_df.index, y=filtered_df['Confirmed Daily Average'], name='Daily Average')
)

confirmed_figure.add_trace(
    go.Scatter(x=filtered_df.index, y=filtered_df['Confirmed 7-Day Moving Average'], name='7-Day Average')
)

active_figure.add_trace(
    go.Bar(x=filtered_df.index, y=filtered_df['Active'], name='Active')
)

active_figure.add_trace(
    go.Scatter(x=filtered_df.index, y=filtered_df['Active Daily Average'], name='Daily Average')
)

active_figure.add_trace(
    go.Scatter(x=filtered_df.index, y=filtered_df['Active 7-Day Moving Average'], name='7-Day Moving Average')
)

confirmed_figure.show()
active_figure.show()

