# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:51:35 2020

@author: pepe
"""
from __future__ import print_function
import time
import requests
import pandas as pd
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import re
from unicodedata import normalize
from urllib.request import urlopen 
from urllib.error import URLError

tipo = ['texto', 'valores']


def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err: 
        return False
    
def get_url(tipo, fecha, provincia):
    # Configure API key authorization: api_key
    configuration = swagger_client.Configuration()
    configuration.api_key['api_key'] = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwZXBlYmFsbGVzdGVyb3MudGVsQGdtYWlsLmNvbSIsImp0aSI6IjhhNDdjOGRmLTMwZmEtNGE3Yi1hZDE0LTExNmM5MjhiOWMwZiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjA0OTQzNjI4LCJ1c2VySWQiOiI4YTQ3YzhkZi0zMGZhLTRhN2ItYWQxNC0xMTZjOTI4YjljMGYiLCJyb2xlIjoiIn0.ypkrf9pPSye9lLqos3y6uSJAeZlYax7FrpzpwOwYQwI'
    if tipo == 'texto':
        # create an instance of the API class
        api_instance = swagger_client.PrediccionesNormalizadasTextoApi(swagger_client.ApiClient(configuration))
        try:
            # Predicción provincia mañana. Archivo.
            api_response = api_instance.prediccin_provincia_maana__archivo_(provincia, fecha)
            pprint(api_response)
            url_data = api_response.datos
        except ApiException as e:       
            print("Exception when calling PrediccionesNormalizadasTextoApi->prediccin_provincia_hoy__archivo_: %s\n" % e)
            pass
    if tipo == 'valores':
        fecha = fecha + 'T00:00:00UTC'
        # create an instance of the API class
        api_instance = swagger_client.ValoresClimatologicosApi(swagger_client.ApiClient(configuration))
        try:
            # Climatologías diarias.
            api_response = api_instance.climatologas_diarias_1(fecha, fecha)
            pprint(api_response)
            url_data = api_response.datos
        except ApiException as e:       
            print("Exception when calling ValoresClimatologicosApi->climatologas_diarias_1: %s\n" % e)
            pass
    time.sleep(2)
    return url_data

def get_values(url):
    data = requests.request("GET", url)
    data = data.json()
    df = pd.DataFrame(data)
    return df
def get_text(url):
    data = requests.request('GET', url)
    text = data.text
    return text
    
def clean_text(text, provincia):
    # Valid function from 2014 to 2012
    # 1. Remove tildes for hey recognition
    text = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", text), 0, re.I
    )
    text = normalize( 'NFC', text)
    # 2. Get only the text we want
    if provincia == 'ILLES BALEARS':
        provincia = 'MENORCA'
    if provincia == 'STA. CRUZ DE TENERIFE':
        provincia = 'TENERIFE'
    if provincia == 'LAS PALMAS':
        provincia = 'LANZAROTE'   
    stripped = text.split('PREDICCION', 1)[1]
    stripped = stripped.split('PREDICCION', 1)[1]
    #stripped = re.sub(r'^.*?\n\n', '\n\n', stripped)
    stripped = stripped.split('\n\n', 1)[1]
    stripped = re.sub(r'^.*?\r\r', '\r\r', stripped)
    stripped = stripped.split('(C)', 1)[0]
    stripped = stripped.split('( C)', 1)[0]
    stripped = stripped.split('TEMPERATURAS MINIMAS Y MAXIMAS PREVISTAS', 1)[0]
    stripped = stripped.split('TEMPERATURA MINIMA Y MAXIMA PREVISTA', 1)[0]
    stripped = stripped.split('TEMPERATURAS MINIMA Y MAXIMA PREVISTAS', 1)[0]
    stripped = stripped.split('TEMPERATURAS PREVISTAS: MINIMAS MAXIMAS', 1)[0]
    stripped = stripped.split('TEMPERATURAS MINIMAS Y MAXIMA PREVISTAS', 1)[0]
    stripped = re.sub("[\(\[].*?[\)\]]", "", stripped)
    single_line = stripped.replace("\r", " ")
    single_line = single_line.replace("\n", " ")
    final_text = single_line.lower()
    return final_text

def df_text(provincias, fecha):
    lst = []
    cols = ['fecha', 'provincia', 'prediccion']
    list_provincias = provincias.keys()
    for provincia in list_provincias:
        provincia_key = provincias[provincia]
        try:
            url = get_url(tipo[0], fecha, provincia_key)
            text = get_text(url)
            text_clean = clean_text(text, provincia)
            lst.append([fecha, provincia, text_clean])
            print(lst)
        except:
            print('--------------- Provincia sin Prediccion: {} -----------------'.format(provincia))
    df = pd.DataFrame(lst, columns=cols ) 
    return df

def merge_df(df_values, df_pred):
    df_merged = pd.merge(df_values, df_pred, on='provincia', how='inner')
    df_merged.rename(columns = {'fecha_x':'fecha'}, inplace = True)
    df_merged.drop(columns='fecha_y', axis=1)
    return df_merged



    
    
    
    
    