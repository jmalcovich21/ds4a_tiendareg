from lib.dataframe_proc import get_dataframe

data = get_dataframe().copy()


def get_portfolio_model(select_product, select_marca, select_ciudad, select_zona):
    if select_product is not None and select_marca is not None and select_ciudad is not None and select_zona is not None:

        # The dataframe filter is performed
        df_filter = data.loc[
            (data['NombreDeProductor'] == select_product) &
            (data['marca'] == select_marca) &
            (data['Municipio'] == select_ciudad) &
            (data['Zona'] == select_zona)
        ]
        # Create a new column with the year-month
        df_filter['Month'] = df_filter['date'].dt.to_period('M')
        # Make the sum of the units sold by month, stratum and sku
        df_filter_aux = df_filter.groupby(['DescripcionLargaProducto', 'Estrato', 'Month'])['Unidades'].sum().to_frame()
        # Calculate the median number of units per month of each sku by stratum and order it in descending order
        df_filter_aux = df_filter_aux.groupby(['DescripcionLargaProducto', 'Estrato'])['Unidades'].median().reset_index(name='Median').sort_values(['Median'], ascending=False)
        # Convert the column Estrato to string type
        df_filter_aux["Estrato"] = df_filter_aux["Estrato"].astype(str)
        # Create a new column where it joins the word Estrato and the number
        df_filter_aux["Estrato2"] = "Estrato " + df_filter_aux["Estrato"]
        # Take the top 5 skus sold by stratum from the calculated median
        return df_filter_aux.head(5)

    elif select_product is None and select_marca is None and select_ciudad is None and select_zona is None:

        data['Month'] = data['date'].dt.to_period('M')
        # Make the sum of the units sold by month, stratum and sku
        df_filter_aux = data.groupby(['DescripcionLargaProducto', 'Estrato', 'Month', 'marca'])['Unidades'].sum().to_frame()
        # Calculate the median number of units per month of each sku by stratum and order it in descending order
        df_filter_aux = df_filter_aux.groupby(['DescripcionLargaProducto', 'Estrato', 'marca'])['Unidades'].median().reset_index(name='Median').sort_values(['Median'], ascending=False)
        # Take the top 10 skus sold from the hole dataset
        return df_filter_aux.head(10)

