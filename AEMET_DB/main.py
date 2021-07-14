# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:51:35 2020

@author: pepe

This is the main script to download data from the AEMET OpenDATA. 
Here is a few thing to take into account when using this script:
    
    - All of the directories are pointing to local files, so it is necessary
    to update this information
    
    - This script imports functions, which intetacts with the API to get 
    the meteorological values and the text predictions, does some text cleaning,
    and merges this information by 'provincia'
    
    - The collections are made by months. You can select a year and a month
    and a csv for each month will be created, with the numerical data and the 
    text predictions organized by date and region
    
    - In the 'main_directory' selected, you will have each year on a directory
    and inside each directory all csv corresponding to each month
    
    - The dicctionary 'provincias' is used to link each region to the number key
    that identifies each one on the API
    
    - Be aware that it takes approximately 90 minutes to collect each month 
    of data
"""

from __future__ import print_function
import time
import os
import pandas as pd
import os.path
import datetime, calendar
import functions


# Setp-up Variables -------------------------------------------------------

provincias = {
  "A CORUÑA": "15",
  "ALBACETE": "02",
  "ALICANTE": "03",
  "ARABA/ALAVA": "01",
  "ASTURIAS": "33",
  "ALMERIA": "04",
  "AVILA": "05",
  "BADAJOZ": "06",
  "ILLES BALEARS": "07",
  "BARCELONA": "08",
  "BIZKAIA": "48",
  "BURGOS": "09",
  "CACERES": "10",
  "CADIZ": "11",
  "CANTABRIA": "39",
  "CASTELLON": "12",
  "CEUTA": "51",
  "CIUDAD REAL": "13",
  "CORDOBA": "14",
  "CUENCA": "16",
  "GIRONA": "17",
  "GRANADA": "18",
  "GUADALAJARA": "19",
  "GIPUZKOA": "20",
  "HUELVA": "21",
  "HUESCA": "22",
  "JAEN": "23",
  "LEON": "24",
  "LLEIDA": "25",
  "LUGO": "27",
  "MADRID": "28",
  "MALAGA": "29",
  "MELILLA": "52",
  "MURCIA": "30",
  "NAVARRA": "31",
  "OURENSE": "32",
  "PALENCIA": "34",
  "LAS PALMAS": "35",
  "PONTEVEDRA": "36",
  "LA RIOJA": "26",
  "SALAMANCA": "37",
  "STA. CRUZ DE TENERIFE": "38",
  "SEGOVIA": "40",
  "SEVILLA": "41",
  "SORIA": "42",
  "TARRAGONA": "43",
  "TERUEL": "44",
  "TOLEDO": "45",
  "VALENCIA": "46",
  "VALLADOLID": "47",
  "ZAMORA": "49",
  "ZARAGOZA": "50"
}
tipo = ['texto', 'valores']
main_directory = 'Scrapped-by-Years' 
year = 2021
months = [1,2,3]

# Setp-up Directories -------------------------------------------------------

os.chdir(main_directory)
if os.path.exists(str(year)):
    os.chdir(str(year))

else:
    os.mkdir(str(year))
    os.chdir(str(year))
print("Current Working Directory " , os.getcwd())

# Start collecging -------------------------------------------------------

start_time = time.time()
dates_unaccepted = []
for month in months:
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    appended_data = []
    for day in days:
        fecha = str(day)
        try:
            url_values = functions.get_url(tipo[1], fecha, '01')
            df_values = functions.get_values(url_values)
            if not functions.internet_on:
                time.sleep(60)
            df_pred = functions.df_text(provincias, fecha)
            temp_df = functions.merge_df(df_values, df_pred)   
            appended_data.append(temp_df)
            print(" ###################### Dataframe of day {} generated ########################".format(fecha))
        except:
            print('¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ Not validate date: {} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(fecha))
            dates_unaccepted.append(fecha)
            pass
        
    print(" ........................... GENERATING FINAL CSV FILE FOR DATE {}........................".format(fecha))
    final_df = pd.concat(appended_data)
    final_df.to_excel("{}.xlsx".format(month))
time = (time.time() - start_time)/60
print("--- {} minutes ---".format(time))



    
    


    


    
    