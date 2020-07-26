import pandas as pd
import plotly.graph_objects as go
import numpy as np
from DOHDataAnalysis.DOHCaseInfo import df_case_info as dfci

confirmed_cases = dfci.pivot_table(dfci, index='DateRepConf', columns='RegionRes', aggfunc='size')
confirmed_cases = confirmed_cases.fillna(0)
confirmed_cases = confirmed_cases.astype(int)

graph = go.Figure()

daily_average = confirmed_cases['Region XI: Davao Region'].expanding(min_periods=1).mean().round(0)
moving_average = confirmed_cases['Region XI: Davao Region'].rolling(window=7).mean().round(0)

graph.add_trace(
    go.Bar(x=confirmed_cases.index, y=confirmed_cases['Region XI: Davao Region'], name='Confirmed Cases in Region XI: Davao Region')
)

graph.add_trace(
    go.Scatter(x=confirmed_cases.index, y=daily_average, name='Daily Average')
)

graph.add_trace(
    go.Scatter(x=confirmed_cases.index, y=moving_average, name='7-Day Moving Average', line=dict(color='orange'))
)

graph.show()