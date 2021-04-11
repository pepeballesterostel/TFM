# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:57:06 2021

@author: pepe
"""


import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

"""
This script gets confidencial htmls and creates an excel with information
about the fecha, municipio and prediccion in text.
Remember to run *code_toadd_provinciastoEC* in order to add the provincias
information corresponding to the AEMET dataset.
"""

# get to the HTML wanted
os.chdir('C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo')
print("Current Working Directory " , os.getcwd())

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

'''
This function scrapes the predictions from ElConfidencial and returns
a list contining each cleaned parragraph of interest and the municipio.
'''
def get_municipioyprediccion():
    with open("index.html",'r',encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
        # find text
        sections = []
        for section in soup.findAll('p'):
            text = str(section)
            sections.append(text) 
        soup_tmp = BeautifulSoup(''.join(sections[0]))
        municipio = soup_tmp.b.contents[0]
    del sections[2]
    del sections[5]
    final_sections = []
    for text in sections:
        text = remove_html_tags(text)
        text = re.sub(r'[^\w]', ' ', text)
        text = text.replace("[", " ")
        text = text.replace("]", " ")
        text = text.replace("'", " ")
        final_sections.append(text)
    final_sections = ' '.join(final_sections)
    return municipio, final_sections

start_time = time.time()
days_dir = os.listdir()
df = pd.DataFrame(columns=['fecha', 'municipio', 'prediccion EC'])
for day_dir in days_dir:
    fecha = day_dir
    os.chdir(fecha)
    prov_dir = os.listdir()
    for prov in prov_dir:
        os.chdir(prov)
        try:
            municipio, processed_text = get_municipioyprediccion()
            df = df.append({'fecha': fecha, 'municipio': municipio, 'prediccion EC': processed_text}, ignore_index=True)
        except:
            pass
        os.chdir("../")
    os.chdir("../")
    
df.to_excel("database_elconfidencial_{}_{}.xlsx".format(days_dir[0], days_dir[len(days_dir)-1]))
time = (time.time() - start_time)/60
print("--- {} minutes ---".format(time))
   
