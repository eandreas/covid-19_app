# -*- coding: utf-8 -*-
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime as dt
from constants import CANTONS
from dataloader import get_CH_data_total
from colors import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = get_CH_data_total()

start_date = '20200601'
fig = px.bar(df[df['date'] >= start_date], x="date", y=["new_conf"], barmode="group")
fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(title_text='New confirmed cases - Switzerland')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-19 Cases and Analysis',
        style={'textAlign': 'center', 'color': colors['text']}
    ),

    html.Div(
        style={'textAlign': 'center', 'color': colors['text']},
        children='Andreas Dorta'
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.RangeSlider(
        id='date-range-slider',
        min=df['date'].min().value,
        max=df['date'].max().value,
        step=1,
        value=[df['date'].min().value, df['date'].max().value],
        allowCross=False,
        updatemode='drag'
    )
])

#@app.callback(
#    dash.dependencies.Output('output-container-range-slider', 'children'),
#    [dash.dependencies.Input('my-range-slider', 'value')])
#def update_output(value):
#    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    # True for hot reloading
    app.run_server(debug=True)