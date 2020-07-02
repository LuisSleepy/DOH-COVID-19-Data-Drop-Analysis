import pandas as pd
import plotly.graph_objects as go

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# The csv file from DOH updated every day at 10:00 AM (Philippine Standard Time)
# I encounter error in downloading the file directly since it comes from Google Drive
case_info = 'DOH COVID Data Drop_ 20200702 - 04 Case Information.csv'

df_case_info = pd.read_csv(case_info, parse_dates=[4, 5, 6, 7, 8, 10, 18], low_memory=False)
# Fill those rows with no values in RemovalType as "Active" and in RegionRes as "Unknown Region"
df_case_info = df_case_info.fillna({'RemovalType': 'Active', 'RegionRes': 'Unknown Region'})

# Automation of checking the number of cases per region
# Used for the weekly update of COVID-19 cases per region in Ang Pahayagang Plaridel
confirmed_cases = pd.pivot_table(df_case_info, index='RegionRes', aggfunc='size')
all_cases = pd.pivot_table(df_case_info, index='RegionRes', columns='RemovalType', aggfunc='size')
all_cases['Confirmed'] = confirmed_cases
all_cases = all_cases.fillna({'Active': 0, 'Died': 0, 'Recovered': 0, 'Confirmed': 0})
all_cases = all_cases.astype({'Active': 'int64', 'Died': 'int64', 'Recovered': 'int64'})
all_cases.to_excel('DOH COVID-19 Cases Per Region - 20200702.xlsx')

# Graphing the number of cases per day based on confirmation day
confirmed_series = df_case_info.pivot_table(index=df_case_info['DateRepConf'], aggfunc='size')

frame = {'Confirmed': confirmed_series}
confirmed_reported_df = pd.DataFrame(frame)

confirmed_reported_df['Daily Average'] = \
    confirmed_reported_df['Confirmed'].expanding(min_periods=1).mean().round(0)

confirmed_reported_df['7-Day Moving Average'] = \
    confirmed_reported_df['Confirmed'].rolling(window=7).mean().round(0)

fig = go.Figure()

fig.add_trace(
    go.Bar(x=confirmed_reported_df.index, y=confirmed_reported_df['Confirmed'], name='Confirmed')
)

fig.add_trace(
    go.Scatter(x=confirmed_reported_df.index, y=confirmed_reported_df['Daily Average'], name='Daily Average')
)

fig.add_trace(
    go.Scatter(x=confirmed_reported_df.index, y=confirmed_reported_df['7-Day Moving Average'],
               name='7-Day Moving Average', line=dict(color='orange'))
)

fig.show()
