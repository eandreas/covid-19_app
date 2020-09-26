import plotly.graph_objects as go
import constants
from plotly.subplots import make_subplots
from colors import *

import pandas as pd

def get_daily_new_conf_bars_only(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.date, y=df.new_conf))
    # Set x-axis title
    fig.update_xaxes(
        title_text='date',
        #linecolor=colors['axis']
    )
    # Set y-axes titles
    fig.update_yaxes(title_text='Newly confirmed COVID-19 cases')
    fig.update_layout(
        title=None,
        #font_color=colors['axis_label'],
        margin=dict(t=10, b=10, l=60, r=0, pad=0),
        template=constants.FIGURE_TEMPLATE
    )
    return fig

def get_daly_new_conf(df, df_bag_test):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(name='PCR-tests performed (SMA7)', x=df_bag_test.date, y=df_bag_test.new_tests_SMA7), secondary_y=True)
    fig.add_trace(go.Bar(name='daily new confirmed COVID-19 cases', x=df.date, y=df.new_conf), secondary_y=False)
    fig.add_trace(go.Scatter(name='Daily new confirmed COVID-19 cases (SMA7)', x=df.date, y=df.new_conf_SMA7, fill='tonexty'), secondary_y=False)
    # Set x-axis title
    fig.update_xaxes(title_text='date')
    # Set y-axes titles
    fig.update_yaxes(title_text='Newly confirmed COVID-19 cases', secondary_y=False)
    fig.update_yaxes(title_text='Number of PCR-tests', secondary_y=True)
    fig.update_yaxes(rangemode = 'tozero')
    fig.update_layout(
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)'),
        title=None,
        margin=dict(t=10, b=10, l=60, r=0, pad=0),
        template=constants.FIGURE_TEMPLATE
    )
    return fig

def get_pcr_tests(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(name='positive', x=df.date, y=df.positive), secondary_y=False)
    fig.add_trace(go.Bar(name='negative', x=df.date, y=df.negative), secondary_y=False)
    fig.add_trace(go.Scatter(name='daily tests (SMA7)', x=df.date, y=df.new_tests_SMA7, fill='tonexty'), secondary_y=False)
    fig.add_trace(go.Scatter(name='positivity rate (SMA7)', x=df.date, y=df.pos_rate_SMA7), secondary_y=True)
    # Set x-axis title
    fig.update_xaxes(title_text='date')
    # Set y-axes titles
    fig.update_yaxes(title_text='Number of PCR-tests', secondary_y=False)
    fig.update_yaxes(title_text='positivity rate / %', secondary_y=True)
    fig.update_yaxes(rangemode = 'tozero')
    fig.update_layout(
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)'),
        title=None,
        margin=dict(t=10, b=10, l=60, r=0, pad=0),
        template=constants.FIGURE_TEMPLATE
    )
    return fig

def get_hospitalizations(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(name='new confirmed (SMA7)', x=df.date, y=df.new_conf_SMA7), secondary_y=True)
    fig.add_trace(go.Bar(name='ventilated', x=df.date, y=df.current_vent), secondary_y=False)
    fig.add_trace(go.Bar(name='intensive', x=df.date, y=df.current_icu), secondary_y=False)
    fig.add_trace(go.Bar(name='regular', x=df.date, y=(df.current_hosp - df.current_icu - df.current_vent)), secondary_y=False)
    fig.add_trace(go.Scatter(name='hospitalized (SMA7)', x=df.date, y=df.current_hosp_SMA7), secondary_y=False)
    # Set x-axis title
    fig.update_xaxes(title_text='date')
    # Set y-axes titles
    fig.update_yaxes(title_text='Current hospitalizations', secondary_y=False)
    fig.update_yaxes(title_text='Newly confirmed COVID-19 cases', secondary_y=True)
    fig.update_yaxes(rangemode = 'tozero')
    fig.update_layout(
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)'),
        title=None,
        margin=dict(t=10, b=10, l=60, r=0, pad=0),
        template=constants.FIGURE_TEMPLATE
    )
    return fig

def get_pand_prog(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='', x=df.ncumul_conf, y=df.new_conf_SMA7))
    # Set x-axis title
    fig.update_xaxes(title_text='Total reported cases (SMA7)')
    # Set y-axes titles
    fig.update_yaxes(title_text='Daily reported cases')
    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")
    #fig.update_xaxes(rangemode = 'tozero')
    #fig.update_yaxes(rangemode = 'tozero')
    fig.update_layout(
        title=None,
        margin=dict(t=10, b=10, l=60, r=0, pad=0),
        template=constants.FIGURE_TEMPLATE
    )
    return fig

def get_map_figure():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

    for col in df.columns:
        df[col] = df[col].astype(str)

    df['text'] = df['state'] + '<br>' + \
        'Beef ' + df['beef'] + ' Dairy ' + df['dairy'] + '<br>' + \
        'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
        'Wheat ' + df['wheat'] + ' Corn ' + df['corn']

    fig = go.Figure(data=go.Choropleth(
        locations=df['code'],
        z=df['total exports'].astype(float),
        locationmode='USA-states',
        colorscale='Reds',
        autocolorscale=False,
        text=df['text'], # hover text
        marker_line_color='white', # line markers between states
        colorbar_title="Millions USD"
    ))
    
    fig.update_layout(
        title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    return fig
