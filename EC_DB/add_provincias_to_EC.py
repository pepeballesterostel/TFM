# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:57:06 2021

@author: pepe

This script adds the Region based on the municipio. This is done in order to 
merge this informaiton to the AEMET database based on date and Region.


import pandas as pd

municipio_provincia = {
  "Santiago de Compostela": "A CORUÑA",
  "Albacete": "ALBACETE",
  "Alicante": "ALICANTE",
  "Benidorm": "ALICANTE",
  "Elche ": "ALICANTE",
  "Torrevieja": "ALICANTE",
  "Vitoria-Gasteiz": "ARABA/ALAVA",
  "Gijón": "ASTURIAS",
  "Oviedo": "ASTURIAS",
  "Siero": "ASTURIAS", 
  "Almería": "ALMERIA",
  "Garrucha": "ALMERIA",
  "Oria": "ALMERIA",
  "El Ejido": "ALMERIA",
  "Níjar": "ALMERIA",
  "Badajoz": "BADAJOZ",
  "Palma": "ILLES BALEARS",
  "Manacor": "ILLES BALEARS",
  "Castelldefels": "BARCELONA",
  "Sabadell": "BARCELONA",
  "Barcelona": "BARCELONA",
  "L' Hospitalet de Llobregat": "BARCELONA",
  "Getxo": "BIZKAIA",
  "Burgos": "BURGOS",
  "Cáceres": "CACERES",
  "Cádiz": "CADIZ",
  "Jerez de la Frontera": "CADIZ",
  "Ciudad Real": "CIUDAD REAL",
  "Tomelloso": "CIUDAD REAL",
  "Cuenca": "CUENCA",
  "Figueres": "GIRONA",
  "Motril": "GRANADA",
  "Guadalajara": "GUADALAJARA",
  "Irun": "GIPUZKOA",
  "Huelva": "HUELVA",
  "Huesca": "HUESCA",
  "Jaén": "JAEN",
  "Linares": "JAEN",
  "Ponferrada": "LEON",
  "Lugo": "LUGO",
  "Las Rozas de Madrid": "MADRID",
  "Madrid": "MADRID",
  "Brunete": "MADRID",
  "Benalmádena": "MALAGA",
  "Estepona": "MALAGA",
  "Málaga": "MALAGA", 
  "Torremolinos": "MALAGA",
  "Cartagena": "MURCIA",
  "Las Palmas de Gran Canaria": "LAS PALMAS",
  "Santa Lucía de Tirajana": "LAS PALMAS",
  "Telde": "LAS PALMAS",
  "Vigo": "PONTEVEDRA",
  "Calahorra": "LA RIOJA",
  "Salamanca": "SALAMANCA",
  "Santa Cruz de Tenerife": "STA. CRUZ DE TENERIFE",
  "Segovia": "SEGOVIA",
  "Sevilla": "SEVILLA",
  "Soria": "SORIA",
  "Talavera de la Reina": "TOLEDO",
  "Toledo": "TOLEDO",
  "Gandia": "VALENCIA",
  "Valencia": "VALENCIA",
  "Zamora": "ZAMORA"
}


def get_provincia(municipio):
    provincia = municipio_provincia[municipio]
    return provincia

# Load the df, add Region, and save it.
df = pd.read_excel('database_elconfidencial_2021-01-26_2021-03-24.xlsx')
df['provincia'] = df['municipio'].apply(get_provincia)
df.to_excel("database_elconfidencial_2021-01-26_2021-03-24.xlsx")
