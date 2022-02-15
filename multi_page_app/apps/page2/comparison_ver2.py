import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from multi_page_app.app import app

df1 = pd.read_csv(
    'apps/page2/datasets/business-demographics-updated.csv')
df2 = pd.read_csv(
    'apps/page2/datasets/business-survival-rates-updated.csv')

layout = dbc.Container([
    html.Br(),

    dbc.Row(
        dbc.Col(html.H2("Comparison Graphs"),
                id='title')
    ),

    dbc.Row(
        dbc.Col(html.H5("Select 2 boroughs, a year and the desired statistic to compare them side-by-side!"),
                className='text-muted')
    ),

    dbc.Row(children=[
        dbc.Col(width=4, children=[
            dcc.Dropdown(id='bar_type',
                         options=[
                             {'label': 'Birth, Death and Net Birth Rates', 'value': 'Birth, Death and Net Birth Rates'},
                             {'label': 'Survival Rates over the years', 'value': 'Survival Rates'}],
                         multi=False,
                         searchable=False,
                         placeholder='Select the statistic to be compared...',
                         # clearable=False
                         style={"color": "black"},
                         value='Birth, Death and Net Birth Rates',
                         clearable=False
                         )]),
        dbc.Col(width=3, children=[
            dcc.Dropdown(id='select_year',
                         options=[{'label': x, 'value': x} for x in df1.year.unique()],
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Select a year between 2004-2018...',
                         # clearable=False
                         style={"color": "black"},
                         value=2004,
                         clearable=False
                         )
        ]
                ),
        dbc.Col(html.Em(children=[
        '*Data after 2019 is not available.*']))
    ]),
    html.Br(),
    dbc.Row(children=[
        dbc.Col(width={'size': 4, 'offset': 1}, children=[
            dcc.Dropdown(id='select_borough1',
                         options=[{'label': x, 'value': x} for x in df1.area.unique()],
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Select the first borough to compare...',
                         # clearable=False
                         style={"color": "black"},
                         value='City of London',
                         clearable=False
                         )]),
        dbc.Col(width={'size': 4, 'offset': 2}, children=[
            dcc.Dropdown(id='select_borough2',
                         options=[{'label': x, 'value': x} for x in df1.area.unique()],
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Select the second borough to compare...',
                         # clearable=False
                         style={"color": "black"},
                         value='Camden',
                         clearable=False
                         ),
        ])
    ]),

    dbc.Row(
    ),

    dbc.Row(children=[
        dbc.Col(xs=12, sm=12, md=12, lg=6, xl=6,children=[
            dcc.Graph(id='bar1')
        ], style={'margin': '0'}),
        dbc.Col(xs=12, sm=12, md=12, lg=6, xl=6, children=[
            dcc.Graph(id='bar2')
        ], style={'margin': '0'})
    ]),

])


@app.callback(
    [Output(component_id='bar1', component_property='figure'),
     Output(component_id='bar2', component_property='figure'),
     Input(component_id='bar_type', component_property='value'),
     Input(component_id='select_borough1', component_property='value'),
     Input(component_id='select_borough2', component_property='value'),
     Input(component_id='select_year', component_property='value')]
)
def survival_rate_bar(type, borough1, borough2, year_chosen):
    if type == "Birth, Death and Net Birth Rates":

        categories = ['birth_rate-death_rate', 'death_rate', 'birth_rate']
        new_names = {'birth_rate-death_rate': 'Birth Rate-Death Rate', 'death_rate': 'Death Rate',
                     'birth_rate': 'Birth Rate'}

        dff1 = df1.copy()
        dff1 = dff1[dff1["year"] == year_chosen]
        dff1 = dff1[dff1["area"] == borough1]

        dfff1 = df1.copy()
        dfff1 = dfff1[dfff1["year"] == year_chosen]
        dfff1 = dfff1[dfff1["area"] == borough2]

        fig1 = px.bar(
            data_frame=dff1,
            x=categories,
            y='area',
            orientation='h',
            barmode='group',
            labels={'area': ''},
            title='{} of {} in {}'.format(type, borough1, year_chosen)
        )
        fig1.update_layout(showlegend=False)
        fig1.update_xaxes(autorange="reversed")

        fig2 = px.bar(
            data_frame=dfff1,
            x=categories,
            y='area',
            orientation='h',
            barmode='group',
            labels={'area': '', 'variable': ''},
            title='{} of {} in {}'.format(type, borough2, year_chosen)
        )

        fig2.update_layout(legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        ))

        fig2.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                               legendgroup=new_names[t.name],
                                               hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                               )
                            )

        return fig1, fig2

    else:

        dff2 = df2.copy()
        dff2 = dff2[dff2["year"] == year_chosen]
        dff2 = dff2[dff2["area"] == borough1]

        dfff2 = df2.copy()
        dfff2 = dfff2[dfff2["year"] == year_chosen]
        dfff2 = dfff2[dfff2["area"] == borough2]

        survival_rates = ['5_year_survival_rate', '4_year_survival_rate', '3_year_survival_rate',
                          '2_year_survival_rate', '1_year_survival_rate']

        new_names = {'5_year_survival_rate': '5 Years', '4_year_survival_rate': '4 Years',
                     '3_year_survival_rate': '3 Years',
                     '2_year_survival_rate': '2 Years', '1_year_survival_rate': '1 Year'}

        fig1 = px.bar(
            data_frame=dff2,
            x=survival_rates,
            y='area',
            orientation='h',
            barmode='group',
            labels={'area': ''},
            title='{} in {} after {}'.format(type, borough1, year_chosen)
        )

        fig1.update_layout(showlegend=False)
        fig1.update_xaxes(autorange="reversed")

        fig2 = px.bar(
            data_frame=dfff2,
            x=survival_rates,
            y='area',
            orientation='h',
            barmode='group',
            labels={'area': '', 'variable': ''},
            title='{} in {} after {}'.format(type, borough1, year_chosen)
        )

        fig2.update_layout(legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        ))

        fig2.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                               legendgroup=new_names[t.name],
                                               hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                               )
                            )
        return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
