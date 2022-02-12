import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from multi_page_app.app import app

df1 = pd.read_csv(
    '/Users/limchernyao/PycharmProjects/comp0034-cw1-i-team10/multi_page_app/apps/page2/datasets/business-demographics-updated.csv')
df2 = pd.read_csv(
    '/Users/limchernyao/PycharmProjects/comp0034-cw1-i-team10/multi_page_app/apps/page2/datasets/business-survival-rates-updated.csv')

app.layout = dbc.Container([
    html.Br(),

    dbc.Row(
        dbc.Col(html.H2("Comparison Graphs"),
                id='title')
    ),

    dbc.Row(
        dbc.Col(html.H5("Select 2 boroughs and a year between 2004-2018 to compare statistics"))
    ),

    dbc.Row(
        dcc.Dropdown(id='bar_type',
                     options=[
                         {'label': 'Survival rates', 'value': 'Survival rates'},
                         {'label': 'Survival numbers', 'value': 'Survival numbers'}],
                     multi=False,
                     searchable=False,
                     placeholder='Select the statistic to be compared...',
                     #clearable=False
                     style={"width": "55%", "color": "black"}
                     )
    ),

    dbc.Row(
        dcc.Dropdown(id='select_borough1',
                     options=[{'label':x, 'value':x} for x in df1.area.unique()],
                     multi=False,
                     searchable=True,
                     search_value='',
                     placeholder='Select the first borough to compare...',
                     #clearable=False
                     style={"width": "55%", "color": "black"}
                     )
    ),

    dbc.Row(
        dcc.Dropdown(id='select_borough2',
                     options=[{'label':x, 'value':x} for x in df1.area.unique()],
                     multi=False,
                     searchable=True,
                     search_value='',
                     placeholder='Select the second borough to compare...',
                     #clearable=False
                     style={"width": "55%", "color": "black"}
                     )
    ),

    dbc.Row(
        dcc.Dropdown(id='select_year',
                     options=[{'label':x, 'value':x} for x in df1.year.unique()],
                     multi=False,
                     searchable=True,
                     search_value='',
                     placeholder='Select a year between 2004-2018...',
                     #clearable=False
                     style={"width": "55%", "color": "black"}
                     )
    ),

    dbc.Row(children=[
        dbc.Col(width=6, children=[
            dcc.Graph(id='bar1')
        ], style={'margin':'0'}),
        dbc.Col(width=6, children=[
            dcc.Graph(id='bar2')
        ], style={'margin':'0'})
    ]),

])

@app.callback(
    [Output(component_id='survival_rate_bar', component_property='figure'),
     Input(component_id='bar_type', component_property='value'),
     Input(component_id='select_borough1', component_property='value'),
     Input(component_id='select_borough2', component_property='value'),
     Input(component_id='select_year', component_property='value')]
)

def survival_rate_bar(type, borough1, borough2, year_chosen):

    if type == "Survival rates":

        dff1 = df1.copy()
        dff1 = dff1[dff1["year"] == year_chosen]
        dff1 = dff1[dff1["area"] == borough1]

        dfff1 = df1.copy()
        dfff1 = dfff1[dfff1["year"] == year_chosen]
        dfff1 = dfff1[dfff1["area"] == borough2]

        fig1 = px.bar(
            data_frame=dff1,
            x='birth-death_rate',
            y='area',
            orientation='h',
            barmode='group',
        )

        fig2 = px.bar(
            data_frame=dfff1,
            x='birth-death_rate',
            y='area',
            orientation='h',
            barmode='group',
        )

        return [fig1], [fig2]

    else:

        dff2 = df2.copy()
        dff2 = dff2[dff2["year"] == year_chosen]
        dff2 = dff2[dff2["area"] == borough1]

        dfff2 = df2.copy()
        dfff2 = dfff2[dfff2["year"] == year_chosen]
        dfff2 = dfff2[dfff2["area"] == borough2]

        survival_rates = ['1_year_survival_rate', '2_year_survival_rate', '3_year_survival_rate',
                          '4_year_survival_rate', '5_year_survival_rate']

        fig1 = px.bar(
            data_frame=dff2,
            x=survival_rates,
            y='area',
            orientation='h',
            barmode='group'
        )

        fig2 = px.bar(
            data_frame=dfff2,
            x=survival_rates,
            y='area',
            orientation='h',
            barmode='group'
        )

        return [fig1], [fig2]



if __name__ == '__main__':
    app.run_server(debug=True)