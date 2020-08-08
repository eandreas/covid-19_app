# -*- coding: utf-8 -*-
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# assume you have a "wide-form" data frame with no index
# see https://plotly.com/python/wide-form/ for more options
df = pd.DataFrame({"x": [1, 2, 3], "SF": [4, 1, 2], "Montreal": [2, 4, 5]})

fig = px.bar(df, x="x", y=["SF", "Montreal"], barmode="group")



# all cantons including FL
CANTONS = {
    "01": "AG",
    "02": "AI",
    "03": "AR",
    "04": "BE",
    "05": "BL",
    "06": "BS",
    "07": "FL",
    "08": "FR",
    "09": "GE",
    "10": "GL",
    "11": "GR",
    "12": "JU",
    "13": "LU",
    "14": "NE",
    "15": "NW",
    "16": "OW",
    "17": "SG",
    "18": "SH",
    "19": "SO",
    "20": "SZ",
    "21": "TG",
    "22": "TI",
    "23": "UR",
    "24": "VD",
    "26": "VS",
    "27": "ZG",
    "28": "ZH"
}

def add_diff_col(df, col, new_col):
    df[new_col] = df[col].diff()
    return df

folder_v2 = '/Users/eandreas/projects/dev/covid-19/openZH_covid-19/fallzahlen_kanton_total_csv_v2'
prefix_c_fn = 'COVID19_Fallzahlen_Kanton'
prefix_fn = 'COVID19_Fallzahlen'
postfix_fn = 'total.csv'

dfs = []

for c in CANTONS.values():
    
    #c = "ZH"
    
    # remove next line in final version
    #print(c)
    
    if (c == "FL"):
        file = f'{folder_v2}/{prefix_fn}_{c}_{postfix_fn}'
    else:
        file = f'{folder_v2}/{prefix_c_fn}_{c}_{postfix_fn}'
    
    dfc = pd.read_csv(file)
    add_diff_col(dfc, 'ncumul_tested', 'new_tested')
    add_diff_col(dfc, 'ncumul_conf', 'new_conf')
    add_diff_col(dfc, 'ncumul_deceased', 'new_deceased')
    add_diff_col(dfc, 'current_hosp', 'delta_hosp')
    add_diff_col(dfc, 'current_icu', 'delta_icu')
    add_diff_col(dfc, 'current_vent', 'delta_vent')
    add_diff_col(dfc, 'current_isolated', 'delta_isolated')
    add_diff_col(dfc, 'current_quarantined', 'delta_quarantined')
    add_diff_col(dfc, 'ncumul_released', 'new_released')
    dfs.append(dfc)
    
    # comment the next line to get all cantons
    #break
    
df = pd.concat(dfs)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

df_ch = df.groupby('date').sum()
df_ch.reset_index(level=0, inplace=True)

colors = {
    'background': '#ffffff',
    'text': '#7FDBFF'
}

start_date = '20200601'

fig = px.bar(df_ch[df_ch['date'] >= start_date], x="date", y=["new_conf"], barmode="group")

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
        min=df_ch['date'].min().value,
        max=df_ch['date'].max().value,
        step=1,
        value=[df_ch['date'].min().value, df_ch['date'].max().value],
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