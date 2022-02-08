import pandas as pd
import plotly.express as px
import json

from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from multi_page_app.app import app

df = pd.read_csv('datasets/business-demographics-updated.csv')
f = open('datasets/london_boroughs.json')
geoj = json.load(f)

layout = dbc.Container([
    html.Br(),

    dbc.Row(
        dbc.Col(html.H1("Choropleth Map")
                )
    ),

    dbc.Row(
        dbc.Col(html.H5("Select the year on the dropdown menu that you want to explore and hover over the boroughs to "
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
    )
])
