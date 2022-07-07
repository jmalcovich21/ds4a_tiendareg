from dash import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
from lib.portfolio_model import get_portfolio_model
from lib.dataframe_proc import get_city_lat_lon


def topright_callbacks(app, data, df_barrios):
    @app.callback(
        Output("topright-chart", "figure"),
        [
            State("company_dropdwn", "value"),
            State("brand_dropdwn", "value"),
            State("city_dropdwn", "value"),
            State("zone_dropdwn", "value"),
            State('my-slider', "value")
        ],
        [
            Input('button-1', 'n_clicks')
        ])
    def get_topright_figure(select_product, select_marca, select_ciudad, select_zona, slider_pos, n_clicks):
        if select_product is None or select_marca is None or select_ciudad is None or select_zona is None or n_clicks == 0:
            raise PreventUpdate
        else:
            if slider_pos == 1:
                df_treemap = get_portfolio_model(select_product, select_marca, select_ciudad, select_zona)
                # Create the graph that will show the top 5 product for the filtered brand
                fig = px.treemap(df_treemap, path=["DescripcionLargaProducto", "Estrato2"], values="Median",
                                 color_discrete_sequence=["#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"])
                fig.update_layout(template='plotly_dark',
                                  title_text='COMPANY´s BEST PRODUCTS PORTFOLIO (PER STRATA)',
                                  uniformtext=dict(minsize=14),
                                  margin=dict(t=55, l=10, r=10, b=0),
                                  font=dict(family='Barlow, sans-serif',
                                            size=14,
                                            color="LightBlue"
                                  )
                )

            elif slider_pos == 0:
                df_filter = data.loc[(data['NombreDeProductor'] == select_product) &
                                     (data['marca'] == select_marca) &
                                     (data['Municipio'] == select_ciudad) &
                                     (data['Zona'] == select_zona)]
                df_filter.drop(columns=['Estrato'])
                # Create a new column with the year-month
                df_filter['Month'] = df_filter['date'].dt.to_period('M')
                # Make the sum of the units sold by month, stratum and sku
                df_filter_aux = df_filter.groupby(['NombreDeProductor', 'marca', 'Municipio', 'BARRIO', 'Month'])[
                    'Unidades'].sum().to_frame()
                # Calculate the median number of units per month of each sku by stratum and order it in descending order
                df_filter_aux = df_filter_aux.groupby(['NombreDeProductor', 'marca', 'Municipio', 'BARRIO'])[
                    'Unidades'].median().reset_index(name='Median').sort_values(['Median'], ascending=False)

                latitude, longitude = get_city_lat_lon(select_ciudad)

                fig = px.choropleth_mapbox(df_filter_aux, geojson=df_barrios.set_index("BARRIO").GEOMETRY,
                                           locations='BARRIO', color="Median", mapbox_style='carto-darkmatter',
                                           center={'lat': latitude, 'lon': longitude}, zoom=12, opacity=0.5,
                                           width=930, height=475, template='plotly_dark',
                                           color_continuous_scale=px.colors.sequential.Blues)
                fig.update_layout(
                                  title_text='PRODUCTS PORTFOLIO MONTHLY MARKET SHARE (PER LOCATION)',
                                  uniformtext=dict(minsize=14),
                                  margin=dict(t=55, l=10, r=10, b=0),
                                  font=dict(family='Barlow, sans-serif',
                                            size=14,
                                            color="LightBlue"
                                            )
                                  )

            return fig
