import pandas as pd
import os
import geopandas as gpd
DATA_DIR = "data"


def get_dataframe():
    ds_path1 = os.path.join(DATA_DIR, "df_1st_v3.csv.gz")
    ds_path2 = os.path.join(DATA_DIR, "df_2nd_v3.csv.gz")
    df1 = pd.read_csv(ds_path1, sep=',', low_memory=False, parse_dates=['date'])
    df2 = pd.read_csv(ds_path2, sep=',', low_memory=False, parse_dates=['date'])
    return pd.concat([df1, df2])


def get_neighbors():
    cali_path         = os.path.join(DATA_DIR, "Cali.geojson")
    bogota_path       = os.path.join(DATA_DIR, "poligonos-localidades.geojson")
    barranquilla_path = os.path.join(DATA_DIR, "Barranquilla.geojson")
    itagui_path       = os.path.join(DATA_DIR, "Barrios_Itagui.geojson")
    soacha_path       = os.path.join(DATA_DIR, "Soacha.geojson")
    barriosExtra_path = os.path.join(DATA_DIR, "Barrios_extra.geojson")
    medellin_path     = os.path.join(DATA_DIR, "Medellin.geojson")

    # Load geographic information
    # Medellin
    barrios_Med = gpd.read_file(medellin_path)
    barrios_Med['BARRIO'] = barrios_Med['BARRIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode(
        'utf-8')
    barrios_Med['BARRIO'] = barrios_Med['BARRIO'].str.upper()
    barrios_Med = barrios_Med[['BARRIO', 'geometry']]
    barrios_Med['CIUDAD'] = "MEDELLIN"
    barrios_Med.rename(columns={'geometry': 'GEOMETRY', }, inplace=True)

    # Bogota
    barrios_Bog = gpd.read_file(bogota_path)
    barrios_Bog['Nombre de la localidad'] = barrios_Bog['Nombre de la localidad'].str.normalize('NFKD').str.encode(
        'ascii', errors='ignore').str.decode('utf-8')
    barrios_Bog['Nombre de la localidad'] = barrios_Bog['Nombre de la localidad'].str.upper()
    barrios_Bog = barrios_Bog[['Nombre de la localidad', 'geometry']]
    barrios_Bog['CIUDAD'] = "BOGOTA"
    barrios_Bog.rename(columns={'geometry': 'GEOMETRY', 'Nombre de la localidad': 'BARRIO'}, inplace=True)

    # Cali
    barrios_Cal = gpd.read_file(cali_path)
    barrios_Cal['BARRIO'] = barrios_Cal['BARRIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode(
        'utf-8')
    barrios_Cal['BARRIO'] = barrios_Cal['BARRIO'].str.upper()
    barrios_Cal = barrios_Cal[['BARRIO', 'geometry']]
    barrios_Cal['CIUDAD'] = "CALI"
    barrios_Cal.rename(columns={'geometry': 'GEOMETRY'}, inplace=True)

    # Barranquilla
    barrios_Bar = gpd.read_file(barranquilla_path)
    barrios_Bar['NOMBRE'] = barrios_Bar['NOMBRE'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode(
        'utf-8')
    barrios_Bar['NOMBRE'] = barrios_Bar['NOMBRE'].str.upper()
    barrios_Bar = barrios_Bar[['NOMBRE', 'geometry']]
    barrios_Bar['CIUDAD'] = "BARRANQUILLA"
    barrios_Bar.rename(columns={'geometry': 'GEOMETRY', 'NOMBRE': 'BARRIO'}, inplace=True)

    # Itagui
    barrios_Ita = gpd.read_file(itagui_path)
    barrios_Ita['nom_barrio'] = barrios_Ita['nom_barrio'].str.normalize('NFKD').str.encode('ascii',
                                                                                           errors='ignore').str.decode(
        'utf-8')
    barrios_Ita['nom_barrio'] = barrios_Ita['nom_barrio'].str.upper()
    barrios_Ita = barrios_Ita[['nom_barrio', 'geometry']]
    barrios_Ita['CIUDAD'] = "ITAGUI"
    barrios_Ita.rename(columns={'geometry': 'GEOMETRY', 'nom_barrio': 'BARRIO'}, inplace=True)

    # Soacha
    barrios_Soa = gpd.read_file(soacha_path)
    barrios_Soa['MpNombre'] = barrios_Soa['MpNombre'].str.normalize('NFKD').str.encode('ascii',
                                                                                       errors='ignore').str.decode(
        'utf-8')
    barrios_Soa['MpNombre'] = barrios_Soa['MpNombre'].str.upper()
    barrios_Soa = barrios_Soa[['MpNombre', 'geometry']]
    barrios_Soa['CIUDAD'] = "SOACHA"
    barrios_Soa.rename(columns={'geometry': 'GEOMETRY', 'MpNombre': 'BARRIO'}, inplace=True)

    # Barrios Extra
    barrios_extra = gpd.read_file(barriosExtra_path)
    barrios_extra['NOM_BARRIO'] = barrios_extra['NOM_BARRIO'].str.normalize('NFKD').str.encode('ascii',
                                                                                               errors='ignore').str.decode(
        'utf-8')
    barrios_extra['NOM_BARRIO'] = barrios_extra['NOM_BARRIO'].str.upper()
    barrios_extra = barrios_extra[['NOM_BARRIO', 'geometry']]
    barrios_extra['CIUDAD'] = "EXTRA"
    barrios_extra.rename(columns={'geometry': 'GEOMETRY', 'NOM_BARRIO': 'BARRIO'}, inplace=True)
    barrios_extra.at[0, 'BARRIO'] = 'GALAPA'
    barrios_extra.at[1, 'BARRIO'] = 'SOLEDAD'

    # Getting unique dataframe with geographic information
    df_barrios = barrios_Med.append(barrios_Bog)
    df_barrios = df_barrios.append(barrios_Cal)
    df_barrios = df_barrios.append(barrios_Bar)
    df_barrios = df_barrios.append(barrios_Ita)
    df_barrios = df_barrios.append(barrios_Soa)
    df_barrios = df_barrios.append(barrios_extra)

    return df_barrios


def neighbors_processing(data):
    # Cleaning column Barrio
    data['Barrio'] = data['Barrio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    data['Barrio'] = data['Barrio'].str.upper()

    # Data cleaning in the dataset to join with geographic information
    dicti = {"CAMPO VALDES NO 1": "CAMPO VALDES NO.1",
             "CAMPO VALDES NO 2": "CAMPO VALDES NO.2",
             "MANRIQUE CENTRAL NO 2": "MANRIQUE CENTRAL NO.2",
             "MANRIQUE CENTRAL NO 1": "MANRIQUE CENTRAL NO.1",
             "UNICO SAN CRISTOBAL": "SAN CRISTOBAL",
             "UNICO ENGATIVA": "ENGATIVA",
             "UNICO BOSA": "BOSA",
             "UNICO SUBA": "SUBA",
             "UNICO CIUDAD KENNEDY": "KENNEDY",
             "UNICO CHAPINERO": "CHAPINERO",
             "UNICO FONTIBON": "FONTIBON",
             "UNICO CIUDAD BOLIVAR": "CIUDAD BOLIVAR",
             "UNICO TUNJUELITO": "TUNJUELITO",
             "UNICO BARRIOS UNIDOS": "BARRIOS UNIDOS",
             "UNICO RAFAEL URIBE URIBE": "RAFAEL URIBE URIBE",
             "UNICO USME": "USME",
             "UNICO TEUSAQUILLO": "TEUSAQUILLO",
             "UNICO LOS MARTIRES": "LOS MARTIRES",
             "UNICO USAQUEN": "USAQUEN",
             "UNICO PUENTE ARANDA": "PUENTE ARANDA",
             "UNICO ANTONIO NARINO": "ANTONIO NARINO",
             "ANTONIO NARIÑO": "ANTONIO NARINO",
             "UNICO SANTA FE": "SANTA FE",
             "EL INGENIO III": "EL INGENIO",
             "SAN LUIS I": "SAN LUIS",
             "BARRIO RESIDENCIAL EL BOSQUE": "EL BOSQUE",
             "ACUEDUCTO SAN ANTONIO": "SAN ANTONIO",
             "ALFONSO LOPEZ 1.A ETAPA.": "ALFONSO LOPEZ I",
             "URBANIZACION CORTIJO": "EL CORTIJO",
             "CIUDAD 2.000": "CIUDAD 2000",
             "LA RIVERA II": "LOS ANDES B - LA RIVIERA",
             "ABAJO": "BARRIO ABAJO",
             "ALTOS DEL PRADO": "ALTO PRADO",
             "CIUDAD 20 DE JULIO": "20 DE JULIO",
             "LOS ANDRES": "LOS ANDES",
             "LOS OLIVOS": "LOS OLIVOS I",
             "PARTE DE PARAISO": "PARAISO",
             "VILLA SAN PEDRO": "SAN PEDRO",
             "SANTA MARIA NRO. 1": "SANTA MARIA 1",
             "UNICO SOACHA": "SOACHA",
             "UNICA SOLEDAD": "SOLEDAD",
             "EL CARMELO NRO. 1": "EL CARMELO",
             "SAN JOSE PARTE BAJA": "SAN JOSE",
             "UNICO GALAPA": "GALAPA",
             "7 DE AGOSTO": "GALAPA"
             }

    data = data.replace({"Barrio": dicti})
    data.rename(columns={'Barrio': 'BARRIO'}, inplace=True)

    return data

def get_city_lat_lon(select_ciudad):
    # Set latitud and longitude for each city
    if select_ciudad == "ITAGUI":
        latitude = 6.18461
        longitude = -75.59913

    elif select_ciudad == "MEDELLIN":
        latitude = 6.25184
        longitude = -75.56359

    elif select_ciudad == "BOGOTA":
        latitude = 4.60971
        longitude = -74.08175

    elif select_ciudad == 'CALI':
        latitude = 3.43722
        longitude = -76.5225

    elif select_ciudad == 'BELLO':
        latitude = 6.333
        longitude = -75.55

    elif select_ciudad == 'BARRANQUILLA':
        latitude = 10.96854
        longitude = -74.78132

    elif select_ciudad == 'SOACHA':
        latitude = 4.583
        longitude = -74.217

    elif select_ciudad == 'SOLEDAD':
        latitude = 10.91843
        longitude = -74.76459

    elif select_ciudad == 'SABANETA':
        latitude = 6.15153
        longitude = -75.61657

    elif select_ciudad == 'ENVIGADO':
        latitude = 6.17591
        longitude = -75.59174

    elif select_ciudad == 'GALAPA':
        latitude = 10.8932
        longitude = -74.8792

    elif select_ciudad == 'LA ESTRELLA':
        latitude = 6.15769
        longitude = -75.64317

    elif select_ciudad == None:
        latitude = 4.60971
        longitude = -74.08175

    return latitude, longitude