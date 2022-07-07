# Callbacks

from dash import Input, Output, State
from dash.exceptions import PreventUpdate


def sidebar_callbacks(app, df):
    @app.callback(
        [
            Output("brand_dropdwn", 'options'),
            Output("brand_dropdwn", 'value')
        ],
        [
            State("date_picker", "start_date"),
            State("date_picker", "end_date"),
        ],
        [
            Input("company_dropdwn", 'value')
        ]
    )
    def get_brand_options(start_date, end_date, company):
        if company is None or start_date is None or end_date is None:
            raise PreventUpdate
        else:
            get_brand_options.df2 = df[df['NombreDeProductor'] == company]
            brand_options = [{'label': b, 'value': b} for b in get_brand_options.df2.marca.unique()]
            return brand_options, None

    @app.callback(
        [Output("city_dropdwn", 'options'),
         Output("city_dropdwn", 'value')],
        [Input("brand_dropdwn", 'value')])
    def get_city_list(marca):
        if marca is None:
            raise PreventUpdate
        else:
            get_city_list.df3 = get_brand_options.df2[get_brand_options.df2['marca'] == marca]
            city_options = [{'label': c, 'value': c} for c in get_city_list.df3.Municipio.unique()]
            return city_options, None

    @app.callback(
        [Output("zone_dropdwn", 'options'),
         Output("zone_dropdwn", 'value')],
        [Input("city_dropdwn",  'value')])
    def get_zone_list(city):
        if city is None:
            raise PreventUpdate
        else:
            get_zone_list.df4 = get_city_list.df3[get_city_list.df3['Municipio'] == city]
            zone_options = [{'label': z, 'value': z} for z in get_zone_list.df4.Zona.unique()]
            return zone_options, None
