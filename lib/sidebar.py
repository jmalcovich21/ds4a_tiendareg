from dash import html, dcc
import dash_bootstrap_components as dbc
from lib.dataframe_proc import get_dataframe
import pandas as pd

df = get_dataframe()

# Date Picker
date_picker = dcc.DatePickerRange(
                        id="date_picker",
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        min_date_allowed=df.date.min().date(),
                        max_date_allowed=df.date.max().date(),
                        start_date=None,
                        end_date=None,
                        calendar_orientation='horizontal',
                        clearable=True,
                        style={
                                'height': '10%',
                                'padding-top': '0px',
                                'padding-bottom': '8px',
                                'font-size': '16px',
                                'background-color': '#00131C',
                                'display': 'inline-block',
                                'zIndex': 10
                        },
)

# Company Dropdown
company_dropdown = dcc.Dropdown(
                        id="company_dropdwn",
                        multi=False,
                        clearable=True,
                        disabled=False,
                        searchable=True,
                        options=[{'label': c, 'value': c} for c in df.NombreDeProductor.unique()],
                        style={
                               'width': '100%',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '4px',
                               'font-size': '14px',
                               'margin-top': '2px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'dark-blue',
                               'background-color': '#00131C',
                               'display': True,
                        },
)

# Company's Brand Dropdown
brand_dropdown = dcc.Dropdown(
                        id="brand_dropdwn",
                        multi=False,
                        clearable=True,
                        disabled=False,
                        searchable=True,
                        options=[],
                        style={
                               'width': '100%',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '4px',
                               'font-size': '14px',
                               'margin-top': '2px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'dark-blue',
                               'background-color': '#00131C',
                               'display': True,
                                },
)

# City Dropdown
city_dropdown = dcc.Dropdown(
                        id="city_dropdwn",
                        multi=False,
                        clearable=True,
                        disabled=False,
                        searchable=True,
                        options=[],
                        style={
                               'width': '100%',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '4px',
                               'font-size': '14px',
                               'margin-top': '2px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'dark-blue',
                               'background-color': '#00131C',
                               'display': True,
                               },
)

# Zone Dropdown
zone_dropdown = dcc.Dropdown(
                        id="zone_dropdwn",
                        multi=False,
                        clearable=True,
                        disabled=False,
                        searchable=True,
                        options=[],
                        style={
                               'width': '100%',
                               'height': '25px',
                               'padding-top': '0px',
                               'padding-bottom': '4px',
                               'font-size': '14px',
                               'margin-top': '2px',
                               'margin-bottom': '15px',
                               'margin-left': '0px',
                               'color': 'dark-blue',
                               'background-color': '#00131C',
                               'display': True,
                               },
)

blue_button_style = {'background-color': '#034f84',
                     'color': 'white',
                     'height': '50px',
                     'width': '180px',
                     'margin-top': '0px',
                     }

slider = dcc.Slider(0, 1,
                    id='my-slider',
                    step=None,
                    marks={
                        0: 'SALES MAP',
                        1: 'PORTFOLIO',
                    },
                    value=0,
)

# Sidebar Design
sidebar = html.Div([
        dbc.Col([
                dbc.Row([  # Imagen Superior
                    html.Div(children=[html.Img(src='assets/DS4AColombia.jpeg',
                                                id="ds4a-image",
                                                style={'height': '100%', 'width': '100%'})])]),
                dbc.Row(html.H2(id='date_filter',     children='Select Analysis Timeframe:')),
                dbc.Row(date_picker),
                dbc.Row(html.H2(id='company_text',    children='Select your Company:')),
                dbc.Row(company_dropdown),
                dbc.Row(html.H2(id='brand_text',      children='Select the Company\'s brand:')),
                dbc.Row(brand_dropdown),
                dbc.Row(html.H2(id='city_text',       children='Select a brand\'s city of interest:')),
                dbc.Row(city_dropdown),
                dbc.Row(html.H2(id='zone_text',       children='Select a brand\'s zone of interest:')),
                dbc.Row(zone_dropdown),
                dbc.Row(html.H2(id='slider_text',     children='Select either Portfolio Treemap Graph or Available Sales GeoMap:')),
                dbc.Row(slider),
                dbc.Row(html.P(html.Br())),
                html.Button(id='button-1',
                            children=['Update dashboard'],
                            n_clicks=0,
                            style=blue_button_style
                            ),
                dbc.Row(html.P(html.Br())),
                dbc.Row([  # Imagen Inferior
                    html.Div(children=[html.Img(src='assets/Team183.jpeg',
                                                id="team183-image",
                                                style={'height': '100%', 'width': '100%'})])]),
                ], width={"size": 2}, className="sidebar",),
],
)
