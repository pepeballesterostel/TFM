# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:59:10 2021

@author: pepe
"""

import os
from bs4 import BeautifulSoup
import re

# get to the HTML wanted
os.chdir('C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo')
print("Current Working Directory " , os.getcwd())

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

'''
This function scrapes the predictions from ElConfidencial and returns
a list contining each parragraph of interest
'''
def get_scrapped_predictions():
    with open("index.html",'r',encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
        # find text
        sections = []
        for section in soup.findAll('p'):
            text = str(section)
            text = remove_html_tags(text)
            sections.append(text)       
    del sections[2]
    del sections[5]
    return sections

days_dir = os.listdir()
text = []
for day_dir in days_dir:
    os.chdir(day_dir)
    prov_dir = os.listdir()
    for prov in prov_dir:
        os.chdir(prov)
        try:
            processed_text = get_scrapped_predictions()
            text.append(processed_text)
        except:
            pass
        os.chdir("../")
    os.chdir("../")
    
final_list = [item for sublist in text for item in sublist]
with open('database.txt','w',encoding='utf-8') as f:
  f.write('\n'.join(final_list))
  f.close()

