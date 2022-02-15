import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from multi_page_app.app import app

df1 = pd.read_csv(
    'apps/page1/datasets/business-demographics-updated.csv')
df2 = pd.read_csv(
    'apps/page1/datasets/business-survival-rates-updated.csv')

# This json file is sourceed from the London Data Store
# https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london?resource=9ba8c833-6370-4b11-abdc-314aa020d5e0

f = open(
    'apps/page1/datasets/london_boroughs.json')

geoj = json.load(f)

layout = dbc.Container([
    html.Br(),

    dbc.Row(
        dbc.Col(html.H2("Choropleth Map")
                , id='title')
    ),

    dbc.Row(
        dbc.Col(html.H5("Select the year on the dropdown menu that you want to explore and click on the boroughs to "
                        "learn more about the businesses there!"), className='text-muted')
    ),

    dbc.Row(
        dcc.Dropdown(id='slct_yr',
                     options=[
                         {"label": "2004", "value": 2004},
                         {"label": "2005", "value": 2005},
                         {"label": "2006", "value": 2006},
                         {"label": "2007", "value": 2007},
                         {"label": "2008", "value": 2008},
                         {"label": "2009", "value": 2009},
                         {"label": "2010", "value": 2010},
                         {"label": "2011", "value": 2011},
                         {"label": "2012", "value": 2012},
                         {"label": "2013", "value": 2013},
                         {"label": "2014", "value": 2014},
                         {"label": "2015", "value": 2015},
                         {"label": "2016", "value": 2016},
                         {"label": "2017", "value": 2017},
                         {"label": "2018", "value": 2018},
                         {"label": "2019", "value": 2019},
                     ],
                     multi=False,
                     value=2004,
                     clearable=False,
                     style={"width": "40%", "color": "black"}
                     )
    ),
    html.Em(children=[
        '*Data after 2019 is not available.*'
    ]
    ),
    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Graph(id='surv-graph')
        ], style={'margin': '0'}, xs=12, sm=12, md=10, lg=10, xl=5),
        dbc.Col(children=[
            dcc.Graph(id='map')
        ], style={'margin': '0'}, xs=12, sm=12, md=10, lg=10, xl=7)
    ]),
])


@app.callback(
    [Output('map', 'figure')],
    [Input('slct_yr', 'value')]
)
def update_map(option_slctd):
    dff1 = df1.copy()
    geojj = geoj.copy()
    dff1 = dff1[dff1["year"] == option_slctd]

    fig = px.choropleth_mapbox(
        data_frame=dff1,
        featureidkey='properties.code',
        locations='code',
        geojson=geojj,
        mapbox_style="carto-positron",
        color='birth-death_rate',
        hover_name='area',
        hover_data=['active_enterprises', 'births', 'birth_rate', 'death_rate', 'birth-death_rate'],
        color_continuous_scale='Viridis',
        custom_data=['area'],
        opacity=0.5,
        center={'lat': 51.509865, 'lon': -0.118092},
        title=('Birth Rate-Death Rate (%) of businesses in {}'.format(option_slctd)),
        labels={'birth-death_rate': '%'}
    )
    return [fig]


@app.callback(
    [Output('surv-graph', 'figure'),
     Input('map', 'clickData'),
     Input('slct_yr', 'value')]
)
def update_bar(clk_data, year):
    dff2 = df2.copy()

    if clk_data is None:
        dff2 = dff2[dff2["year"] == 2004]
        dff2 = dff2[dff2['area'] == 'City of London']

        survival_rates = ['1_year_survival_rate', '2_year_survival_rate', '3_year_survival_rate',
                          '4_year_survival_rate', '5_year_survival_rate']
        new_names = {'5_year_survival_rate': '5 Years', '4_year_survival_rate': '4 Years',
                     '3_year_survival_rate': '3 Years',
                     '2_year_survival_rate': '2 Years', '1_year_survival_rate': '1 Year'}

        fig1 = px.bar(dff2, x='area', y=survival_rates, barmode='group', orientation='v',
                      title='Business Survival Rates in City '
                            'of London after '
                            '2004',
                      labels={'area': '', 'variable': 'Years after 2004'})

        fig1.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                               legendgroup=new_names[t.name],
                                               hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                               ))
        return [fig1]
    else:
        dff2 = dff2[dff2["year"] == year]
        click_area = clk_data['points'][0]['customdata'][0]
        dff2 = dff2[dff2["area"] == click_area]

        survival_rates = ['1_year_survival_rate', '2_year_survival_rate', '3_year_survival_rate',
                          '4_year_survival_rate', '5_year_survival_rate']
        new_names = {'5_year_survival_rate': '5 Years', '4_year_survival_rate': '4 Years',
                     '3_year_survival_rate': '3 Years',
                     '2_year_survival_rate': '2 Years', '1_year_survival_rate': '1 Year'}

        fig1 = px.bar(dff2, x='area', y=survival_rates, barmode='group', orientation='v',
                      title='Business Survival Rates in {} '
                            'after {}'.format(click_area, year),
                      labels={'area': '', 'variable': 'Years after {}'.format(year)})

        fig1.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                               legendgroup=new_names[t.name],
                                               hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                               ))
        return [fig1]
