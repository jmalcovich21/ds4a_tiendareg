from dash import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate


def bottom_callbacks(app, df):
    @app.callback(
        Output("bottomcentral-chart", "figure"),
        [
            State("date_picker", "start_date"),
            State("date_picker", "end_date"),
            State("company_dropdwn", "value"),
            State("brand_dropdwn", "value"),
            State("city_dropdwn", "value"),
            State("zone_dropdwn", "value")
        ],
        [
            Input('button-1', 'n_clicks')
        ])
    def get_bottom_figure(date_ini, date_lst, prod, brand, city, zone, n_clicks):
        if date_ini is None or date_lst is None or prod is None or brand is None or city is None or zone is None or n_clicks == 0:
            raise PreventUpdate
        else:
            ds_filtered = df.copy()
            ds_filtered = ds_filtered.loc[
                (ds_filtered['NombreDeProductor'] == prod) &
                (ds_filtered['marca'] == brand) &
                (ds_filtered['Municipio'] == city) &
                (ds_filtered['Zona'] == zone) &
                (ds_filtered['date'] > date_ini) & (ds_filtered['date'] < date_lst)
            ]

            def_plot = ds_filtered.groupby(['DescripcionLargaProducto'])['Unidades'].sum().reset_index()
            def_plot = def_plot.sort_values(by='Unidades', ascending=False).fillna(0).head(5)
            data_plt = ds_filtered[ds_filtered['DescripcionLargaProducto'].isin(def_plot['DescripcionLargaProducto'].iloc[:5].values)]
            data_plt['mes'] = pd.to_datetime(data_plt['date'], format='%Y-%m').dt.strftime('%Y-%m')
            data_plt['Ganancia'] = data_plt['Unidades'] * data_plt['PrecioProducto']
            data_plt = data_plt.groupby(['DescripcionLargaProducto', 'mes'])['Ganancia'].sum().reset_index()

            bc_fig = px.line(data_plt,
                             x="mes",
                             y="Ganancia",
                             color='DescripcionLargaProducto',
                             title="Products' sales performance over time - Top 5",
                             labels={
                                 "mes": "Time Range   (Months)",
                                 "Ganancia": "Accumulative Sales per product   (COP)"
                             },
                             color_discrete_sequence=["#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4", "#90e0ef",
                                                      "#ade8f4", "#caf0f8"]
                        )
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

            return bc_fig
