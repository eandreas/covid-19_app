import plotly.graph_objects as go

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


""" # prepare figure for daily confirmed cases
fig_new_conf = px.bar(df, x="date", y=["new_conf"], barmode="group")
fig_new_conf.update_layout(title_text='Daily confirmed cases - Switzerland')
fig_new_conf.update_layout(showlegend=False)
#fig_new_conf.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
#fig_new_conf.update_traces(marker_color='indianred', marker_line_color='rgb(8,48,107)',
#                  marker_line_width=0, opacity=0.6) """