# -*- coding: utf-8 -*-
import dash
#import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as spl
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt
from dataloader import get_data, get_BAG_report_data, get_BAG_test_data, stretch_data_frames, download_BAG_test_data
from colors import *
from constants import CANTONS, DAY_IN_NS
from tools import *
import figure_creator as fc

external_stylesheets = [
    dbc.themes.YETI,
    #'https://use.fontawesome.com/releases/v5.9.0/css/all.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = get_data()
df_bag_test = get_BAG_test_data()
df_bag_report = get_BAG_report_data()
df, df_bag_test, df_bag_report = stretch_data_frames([df, df_bag_test, df_bag_report])

fig_new_conf = fc.get_daily_new_conf_bars_only(df)
fig_new_conf_zoomed = fc.get_daly_new_conf(df, df_bag_test)
fig_tests_zoomed = fc.get_pcr_tests(df_bag_test)
fig_hosp_zoomed = fc.get_hospitalizations(df)
fig_pand_prog = fc.get_pand_prog(df)

fig_bag_new_conf = fc.get_daily_new_conf_aei(df, df_bag_report)

#fig_map = fc.get_map_figure()

NAVBAR = dbc.NavbarSimple(
    brand="COVID-19 Pandemic - Switzerland",
    brand_href="#",
    color="primary",
    dark=True,
)

TIME_WINDOW_SELECTION = dbc.Card(
    [
        dbc.CardHeader("Wahl des Zeitfensters"),
        dbc.CardBody(
            [
                html.P(
                    "Stelle das gewünschte Zeitfenster ein. Die Auswahl wirkt sich auf die unten angezeigten Kennzahlen und Graphen aus.",
                    className="card-text",
                ),
                html.Hr(),
                dcc.RangeSlider(
                    id='date-range-slider',
                    min=df['date'].min().value,
                    max=df['date'].max().value,
                    step=DAY_IN_NS,
                    value=[yyyymmdd2ns('20200601'), df['date'].max().value],
                    allowCross=False,
                    updatemode='drag',
                    marks = {
                        df.date.min().value: df.date.min().strftime('%d.%m.%Y'),
                        yyyymmdd2ns('20200601'): '1. Juni',
                        df.date.max().value: df.date.max().strftime('%d.%m.%Y')
                    },
                    #persistence=True
                ),
                html.Hr(),
                dcc.Graph(
                    id="new_conf",
                    figure=fig_new_conf,
                    config={
                        'displayModeBar': False,
                        #'staticPlot': True
                    }
                )
            ]
        ),
    ]
)

BAG_CONF = dbc.Card(
    [
        dbc.CardHeader("Tägliche Fallzahlen - OpenZH versus BAG"),
        dbc.CardBody(
            [
                dcc.Graph(
                    id="new_conf_bag",
                    figure=fig_bag_new_conf,
                    config={
                        'displayModeBar': False,
                        #'staticPlot': True
                    }
                )
            ]
        ),
    ], className="mt-3"
)

NEWLY_CONFIRMED_CASES = dbc.Card(
    [
        dbc.CardHeader("Neu bestätigte Fälle"),
        dbc.CardBody(
            [
                dcc.Graph(
                    id='new_conf_zoomed',
                    figure=fig_new_conf_zoomed,
                    config={
                        'displayModeBar': False,
                    #'staticPlot': True
                    }
                ),
            ]
        ),
    ], className="mt-3"
)

TESTS_AND_POSITIVITY_RATE = dbc.Card(
    [
        dbc.CardHeader("Durchgeführte Tests und Positivitätsrate"),
        dbc.CardBody(
            [
                dcc.Graph(
                    id='tests_zoomed',
                    figure=fig_tests_zoomed,
                    config={
                        'displayModeBar': False,
                        #'staticPlot': True
                    }
                ),
            ]
        ),
    ], className="mt-3"
)

HOSPITALIZATIONS = dbc.Card(
    [
        dbc.CardHeader("Hospitalisierungen"),
        dbc.CardBody(
            [
                dcc.Graph(
                    id='hosp_zoomed',
                    figure=fig_hosp_zoomed,
                    config={
                        'displayModeBar': False,
                        #'staticPlot': True
                    }
                )
            ]
        ),
    ], className="mt-3"
)

""" MAP = dbc.Card(
    [
        dbc.CardHeader("Map"),
        dbc.CardBody(
            [
                dcc.Graph(
                    id='map',
                    figure=fig_map,
                    config={
                        'displayModeBar': False,
                        #'staticPlot': True
                    }
                )
            ]
        ),
    ], className="mt-3"
) """

BODY = dbc.Container(
    [
        TIME_WINDOW_SELECTION,
        BAG_CONF,
        #MAP,
        NEWLY_CONFIRMED_CASES,
        TESTS_AND_POSITIVITY_RATE,
        HOSPITALIZATIONS
    ],
    className="mt-3 mb-3",
)

app.layout = html.Div(children=[
    NAVBAR,
    BODY
])

# update color dependent on date range slider (selected time window)
@app.callback(
    Output("new_conf", "figure"),
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
    return fig_new_conf

@app.callback(
    [
        Output("new_conf_zoomed", "figure"),
        Output("tests_zoomed", "figure"),
        Output("hosp_zoomed", "figure")
    ],
    [
        Input("date-range-slider", "value")
    ],
)
def update_zoomed_figure(date_range_slider):
    start_date = pd.to_datetime(date_range_slider[0])
    end_date = pd.to_datetime(date_range_slider[1])
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    df_zoomed = df.loc[mask]
    df_bag_test_zoomed = df_bag_test.loc[mask]

    #fig_new_conf_zoomed = fc.get_daly_new_conf(df_zoomed, df_bag_test_zoomed)
    y1_max = 1.05 * max(df_zoomed.new_conf.max(), df_zoomed.new_conf_SMA7.max())
    y2_max = 1.05 * df_bag_test_zoomed.new_tests_SMA7.max()
    fig_new_conf_zoomed.update_xaxes(range=[start_date, end_date])
    fig_new_conf_zoomed.update_yaxes(range=[0, y1_max], secondary_y=False)
    fig_new_conf_zoomed.update_yaxes(range=[0, y2_max], secondary_y=True)
    fig_new_conf_zoomed.update_layout(transition_duration=500)

    fig_tests_zoomed = fc.get_pcr_tests(df_bag_test_zoomed)
    fig_tests_zoomed.update_layout(transition_duration=500)

    fig_hosp_zoomed = fc.get_hospitalizations(df_zoomed)
    fig_hosp_zoomed.update_layout(transition_duration=500)

    return fig_new_conf_zoomed, fig_tests_zoomed, fig_hosp_zoomed

if __name__ == '__main__':
    # True for hot reloading
    app.run_server(debug=True)