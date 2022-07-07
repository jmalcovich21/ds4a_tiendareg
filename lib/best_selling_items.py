from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from lib.dataframe_proc import get_dataframe

data = get_dataframe().copy()

data['Month'] = data['date'].dt.to_period('M')
best = data.groupby(['DescripcionLargaProducto', 'Estrato', 'Month'])['Unidades'].sum().to_frame()
best = best.groupby(['DescripcionLargaProducto', 'Estrato'])['Unidades'].median().reset_index(name='Median').sort_values(['Median'], ascending=False)
best['market share percentage by median'] = best['Median']*100/best['Median'].sum()
best['market share percentage by median'] = best['market share percentage by median'].apply(lambda x: round(x, 2))

tl_fig = px.bar(best.head(10),
                x="Median",
                y="DescripcionLargaProducto",
                color="Median",
                orientation="h", labels={'Median': 'Monthly Sales (median)', 'DescripcionLargaProducto': ''},
                hover_data={"market share percentage by median", "Median"},
                # hover_name="DescripcionLargaProducto",
                color_continuous_scale=px.colors.sequential.Blues_r)

tl_fig.update_xaxes(tickangle=90, tickfont=dict(size=8))
tl_fig.update_coloraxes(showscale=False)
tl_fig.update_layout(title_text='BEST SELLING PRODUCTS - TOP 10',
                     template='plotly_dark',
                     title_x=0.5, hoverlabel=dict(font_size=14),
                     font=dict(
                         family='Barlow, sans-serif',
                         size=12,
                         color="LightBlue")
                     )

tl_graph = dbc.Col([
        dcc.Graph(
            figure=tl_fig,
            id="topleft-chart",
            config={"displayModeBar": False},
            style={'height': '50vh'},
            className="card",
            ),
        ],  sm={"size": 2, "offset": 2},
            md={"size": 3, "offset": 2},
            lg={"size": 4, "offset": 2},
            xl={"size": 4, "offset": 2},
    )

