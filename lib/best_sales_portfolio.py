from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from lib.portfolio_model import get_portfolio_model

def top5_portfolio_filtered(select_product, select_marca, select_ciudad, select_zona):
    if select_product is not None and select_marca is not None and select_ciudad is not None and select_zona is not None:

        df_treemap = get_portfolio_model(select_product, select_marca, select_ciudad, select_zona)
        # Create the graph that will show the top 5 product for the filtered brand
        fig = px.treemap(df_treemap, path=["DescripcionLargaProducto", "Estrato2"], values="Median")
        fig.update_layout(
            uniformtext=dict(minsize=10),
            margin=dict(t=10, l=10, r=10, b=10),
        )
    elif select_product is None and select_marca is None and select_ciudad is None and select_zona is None:

        df_treemap = get_portfolio_model(select_product, select_marca, select_ciudad, select_zona)
        # Create the graphic
        fig = px.treemap(df_treemap, path=["marca", "DescripcionLargaProducto"], values="Median",
                         color_discrete_sequence=["#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"])
        fig.update_layout(
            template='plotly_dark',
            title_text='TRs NATIONAL OPERATIONS TOP PRODUCTS MARKET SHARE',
            uniformtext=dict(minsize=14),
            margin=dict(t=55, l=10, r=10, b=0),
            font=dict(
                family='Barlow, sans-serif',
                size=14,
                color="LightBlue"),
        )
    return fig


tr_fig = top5_portfolio_filtered(None, None, None, None)

tr_graph = dbc.Col([
        dcc.Graph(
            figure=tr_fig,
            id="topright-chart",
            config={"displayModeBar": True},
            style={'height': '50vh'},
            className="card",
            ),
        ],  sm={"size": 3, "offset": 0},
            md={"size": 4, "offset": 0},
            lg={"size": 6, "offset": 0},
            xl={"size": 6, "offset": 0},
    )
