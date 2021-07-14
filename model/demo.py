"""
Created on Tue Jul 03 09:59:10 2021

@author: pepe

- This Script launches a demo using the library Gradio. 
- Only data from 2020 is considered in order to reduce complexity. 
- The user selects a date and a Region, the output is the AEMET prediction, 
  and the model generation following the input Region and date.

"""
import gradio
import os
from aitextgen import aitextgen
import pandas as pd
#from google_trans_new import google_translator  
  

# Get to the trained_model directory
os.chdir('/home/gth07a/home/jbzapata/Work/probar_modelos')
# Define the main objects and variables
model = 'trained_model_exp_5'
df = pd.read_excel('FINAL_DATABASE_2020.xlsx', engine = 'openpyxl')
ai = aitextgen(model_folder=model, tokenizer_file="aitextgen.tokenizer.json", to_gpu=True)
#translator = google_translator() 
special_tokens = ['prov','mes', 'sol','prec', 'tmed','tmin','htmin',
                 'tmax', 'htmax', 'dir', 'vmed', 'racha','itmed','itmin','itmax']

def setup_tokens(special_tokens): #adds seed format in a list
    tokens = []
    for token in special_tokens:
        token = '<' + token + '>'
        tokens.append(token)
    return tokens

def get_prompt(row,tokens): #add seeds to df values 
    row = row.astype(str)
    prompt =  tokens[0] + str(row.provincia.values[0]) + tokens[1] + str(row.mes.values[0])+ \
    tokens[2]  + str(row.sol_tag.values[0]) + tokens[3] + str(row.prec_tag.values[0]) + \
    tokens[4] + str(row.tmed_tag_tmp.values[0]) + tokens[5] + str(row.tmin_tag_tmp.values[0]) + \
    tokens[6] + str(row.horatmin_tag.values[0]) + tokens[7] + str(row.tmax_tag_tmp.values[0]) + \
    tokens[8] + str(row.horatmax_tag.values[0]) + tokens[9] + str(row.dir_tag.values[0]) + \
    tokens[10] + str(row.velmedia_tag.values[0]) + tokens[11] + str(row.racha_tag.values[0]) + \
    tokens[12] + str(row.tmed_tag.values[0]) + tokens[13] + str(row.tmin_tag.values[0]) + \
    tokens[14] + str(row.tmax_tag.values[0]) + '<ini>' 
    return prompt

def get_target_generated(generated, prompt,tokens):
    generated = str(generated.lstrip())
    for token in tokens:
        prompt = prompt.replace(token,'')  
    prompt = prompt.replace('<ini>','')
    target_generated = generated.replace(prompt,'')
    return target_generated

def predict(fecha, provincia):
    fecha = str(fecha)
    provincia = str(provincia)
    df_tmp = df.loc[(df['fecha'] == fecha) & (df['provincia'] == provincia)]
    tokens = setup_tokens(special_tokens)
    prompt = get_prompt(df_tmp,tokens)
    generated = ai.generate_one(prompt = prompt, temperature = 0.7)
    generated = get_target_generated(generated, prompt, tokens)
    #generated_translated = translator.translate(generated,lang_tgt='en')
    aemet = str(df_tmp.prediccion.values[0]) + '  '*50
    #aemet_translated = translator.translate(aemet,lang_tgt='en')
    gpt2 = generated + '  '*50
    return aemet, gpt2

fecha = gradio.inputs.Textbox(lines = 1, placeholder="2020-07-13", label = 'Date')
#provincia = gradio.inputs.Textbox(lines =1, placeholder="i.e., BARCELONA", label = 'Spanish Region')
provincia = gradio.inputs.Dropdown([
    "A CORUNA",
    "ALBACETE",
    "ALICANTE",
    "ARABA/ALAVA",
    "ASTURIAS",
    "ALMERIA",
    "AVILA",
    "BADAJOZ",
    "ILLES BALEARS",
    "BARCELONA",
    "BIZKAIA",
    "BURGOS",
    "CACERES",
    "CADIZ",
    "CANTABRIA",
    "CASTELLON",
    "CEUTA",
    "CIUDAD REAL",
    "CORDOBA",
    "CUENCA",
    "GIRONA",
    "GRANADA",
    "GUADALAJARA",
    "GIPUZKOA",
    "HUELVA",
    "HUESCA",
    "JAEN",
    "LEON",
    "LLEIDA",
    "LUGO",
    "MADRID",
    "MALAGA",
    "MELILLA",
    "MURCIA",
    "NAVARRA",
    "OURENSE",
    "PALENCIA",
    "LAS PALMAS",
    "PONTEVEDRA",
    "LA RIOJA",
    "SALAMANCA",
    "STA. CRUZ DE TENERIFE",
    "SEGOVIA",
    "SEVILLA",
    "SORIA",
    "TARRAGONA",
    "TERUEL",
    "TOLEDO",
    "VALENCIA",
    "VALLADOLID",
    "ZAMORA",
    "ZARAGOZA"
    ], label = 'Spanish Region')

aemet = gradio.outputs.Textbox(label="Original text from AEMET")
gpt2 = gradio.outputs.Textbox(label="GPT-2 generation")
#aemet_translated = gradio.outputs.Textbox(label="AEMET translation")
#gpt2_translated = gradio.outputs.Textbox(label="GPT-2 generation translation")
title = "GPT-2 for meteorological forecasts in Spanish"
article = "<p style='text-align: center'><strong>Pepe Ballesteros, Universidad Politecnica de Madrid. In collaboration with RTVE.</strong></p><p style='text-align: center'>Contact: j.bzapata@alumnos.upm.es</p>"
example = [['2020-04-17','BARCELONA']]

INTERFACE = gradio.Interface(fn=predict, inputs=[fecha,provincia], outputs=[aemet,gpt2], title=title,
                 article = article, examples = example,
                 layout = 'horizontal', allow_flagging =False)

INTERFACE.launch(inbrowser=True, share = True)