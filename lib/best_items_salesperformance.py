from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from lib.dataframe_proc import get_dataframe
import pandas as pd

ds_filtered = get_dataframe().copy()

prod = None
brand = None
zone = None
city = None
date_ini = None
date_lst = None

if all(char is not None for char in [prod, brand, city, zone, date_ini, date_lst]):
    ds_filtered = ds_filtered.loc[(ds_filtered['NombreDeProductor'] == prod) &
                                  (ds_filtered['marca'] == brand) &
                                  (ds_filtered['Municipio'] == city) &
                                  (ds_filtered['Zona'] == zone) &
                                  (ds_filtered['date'] > date_ini) & (ds_filtered['date'] < date_lst)]

def_plot = ds_filtered.groupby(['DescripcionLargaProducto'])['Unidades'].sum().reset_index()
def_plot = def_plot.sort_values(by='Unidades', ascending=False).fillna(0).head(5)
data_plt = ds_filtered[ds_filtered['DescripcionLargaProducto'].isin(def_plot['DescripcionLargaProducto'].iloc[:5].values)]
data_plt['mes'] = pd.to_datetime(data_plt['date'], format='%Y-%m').dt.strftime('%Y-%m')
data_plt['Ganancia'] = data_plt['Unidades']*data_plt['PrecioProducto']
data_plt = data_plt.groupby(['DescripcionLargaProducto', 'mes'])['Ganancia'].sum().reset_index()

bc_fig = px.line(data_plt,
                 x="mes",
                 y="Ganancia",
                 color='DescripcionLargaProducto',
                 labels={"mes": "Time Range   (Months)",
                         "Ganancia": "Accumulative Sales per product   (COP)"},
                 color_discrete_sequence=["#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"])

bc_fig.update_layout(autosize=True,
                     title={'text': "PRODUCTS' SALES PERFORMANCE OVER TIME - TOP 5"},
                     template='plotly_dark',
                     legend_title="PRODUCT'S TOP",
                     font=dict(
                         family='Barlow, sans-serif',
                         size=14,
                         color="LightBlue"),
                     )
bc_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")

bottom_graph = html.Div([
    dbc.Col([
        dcc.Graph(
            figure=bc_fig,
            id="bottomcentral-chart",
            config={"displayModeBar": False},
            style={'height': '38vh'},
            className="card"
            ),
        ], sm={"size": 6,  "offset": 2},
           md={"size": 8,  "offset": 2},
           lg={"size": 10, "offset": 2},
           xl={"size": 10, "offset": 2}
    )
])
