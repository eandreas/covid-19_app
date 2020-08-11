# -*- coding: utf-8 -*-
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as spl
import pandas as pd
import datetime as dt
from constants import CANTONS
from dataloader import get_CH_data_total
from colors import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = get_CH_data_total()

# cut some old date
start_date = '20190601'
df = df[df['date'] >= start_date]

# prepare figure for daily confirmed cases
fig_new_conf = px.bar(df, x="date", y=["new_conf"], barmode="group")
fig_new_conf.update_layout(showlegend=False)
fig_new_conf.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
fig_new_conf.update_traces(marker_color='indianred', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0, opacity=0.6)
fig_new_conf.update_layout(title_text='Daily confirmed cases - Switzerland')

# prepare figure for daily confirmed cases (zoomed)
fig_new_conf_zoomed = px.bar(df, x="date", y=["new_conf"], barmode="group")
fig_new_conf_zoomed.update_layout(showlegend=False)
fig_new_conf_zoomed.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
fig_new_conf_zoomed.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0, opacity=0.6)
fig_new_conf_zoomed.update_layout(title_text='Daily confirmed cases (zoomed) - Switzerland')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-19 Cases and Analysis',
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    html.Div(
        style={'textAlign': 'center', 'color': colors['text']},
        children='Andreas Dorta'
    ),
    dcc.RangeSlider(
        id='date-range-slider',
        min=df['date'].min().value,
        max=df['date'].max().value,
        step=864e11,
        value=[df['date'].min().value, df['date'].max().value],
        allowCross=False,
        updatemode='drag'
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

# update new_conf figure
@app.callback(
    Output("new_conf", "figure"),
    [
        Input("date-range-slider", "value")
    ],
)
def update_figure(date_range_slider):
    cols = []
    for i in range(df['date'].min().value, df['date'].max().value + int(864e11), int(864e11)):
        if i >= int(date_range_slider[0]) and i <= int(date_range_slider[1]):
            cols.append('indianred')
        else:
            cols.append('lightsalmon')

    fig_new_conf.update_traces(marker_color=cols)
    return fig_new_conf

# update new_conf_zoomed figure
@app.callback(
    Output("new_conf_zoomed", "figure"),
    [
        Input("date-range-slider", "value")
    ],
)
def update_zoomed_figure(date_range_slider):

    start_date = pd.to_datetime(date_range_slider[0], unit = 'ns')
    end_date = pd.to_datetime(date_range_slider[1], unit = 'ns')
    
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df_zoomed = df.loc[mask]
    
    fig_new_conf_zoomed = px.bar(df_zoomed, x="date", y=["new_conf"], barmode="group")
    fig_new_conf_zoomed.update_layout(showlegend=False)
    fig_new_conf_zoomed.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
    fig_new_conf_zoomed.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0, opacity=0.6)
    fig_new_conf_zoomed.update_layout(title_text='Daily confirmed cases (zoomed) - Switzerland')
    return fig_new_conf_zoomed

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    # True for hot reloading
    app.run_server(debug=True)