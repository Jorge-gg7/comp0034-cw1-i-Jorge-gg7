import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Input, Output

from multi_page_app.apps.page1 import map_app
# from multi_page_app.apps.page2 import page_2

from multi_page_app.app import app

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Map", href="/map"), id="map-link"),
        dbc.NavItem(dbc.NavLink("Compare", href="/compare", id="compare-link")),
        dbc.NavItem(dbc.Button("Logout", color='light', href='/logout', id="logout-link"))
    ],
    brand="London Businesses",
    brand_href="/",
    color='secondary',
    dark='True',
    fluid=True,
    class_name='navbar-expand-sm sticky-top',
)

map_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/Image1.png", top=True, title='Map Image',
                    alt="Get to explore the statistics of the different boroughs in London!"),
        dbc.CardBody(
            [
                html.H4("The Map", className="card-title"),
                html.P(
                    "Be able to visualise business statistics in London "
                    "throughout 2004-2019 on a map!",
                    className="card-text",
                ),
                dbc.Button("Explore the map!", href="/map", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"}
)

index_layout = dbc.Container([
    dbc.Row([dbc.Col(map_card)])
])

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
    #elif pathname == '/compare':
        #return page2.layout
    elif pathname == '/':
        return index_layout
    else:
        return '404 Page Not Found'

if __name__ == '__main__':
    app.run_server(debug=True)
