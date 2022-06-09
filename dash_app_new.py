# https://realpython.com/python-dash/
from dash import Dash, html, dcc, Input, Output, callback, dash_table, State, MATCH, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
#from lib import sidebar

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

dash_app_ds4a = Dash(__name__, requests_pathname_prefix='/tiendareg/', external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
dash_app_ds4a.title = "TR Analytics Dashboard"

dash_app_ds4a.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([ # Imagen Superior
                    html.Div(children=[html.Img(src='assets/DS4AColombia.jpeg',
                                                id="ds4a-image",
                                                style={'height':'100%', 'width':'100%'})])
                ]),
                dbc.Row(html.H1(id='date_filter',children='Select Analysis Timeframe:',className='h1')),
                dbc.Row(
                    dcc.DatePickerRange(
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        calendar_orientation='horizontal',
                        clearable=True,
                        style={
                                'height': '10%',
                                'font-size': '12px',
                                'color': 'darkblue',
                                'background-color': '#000033',
                                'display': 'inline-block',
                                'zIndex': 10
                        },
                    )
                ),
                dbc.Row(html.H1(id='company_text',children='Select your Company:',className='h1')),
                dbc.Row(
                    dcc.Dropdown(
                        ['Postobon', 'Alpina', 'McDonals','Noel', 'Diana','Nutresa','Palmolive'],
                        placeholder="Select a Company",
                        id="company_drop",
                        style={
                                'width':'100%',
                               'font-size': '12px',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '6px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'blue',
                               'background-color': '#000033',
                        },
                    )
                ),
                dbc.Row(html.H1(id='brand_text',children='Select the Company\'s brand:',className='h1')),
                dbc.Row(
                    dcc.Dropdown(
                        ['Quala', 'Bonyurt', 'Signature','Saltin', 'Arroz Premium','Corona','Naturals'],
                        placeholder="Select a brand",
                        id="brand_drop",
                        style={'width':'100%',
                               'font-size': '12px',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '6px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'blue',
                               'background-color': '#000033',
                        },
                    )
                ),
                dbc.Row (html.H1 (id='location_text_1', children='Select a brand\'s city of interest:', className='h1')),
                dbc.Row (
                    dcc.Dropdown (
                        ['Cali', 'Medellin', 'Barranquilla', 'Bogota'],
                        placeholder="Select a location...",
                        searchable=True,
                        id="City_location_drop",
                        style={
                               'width': '100%',
                               'font-size': '12px',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '6px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'blue',
                               'background-color': '#000033',
                               },
                    )
                ),
                dbc.Row (html.H1 (id='location_text_2', children='Select a brand\'s zone of interest:', className='h1')),
                dbc.Row (
                    dcc.Dropdown (
                        ['Centro', 'Norte', 'Occidente', 'Sur'],
                        placeholder="Select a zone...",
                        id="Zone_location_drop",
                        style={
                               'width': '100%',
                               'font-size': '12px',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '6px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'blue',
                               'background-color': '#000033',
                               },
                    )
                ),
                dbc.Row( # Iamgen Inferior
                    html.Div (children=[html.Img (src='assets/Team183.jpeg',
                                                  id="team183-image",
                                                  style={'height': '100%', 'width': '100%'})])
                ),
            ],width={"size": 2}, className="sidebar",),
        ]),
        dbc.Row([
                dbc.Col(html.H1("Tienda Registrada Analytics Dashboard"),
                        xs={"size": 10, "offset": 2})
        ], justify='around'),
        dbc.Row([
                dbc.Col([
                        html.H2("BAR Graph with Most Demanded Products"),
                        dcc.Graph (
                                id="price-chart1",
                                config={"displayModeBar": True},
                                style={'height': '38vh'},
                                className="card",
                        )
                ],lg={"size": 4, "offset": 3},xl={"size": 5, "offset": 2}),
                dbc.Col([
                        html.H2("Companies' Recommended Portfolio"),
                        html.Div (
                            children=dcc.Graph (
                                id="price-chart2",
                                config={"displayModeBar": True},
                                style={'height': '38vh'}
                            ), className="card",
                        ),
                ],lg={"size": 5, "offset": 0},xl={"size": 5, "offset": 0}),
        ]),
        dbc.Row([
                dbc.Col([
                        html.H2("Brand's best products sales performance"),
                        html.Div (
                            children=dcc.Graph (
                                id="price-chart3",
                                config={"displayModeBar": True},
                                style={'height': '45vh'}
                            ), className="card",
                        ),
                ],lg={"size": 9, "offset": 3},xl={"size": 10, "offset": 2}),

        ], justify='around'),

], fluid=True, style={'backgroundColor':'#000033'},
)
# Callbacks

@dash_app_ds4a.callback(
    [
        Output("price-chart", "figure"),
        Output("volume-chart", "figure"),
        #  For example, Output("price-chart", "figure") will update the figure property of the "price-chart" element.
    ],  # Outputs...
    [
        Input("region-filter", "value"),
        # So, Input("region-filter", "value") will watch the "region-filter" element for changes and will take
        # its value property if the element changes.
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
            (data.region == region)
            & (data.type == avocado_type)
            & (data.Date >= start_date)
            & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]

    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


#if __name__ == "__main__":
#    app.run_server(debug=True)
