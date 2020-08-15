import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_daily_new_conf_bars_only(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.date, y=df.new_conf))
    # Set x-axis title
    fig.update_xaxes(title_text='date')
    # Set y-axes titles
    fig.update_yaxes(title_text='Newly confirmed COVID-19 cases')
    fig.update_layout(
        title=None,
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
        title='Daily new confirmed COVID-19 cases - Switzerland',
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)')
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
        title='Daily PCR-tests and outcome - Switzerland',
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)')
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
        title='Hospitalizations',
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor='rgba(255, 255, 255, 0.7)')
    )
    return fig