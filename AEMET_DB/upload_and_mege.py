# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:18:19 2021

@author: pepe
"""


import os
import pandas as pd

os.chdir('C:/Users/pepe/Documents/TFM/data/python-client-generated/Scrapped-by-Years')
print("Current Working Directory: " , os.getcwd())

years = os.listdir()
df = pd.DataFrame()

for year in years:
    os.chdir(year)
    files = os.listdir()
    files_xls = [f for f in files if f[-4:] == 'xlsx']
    for f in files_xls:
        data = pd.read_excel(f)
        df = df.append(data)
    os.chdir("../")


df1 = df.iloc[:545345, :]
df2 = df.iloc[545345:, :]

df1.to_excel('database_AEMET_1part.xlsx')
df2.to_excel('database_AEMET_2part.xlsx')

# -------------------------------------------------------------------------- #
# THIS IS FOR UPLOADING DATA FROM 2021 (WITHOUT RUNNING THE PREV CODE)
# -------------------------------------------------------------------------- #

import os
import pandas as pd

os.chdir('C:/Users/pepe/Documents/TFM/data/python-client-generated/Scrapped-by-Years')
print("Current Working Directory: " , os.getcwd())

df = pd.read_excel('database_AEMET_2part.xlsx')
target_year = 2021
os.chdir(str(target_year))
files = os.listdir()
df_tmp = pd.DataFrame()
for f in files:
    data = pd.read_excel(f)
    df_tmp = df_tmp.append(data)
os.chdir("../")

df = df.append(df_tmp)
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
df.to_excel('DB_AEMET_2.xlsx')

# -------------------------------------------------------------------------- #
# THIS IS FOR MERGING DB2 WITH EC (WITHOUT RUNNING THE PREV CODE)
# -------------------------------------------------------------------------- #

import os
import time
import pandas as pd

os.chdir('C:/Users/pepe/Documents/TFM/data/python-client-generated/Scrapped-by-Years')
print("Current Working Directory: " , os.getcwd())
print('Charging DB AEMET 2 into a DataFrame .........')
start_time = time.time()
df = pd.read_excel('DB_AEMET_2.xlsx')
time = (time.time() - start_time)/60
print("Finished! Total time: --- {} minutes ---".format(time))

os.chdir('C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo')
print("Current Working Directory: " , os.getcwd())
print('Charging DB EC into a DataFrame .........')
df_ec = pd.read_excel('database_elconfidencial_2021-01-26_2021-03-24.xlsx')

print('Merging both DataFrames .........')
# Esto salva el df solo la informacion que comparten. Necesito que 
# la que no comparten no se toque, y la otra se mergee.
df_merged = pd.merge(df, df_ec, on=['fecha','provincia'], how='outer')
print('Finished!')

print('Charging final DB to EXCEL .........')
start_time_2 = time.time()
df_merged.to_excel('DB_AEMET_EC_2.xlsx')
time2 = (time.time() - start_time_2)/60
print("Finished! Total time: --- {} minutes ---".format(time2))

# -------------------------------------------------------------------------- #
# THIS IS FOR CREATING TRAIN/TEST DB (WITHOUT RUNNING THE PREV CODE)
# -------------------------------------------------------------------------- #

import os
import time
import pandas as pd
from sklearn.model_selection import train_test_split


os.chdir('C:/Users/pepe/Documents/TFM/data/python-client-generated/Scrapped-by-Years')
print("Current Working Directory: " , os.getcwd())
print('............... CHARGING DB1 AND DB2 INTO DATAFRAMES ................')
start_time = time.time()
df1 = pd.read_excel('DB_AEMET_1.xlsx')
df2 = pd.read_excel('DB_AEMET_EC_2.xlsx')
time = (time.time() - start_time)/60
print("Finished Charging Dataframes! Total time: --- {} minutes ---".format(time))
print('\n')
print( '............... SPLITTING DATA SET TO TRAIN/TEST ................' )
df = df1.append(df2)
seed = 77
train, test = train_test_split(df, test_size=0.2, random_state=seed)
print('Charging final DB TEST to EXCEL .........')
test.to_excel('DATABASE_TEST.xlsx')
print('Finished!')

print('Charging final DB1 AND DB2 TRAIN to EXCEL .........')
rows = len(train.index) 
split = int(rows/2)
train1 = train.iloc[:split, :]
train2 = train.iloc[split:, :]
train1.to_excel('DATABASE_TRAIN_1.xlsx')
train2.to_excel('DATABASE_TRAIN_2.xlsx')
print('Finished!')



