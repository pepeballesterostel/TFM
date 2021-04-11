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

