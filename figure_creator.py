import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_bar(x, y, title=None):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y))
    fig.update_layout(
        title=title,
        hovermode="x unified"
    )
    return fig

def get_stacked_bar(x1, y1, x2, y2, title):
    fig = go.Figure(data=[
        go.Bar(name='positive', x=x1, y=y1),
        go.Bar(name='negative', x=x2, y=y2)
    ])
    fig.update_layout(
        title=title,
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01)
    )
    return fig

def get_bar_with_SMA(x_bar, y_bar, x_sma, y_sma, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_bar, y=y_bar))
    fig.add_trace(go.Scatter(x=x_sma, y=y_sma, fill='tonexty'))
    fig.update_layout(
        title=title,
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01)
    )
    return fig


def get_stacked_bar_2ys(x1, y1, x2, y2, x3, y3, x4, y4, title):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(name='positive', x=x1, y=y1), secondary_y=False,
    )
    fig.add_trace(
        go.Bar(name='negative', x=x2, y=y2), secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(name='daily tests (SMA7)', x=x3, y=y3, fill='tonexty'), secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(name='positivity rate (SMA7)', x=x4, y=y4),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text='date')

    # Set y-axes titles
    fig.update_yaxes(title_text='Number of PCR-tests', secondary_y=False)
    fig.update_yaxes(title_text='positivity rate / %', secondary_y=True)
    fig.update_yaxes(rangemode = 'tozero', secondary_y=True)

    fig.update_layout(
        title=title,
        barmode='stack',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01)
    )
    return fig
