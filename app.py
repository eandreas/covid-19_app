# -*- coding: utf-8 -*-
import dash
#import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as spl
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt
from dataloader import get_data, get_BAG_test_data, stretch_data_frames, download_BAG_test_data
from colors import *
from constants import CANTONS, DAY_IN_NS
from tools import *
import figure_creator as fc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
#app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

df = get_data()
df_bag_test = get_BAG_test_data()
df, df_bag_test = stretch_data_frames([df, df_bag_test])

fig_new_conf = fc.get_daily_new_conf_bars_only(df)
fig_new_conf_zoomed = fc.get_daly_new_conf(df, df_bag_test)
fig_tests_zoomed = fc.get_pcr_tests(df_bag_test)
fig_hosp_zoomed = fc.get_hospitalizations(df)

app.layout = html.Div([
    html.H1(
        'COVID-19 Cases and Analysis',
    ),
    dcc.DatePickerRange(
        id='date-range-picker',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        display_format='DD.MM.YYYY',
        start_date_placeholder_text='DD.MM.YYYY',
        disabled=True
    ),
    dcc.RangeSlider(
        id='date-range-slider',
        min=df['date'].min().value,
        max=df['date'].max().value,
        step=DAY_IN_NS,
        value=[yyyymmdd2ns('20200601'), df['date'].max().value],
        allowCross=False,
        updatemode='drag',
        marks = {
            yyyymmdd2ns('20200601'): '1. Juni'
        },
        #persistence=True
    ),
    dcc.Graph(
        id='new_conf',
        figure=fig_new_conf
    ),
    dcc.Graph(
        id='new_conf_zoomed',
        figure=fig_new_conf_zoomed
    ),
    dcc.Graph(
        id='tests_zoomed',
        figure=fig_tests_zoomed
    ),
    dcc.Graph(
        id='hosp_zoomed',
        figure=fig_hosp_zoomed
    )
])

# update color dependent on date range slider (selected time window)
@app.callback(
    [
        Output("new_conf", "figure"),
        Output("date-range-picker", "start_date"),
        Output("date-range-picker", "end_date")
    ],
    [
        Input("date-range-slider", "value")
    ],
)
def update_figure(date_range_slider):
    n = int((df['date'].max().value - df['date'].min().value) / DAY_IN_NS + 1)
    cols = [colors['unselected_bars']] * n
    start = int((date_range_slider[0] - df['date'].min().value) / DAY_IN_NS)
    end = int((date_range_slider[1] - df['date'].min().value) / DAY_IN_NS)
    for i in range(start, end + 1):
        cols[i] = colors['selected_bars']
    fig_new_conf.update_traces(marker_color=cols)
    return fig_new_conf, pd.to_datetime(date_range_slider[0]), pd.to_datetime(date_range_slider[1])

@app.callback(
    [
        Output("new_conf_zoomed", "figure"),
        Output("tests_zoomed", "figure"),
        Output("hosp_zoomed", "figure")
    ],
    [
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date")
    ],
)
def update_zoomed_figure(start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    df_zoomed = df.loc[mask]
    df_bag_test_zoomed = df_bag_test.loc[mask]
    fig_new_conf_zoomed = fc.get_daly_new_conf(df_zoomed, df_bag_test_zoomed)
    fig_new_conf_zoomed.update_layout(transition_duration=500)

    fig_tests_zoomed = fc.get_pcr_tests(df_bag_test_zoomed)
    fig_tests_zoomed.update_layout(transition_duration=500)

    fig_hosp_zoomed = fc.get_hospitalizations(df_zoomed)
    fig_hosp_zoomed.update_layout(transition_duration=500)

    return fig_new_conf_zoomed, fig_tests_zoomed, fig_hosp_zoomed

if __name__ == '__main__':
    # True for hot reloading
    app.run_server(debug=True)