# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt


# Recall app
from app import app

####################################################################################
# Add the DS4A_Img
####################################################################################

DS4A_Img = html.Div(
    children=[
        html.Img(
            src=app.get_asset_url("c1_logo_tagline.svg"),
            id="ds4a-image",
        )
    ],
)

#############################################################################
# State Dropdown
#############################################################################
with open('data/states.json') as f:
    states = json.loads (f.read ())

dropdown = dcc.Dropdown(
    id="state_dropdown",
    options=[{"label": key, "value": states[key]} for key in states.keys()],
    value=["NY", 'CA'],
    multi=True
)

##############################################################################
# Date Picker
##############################################################################
date_picker = dcc.DatePickerRange(
    id='date_picker',
    min_date_allowed=dt(2014, 1, 2),
    max_date_allowed=dt(2017, 12, 31),
    start_date=dt(2016, 1, 1).date(),
    end_date=dt(2017, 1, 1).date()
)

#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [DS4A_Img,  # Add the DS4A_Img located in the assets folder
     html.Hr(),  # Add an horizontal line
     ####################################################
     # Place the rest of Layout here
     ####################################################
     html.H5 ("Select dates"),
     date_picker,
     html.Hr(),
     html.H5("Select states"),
     dropdown,
     html.Hr(),
     ], className='ds4a-sidebar'
)

dbc.Row ([

    dbc.Col (  # Barra de Graphics
        [
            dbc.Row (  # Recuadros Superiores
                [
                    dbc.Col ([
                        html.Div("BAR Graph with Most Demanded Products"),
                        html.Div(
                            children=dcc.Graph (
                                id="price-chart1",
                                config={"displayModeBar": True},
                                style={'width': '60vh', 'height': '50vh'}
                            ), className="card",
                        ),
                    ], width="5"),
                    dbc.Col ([
                        html.Div ("Companies' Recommended Portfolio"),
                        html.Div (
                            children=dcc.Graph (
                                id="price-chart2",
                                config={"displayModeBar": True},
                                style={'width': '80vh', 'height': '50vh'}
                            ), className="card",
                        ),
                    ], width="6"),
                ], className="gy-2", justify="center", align="start"
            ),
            dbc.Row (  # Grafica inferior
                [
                    dbc.Col ([
                        html.Div ("TopSales vs Time Graph"),
                        html.Div (
                            children=dcc.Graph (
                                id="price-chart3",
                                config={"displayModeBar": True},
                                style={'width': '160vh', 'height': '10vh'}
                            ),
                        ),
                    ], width="11"),
                ], className="gy-2", justify="center", align="start"
            ),
        ], width={"size": 10, "offset": 0}, className="g-1"
    ),
]
), className = "g-2",

