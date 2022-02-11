import dash
import pandas as pd
import plotly
import plotly.express as px
from dash import html, dcc, Input, Output
from multi_page_app.app import app

df = pd.read_csv(
     'C:/Users/Brandon/PycharmProjects/comp0034-cw1-i-Jorge-gg7/multi_page_app/apps/page2/datasets/business-demographics-updated.csv')

layout = html.Div([

    html.Div([
        dcc.Dropdown(id='select_borough',
            options=[
                     {'label': 'City of London', 'value': 'City of London'},
                     {'label': 'Barking and Dagenham', 'value': 'Barking and Dagenham'},
                     {'label': 'Barnet', 'value': 'Barnet'},
                     {'label': 'Bexley', 'value': 'Bexley'},
                     {'label': 'Brent', 'value': 'Brent'},
                     {'label': 'Bromley', 'value': 'Bromley'},
                     {'label': 'Camden', 'value': 'Camden'},
                     {'label': 'Croydon', 'value': 'Croydon'},
                     {'label': 'Ealing', 'value': 'Ealing'},
                     {'label': 'Enfield', 'value': 'Enfield'},
                     {'label': 'Greenwich', 'value': 'Greenwich'},
                     {'label': 'Hackney', 'value': 'Hackney'},
                     {'label': 'Hammersmith and Fulham', 'value': 'Hammersmith and Fulham'},
                     {'label': 'Haringey', 'value': 'Haringey'},
                     {'label': 'Harrow', 'value': 'Harrow'},
                     {'label': 'Havering', 'value': 'Havering'},
                     {'label': 'Hillingdon', 'value': 'Hillingdon'},
                     {'label': 'Hounslow', 'value': 'Hounslow'},
                     {'label': 'Islington', 'value': 'Islington'},
                     {'label': 'Kensington and Chelsea', 'value': 'Kensington and Chelsea'},
                     {'label': 'Kingston upon Thames', 'value': 'Kingston upon Thames'},
                     {'label': 'Lambeth', 'value': 'Lambeth'},
                     {'label': 'Lewisham', 'value': 'Lewisham'},
                     {'label': 'Merton', 'value': 'Merton'},
                     {'label': 'Newham', 'value': 'Newham'},
                     {'label': 'Redbridge', 'value': 'Redbridge'},
                     {'label': 'Richmond upon Thames', 'value': 'Richmond upon Thames'},
                     {'label': 'Southwark', 'value': 'Southwark'},
                     {'label': 'Sutton', 'value': 'Sutton'},
                     {'label': 'Tower Hamlets', 'value': 'Tower Hamlets'},
                     {'label': 'Waltham Forest', 'value': 'Waltham Forest'},
                     {'label': 'Wandsworth', 'value': 'Wandsworth'},
                     {'label': 'Westminster', 'value': 'Westminster'},
            ],
            optionHeight=20,
            value='Westminster',
            disabled=False,
            multi=True,
            searchable=True,
            search_value='',
            placeholder='Select boroughs...',
            clearable=True,
            )
    ]),

    html.Div([
        dcc.Graph(id='comparison_graph', figure={})
    ]),

])

@app.callback(
    Output(component_id='comparison_graph', component_property='figure'),
    Input(component_id='select_borough', component_property='value'),
)

def build_graph(boroughs_chosen):
    df1 = df.copy()
    df1 = df[df["area"==boroughs_chosen]]

    fig = px.bar(
        data_frame=df1,
        x="year",
        y="birth-death_rate",
        color="area",
        orientation="v",
        barmode='group',
    )
    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)
