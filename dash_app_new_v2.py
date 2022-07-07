from dash import Dash, html
import dash_bootstrap_components as dbc
from lib import best_selling_items, best_sales_portfolio, best_items_salesperformance, sidebar
from lib.dataframe_proc import get_dataframe, get_neighbors, neighbors_processing
from callbks.sidebar_calls import sidebar_callbacks
from callbks.topleft_calls import topleft_callbacks
from callbks.topright_calls import topright_callbacks
from callbks.bottom_calls import bottom_callbacks
import geopandas as gpd

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Barlow:wght@300&display=swap",
    dbc.themes.BOOTSTRAP
]
#################################################################################################################
df = get_dataframe()
data = gpd.GeoDataFrame(get_dataframe())
data = neighbors_processing(data)
neigh_df = gpd.GeoDataFrame(get_neighbors())

#################################################################################################################
dash_app_ds4a = Dash(__name__, external_stylesheets=external_stylesheets,
                     meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
dash_app_ds4a.title = "TR Analytics Dashboard"

dash_app_ds4a.css.config.serve_locally = True
#################################################################################################################
# Layout Structure
dash_app_ds4a.layout = dbc.Container([
        dbc.Row([sidebar.sidebar]),  # Sidebar with customer settings
        dbc.Row([dbc.Col(html.H1("Tienda Registrada Analytics Dashboard"), lg={"size": 10, "offset": 2})]),
        dbc.Row([best_selling_items.tl_graph,      # Top_left Graph
                 best_sales_portfolio.tr_graph]),  # Top_Right Graph
        dbc.Row([best_items_salesperformance.bottom_graph]),
], fluid=True, style={'backgroundColor': '#101010'},)
################################################################################################################
# Callbacks Section
sidebar_callbacks(dash_app_ds4a, df)
topleft_callbacks(dash_app_ds4a, df)
topright_callbacks(dash_app_ds4a, data, neigh_df)
bottom_callbacks(dash_app_ds4a, df)

if __name__ == "__main__":
    dash_app_ds4a.run_server(debug=False)
