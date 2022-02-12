import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Input, Output

from multi_page_app.apps.page1 import map_app
from multi_page_app.apps.page2 import comparison_ver2

from multi_page_app.app import app

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Map", href="/map", id="map-link", style={"padding-right": "30px"})),
        dbc.NavItem(dbc.NavLink("Compare", href="/compare", id="compare-link", style={"padding-right": "30px"})),
        dbc.NavItem(
            dbc.Button("Logout", color='light', href='/logout', id="logout-link", style={"padding-left": "10px"},
                       )
        )
    ],
    brand="London Businesses",
    brand_href="/",
    color='primary',
    dark='True',
    fluid=True,
    class_name='navbar-expand-sm sticky-top',
    style={"border-radius": "10px"}
)

map_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/Map_Image.png", top=True, title='Map Image by Brandon Chew',
                    alt="Get to explore the statistics of the different boroughs in London!",
                    style={"border-radius": "25px"}),
        dbc.CardBody(
            [
                html.H4("The Map", className="card-title"),
                html.P(
                    "Be able to visualise business statistics in London "
                    "throughout 2004-2019 on a map by hovering over the different boroughs",
                    className="card-text",
                ),
                dbc.Button("Explore the map!", href="/map", color="primary"),
            ]
        ),
    ],
    style={"border-radius": "25px"}
)

comparison_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/compare.png", top=True, title='Image by Chern Yao Lim',
                    alt="Get to explore the statistics of the different boroughs in London!",
                    style={"border-radius": "25px"}),
        dbc.CardBody(
            [
                html.H4("Compare the Boroughs", className="card-title"),
                html.P(
                    "Learn about the boroughs birth and death rates over the years "
                    "from 2004-2019 and compare them simultaneously!",
                    className="card-text",
                ),
                dbc.Button("Compare!", href="/compare", color="primary"),
            ]
        ),
    ],
    style={"border-radius": "25px"}
)

index_layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1('Main Menu', id='main-menu-title'), width={'offset': 1})
    ]),
    dbc.Row([dbc.Col(map_card, width={'size': 4, 'offset': 1}),
             dbc.Col(comparison_card, width=4)])
], className="mx-auto rounded", style={"position": "absolute"})

app.layout = dbc.Container(fluid=True, children=[
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/map':
        return map_app.layout
    elif pathname == '/compare':
        return comparison_ver2.layout
    elif pathname == '/':
        return index_layout
    else:
        return '404 Page Not Found'


if __name__ == '__main__':
    app.run_server(debug=True)
