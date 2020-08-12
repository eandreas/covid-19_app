# -*- coding: utf-8 -*-
import dash
#import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as spl
import pandas as pd
from datetime import datetime as dt
from dataloader import get_CH_data_total
from colors import *
from constants import *
from tools import *

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()

df = get_CH_data_total()

# cut some old date
start_date = '20190601'
df = df[df['date'] >= start_date]

# prepare figure for daily confirmed cases
fig_new_conf = px.bar(df, x="date", y=["new_conf"], barmode="group")
fig_new_conf.update_layout(title_text='Daily confirmed cases - Switzerland')
fig_new_conf.update_layout(showlegend=False)
#fig_new_conf.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
#fig_new_conf.update_traces(marker_color='indianred', marker_line_color='rgb(8,48,107)',
#                  marker_line_width=0, opacity=0.6)


# prepare figure for daily confirmed cases (zoomed)
fig_new_conf_zoomed = px.bar(df, x="date", y=["new_conf"], barmode="group")
fig_new_conf_zoomed.update_layout(title_text='Daily confirmed cases (zoomed) - Switzerland')
fig_new_conf_zoomed.update_layout(showlegend=False)
#fig_new_conf_zoomed.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
#fig_new_conf_zoomed.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                  marker_line_width=0, opacity=0.6)


app.layout = html.Div([
    html.H1(
        'COVID-19 Cases and Analysis',
        #style={'textAlign': 'center', 'color': colors['text']}
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
        }
        #persistence=True
    ),
    dcc.Graph(
        id='new_conf',
        figure=fig_new_conf
    ),
    dcc.Graph(
        id='new_conf_zoomed',
        figure=fig_new_conf_zoomed
    )
])

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
    Output("new_conf_zoomed", "figure"),
    [
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date")
    ],
)
def update_zoomed_figure(start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    df_zoomed = df.loc[mask]
    
    fig_new_conf_zoomed = px.bar(df_zoomed, x="date", y=["new_conf"], barmode="group")
    fig_new_conf_zoomed.update_layout(showlegend=False)
    fig_new_conf_zoomed.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
    fig_new_conf_zoomed.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0, opacity=0.6)
    fig_new_conf_zoomed.update_layout(title_text='Daily confirmed cases (zoomed) - Switzerland')
    return fig_new_conf_zoomed

if __name__ == '__main__':
    # True for hot reloading
    app.run_server(debug=True)