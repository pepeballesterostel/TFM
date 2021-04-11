#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


# In[26]:


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


# In[27]:


def get_provincia(municipio):
    provincia = municipio_provincia[municipio]
    return provincia


# In[29]:


df['provincia'] = df['municipio'].apply(get_provincia)


# In[30]:


df.head()


# In[36]:


df = df.drop('Unnamed: 0', axis=1)
df.head()


# In[34]:


df.columns


# In[37]:


df.to_excel("database_elconfidencial_2021-01-26_2021-03-24.xlsx")


# In[22]:


municipio_provincia['Torrevieja ']


# In[11]:


df.municipio.unique()


# In[ ]:


os.chdir('C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo')


# In[ ]:


df = pd.read_excel('database_elconfidencial_2021-01-26_2021-03-24.xlsx')


# In[12]:


len(df.municipio.unique())

