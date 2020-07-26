import pandas as pd
import plotly.graph_objects as go
import numpy as np

# These are modifications in displaying the DataFrame in the terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

testing_info = "DOH COVID Data Drop_ 20200725 - 07 Testing Aggregates.csv"

df_testing_info = pd.read_csv(testing_info)
per_facility = df_testing_info.groupby("facility_name")
