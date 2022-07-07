import pandas as pd
from datetime import timedelta
from pmdarima.arima import auto_arima
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import calendar
import warnings
from dash import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate

warnings.filterwarnings('ignore')

def topleft_callbacks(app, df):
    @app.callback(
        Output("topleft-chart", "figure"),
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
    def get_topleft_figure(select_product, select_marca, select_ciudad, select_zona, slider_pos, n_clicks):
        if select_product is None or select_marca is None or select_ciudad is None or select_zona is None or slider_pos == 1:
            raise PreventUpdate
        else:
            data = df.copy()
            df_filter = data.loc[(data['NombreDeProductor'] == select_product) &
                                    (data['marca'] == select_marca) &
                                    (data['Municipio'] == select_ciudad) &
                                    (data['Zona'] == select_zona)]
            # Create a new column with the year-month
            df_filter['Month'] = df_filter['date'].dt.to_period('M')
            # Make the sum of the units sold by month, stratum and sku
            df_filter_aux = df_filter.groupby(['DescripcionLargaProducto', 'Estrato', 'Month'])['Unidades'].sum().to_frame()
            # Calculate the median number of units per month of each sku by stratum and order it in descending order
            df_filter_aux = df_filter_aux.groupby(['DescripcionLargaProducto', 'Estrato'])['Unidades'].median().reset_index(name='Median').sort_values(['Median'], ascending=False)

            df_filter_aux = df_filter_aux.head(5)[df_filter_aux.Median > 15]
            warnings.filterwarnings('ignore')
            column_names = ["Year", "Month", "sum", "product", "estrato"]
            mensual_grafico = pd.DataFrame(columns=column_names)

            contador = 0

            if len(df_filter_aux) > 5:
                contador = 5
            else:
                contador = len(df_filter_aux)

            for i in range(contador):

                try:
                    # FILTRAR PRODUCTO
                    producto = data.loc[(data['NombreDeProductor'] == select_product) &
                                    (data['marca'] == select_marca) &
                                    (data['Municipio'] == select_ciudad) &
                                    (data['Zona'] == select_zona)]
                    producto = producto[producto.DescripcionLargaProducto == df_filter_aux.iloc[i, 0]]
                    producto = producto[producto.Estrato == df_filter_aux.iloc[i, 1]]

                    # DEJANDO LA FECHA COMO INDICE DE LOS DATOS
                    producto.set_index('date', inplace=True)

                    # HACIENDO RESAMPLING DE LA SERIE POR SEMANA
                    serie = producto['Unidades'].resample('W').sum()
                    serie = serie

                    # QUITANDO LA ULTIMA SEMANA PARA QUE QUEDE INFORMACIÓN COMPLETA
                    serie = serie.iloc[:-1]

                    # CREANDO LA BASE ESTIMACION DEL MODELO (SE QUITAN LAS ULTIMAS 6 FILAS)
                    serie_model = serie.iloc[:-6]

                    # CREANDO BASE PARA PROBAR LA ESTIMACION (ULTIMOS 6 DATOS DE LA SERIE)
                    serie_model_test = serie.tail(6)

                    # CREANDO BASE CON LOGARITMO NATURAL PARA EL MODELO
                    serie_model_log = np.log(serie_model)
                    serie_model_log = serie_model_log.where(serie_model_log > 0).dropna()

                    serie_log = np.log(serie)
                    serie_log = serie_log.where(serie_log > 0).dropna()

                    # ESTIMACIÓN DE LOS MODELOS
                    model1 = auto_arima(serie_model, test='adf', error_action='ignore', suppress_warnings=True,
                                    stepwise=True, seasonal=False)
                    model2 = auto_arima(serie_model_log, test='adf', error_action='ignore', suppress_warnings=True,
                                    stepwise=True, seasonal=False)
                    if (serie_model == 1).any() == False and (serie == 0).any() == False:
                        model3 = ExponentialSmoothing(serie_model, trend='mul', seasonal=None).fit()
                        model4 = ExponentialSmoothing(serie_model_log, trend='mul', seasonal=None).fit()

                    # PROYECCIÓN DE LA SERIE CON CADA MODELO, EN RES_TOTAL, CADA FILA ES LA ESTIMACIÓN DE UN MODELO
                    RES_MODEL1 = model1.predict(6)
                    RES_MODEL2 = np.exp(model2.predict(6))

                    if (serie_model == 1).any() == True or (serie == 0).any() == True:
                        RES_MODEL3 = np.repeat(0, 6, axis=0)
                        RES_MODEL4 = np.repeat(0, 6, axis=0)
                    else:
                        RES_MODEL3 = model3.forecast(6)
                        RES_MODEL4 = np.exp(model4.forecast(6))

                    RES_TOTAL = pd.DataFrame(np.array((RES_MODEL1, RES_MODEL2, RES_MODEL3, RES_MODEL4)))
                    RES_TOTAL = RES_TOTAL.transpose()

                    Errores = []
                    n = 0

                    while n < 4:
                        Errores.append((abs(RES_TOTAL[n] - serie_model_test.values).sum()) / RES_TOTAL[n].size)
                        n = n + 1
                    if (serie_model == 1).any() == True or (serie == 0).any() == True:
                        Errores[2] = 10000
                        Errores[3] = 10000

                    Indicador = Errores.index(min(Errores))

                    if Indicador == 0:
                        model1 = auto_arima(serie, test='adf', error_action='ignore', suppress_warnings=True, stepwise=True,
                                        seasonal=False)
                        prediccion = model1.predict(7)
                        index = pd.date_range(serie.tail(1).index.item() + timedelta(days=7), periods=7, freq='W')
                        prediccion = pd.Series(prediccion, index=index)

                    elif Indicador == 1:
                        model2 = auto_arima(serie_log, test='adf', error_action='ignore', suppress_warnings=True,
                                        stepwise=True, seasonal=False)
                        prediccion = np.exp(model2.predict(7))
                        index = pd.date_range(serie.tail(1).index.item() + timedelta(days=7), periods=7, freq='W')
                        prediccion = pd.Series(prediccion, index=index)

                    elif Indicador == 2:
                        model3 = ExponentialSmoothing(serie, trend='mul', seasonal=None).fit()
                        prediccion = model3.forecast(7)
                        index = pd.date_range(serie.tail(1).index.item() + timedelta(days=7), periods=7, freq='W')
                        prediccion = pd.Series(prediccion.values, index=index)

                    else:
                        model4 = ExponentialSmoothing(serie_log, trend='mul', seasonal=None).fit()
                        prediccion = np.exp(model4.forecast(7))
                        index = pd.date_range(serie.tail(1).index.item() + timedelta(days=7), periods=7, freq='W')
                        prediccion = pd.Series(prediccion.values, index=index)

                    original = serie.tail(12)
                    desagregado_original = pd.DataFrame(np.repeat(original.values / 7, np.repeat(7, 12, axis=0), axis=0))
                    desagregado_original.set_index(pd.date_range(start=original.index[0], freq="D", periods=desagregado_original.size), inplace=True)

                    desagregado_original['Month'] = desagregado_original.index.month
                    desagregado_original['Year'] = desagregado_original.index.year
                    desagregado_original.columns = ["Unidades", 'Month', 'Year']

                    desagregado = pd.DataFrame(np.repeat(prediccion.values / 7, np.repeat(7, len(prediccion), axis=0), axis=0))
                    desagregado.set_index(pd.date_range(start=prediccion.index[0], freq="D", periods=desagregado.size),
                                      inplace=True)
                    desagregado['Month'] = desagregado.index.month
                    desagregado['Year'] = desagregado.index.year
                    desagregado.columns = ["Unidades", 'Month', 'Year']

                    desagregado_total = desagregado_original.append(desagregado)
                    mensual_total = desagregado_total.groupby(["Year", "Month"])["Unidades"].agg(['size', 'sum'])

                    mensual_total = mensual_total.reset_index()
                    dias = []

                    for k in range(len(mensual_total)):
                        dias.append(calendar.monthrange(mensual_total.iloc[k, 0], mensual_total.iloc[k, 1])[1])

                    mensual_total["dias"] = dias
                    mensual_total = mensual_total[mensual_total['size'] == mensual_total['dias']]
                    mensual_total = mensual_total.drop(columns=['size', 'dias'])
                    mensual_total["product"] = np.repeat(df_filter_aux.iloc[i, 0], len(mensual_total), axis=0)
                    mensual_total["estrato"] = np.repeat(df_filter_aux.iloc[i, 1], len(mensual_total), axis=0)

                    mensual_grafico = mensual_grafico.append(mensual_total)

                except:
                    pass

            mensual_grafico["sum"] = mensual_grafico["sum"].astype('float').round(0)
            mensual_grafico["id"] = 'Estrato:' + mensual_grafico['estrato'].astype(str) + " " + 'Product:' + \
                                        mensual_grafico['product']
            mensual_grafico["Date"] = pd.to_datetime(dict(year=mensual_grafico.Year, month=mensual_grafico.Month, day=1))
            fig = px.bar(mensual_grafico, x='Date', y='sum',
                         hover_data=['sum'], color='id',
                         #height=490,
                         template="plotly_dark",
                         color_discrete_sequence=["#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"],
                        )
            fig.update_xaxes(tickangle=0)
            fig.update_layout(
                              yaxis_title="Quantity",
                              title={
                                  'text': 'BEST SELLING PRODUCTS - SALES FORECASTING  (6 WEEKS MAX.)',
                                  'y': 0.03,
                                  'x': 0.5,
                              },
                              font=dict(
                                      family='Barlow, sans-serif',
                                      size=12,
                                      color="LightBlue"),
                              legend=dict(
                                  yanchor="top",
                                  y=1.49,
                                  xanchor="left",
                                  x=0.01)
            )

            return fig
