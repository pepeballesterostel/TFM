# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:28:03 2021

@author: pepe

This script evaluates the generations on the test set of a fine-tuned model.
The special tokens are given as an input (prompt) for the model generation, but they must
be removed form the output string generation of the model. 


Finally, it returns a csv with the reference, the generated output and the 
obtained metrics.

"""
import pandas as pd
from nlgeval import compute_individual_metrics
import os
from aitextgen import aitextgen

# Set the directory
os.chdir('/home/gth07a/home/jbzapata/Work/DATABASE')
print("Current Working Directory " , os.getcwd())

# Charge data and set variables ---------------------------------------------
model = 'trained_model_exp_5'
df_test = pd.read_excel('DATABASE_TEST_EXP_5_WF.xlsx', engine = 'openpyxl')

# Disable tokenizer paralelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"
 
# Initialize variables for final dataframe
lst = []
cols = ['reference', 'generated', 'BLEU_1','BLEU_2', 'BLEU_3', 'BLEU_4','ROUGE_L', 
        'EmbeddingAverageCosineSimilairty', 'VectorExtremaCosineSimilarity',
        'GreedyMatchingScore','provincia','mes','sol','prec','tmed','tmin','horatmin','tmax', 'horatmax', 'dir', 'velmedia', 'racha', 'itmed', 'itmin', 'itmax',
        'sol_n', 'prec_n', 'tmed_n', 'tmin_n', 'horatmin_n', 'tmax_n', 'horatmax_n', 'dir_n', 'velmedia_n', 'racha_n']

special_tokens = ['prov','mes', 'sol','prec', 'tmed','tmin','htmin',
                 'tmax', 'htmax', 'dir', 'vmed', 'racha','itmed','itmin','itmax']

# First, lets do the try with much less data.
df_sample = df_test.sample(n=1000)

# Charge target model into GPU
ai = aitextgen(model_folder=model, tokenizer_file="aitextgen.tokenizer.json", to_gpu=True)

def setup_tokens(special_tokens):
    tokens = []
    for token in special_tokens:
        token = '<' + token + '>'
        tokens.append(token)
    return tokens

def get_prompt(row,tokens):
    row = row.astype(str)
    prompt =  tokens[0] + str(row.provincia) + tokens[1] + str(row.mes)+ \
    tokens[2]  + str(row.sol_tag) + tokens[3] + str(row.prec_tag) + \
    tokens[4] + str(row.tmed_tag_tmp) + tokens[5] + str(row.tmin_tag_tmp) + \
    tokens[6] + str(row.horatmin_tag) + tokens[7] + str(row.tmax_tag_tmp) + \
    tokens[8] + str(row.horatmax_tag) + tokens[9] + str(row.dir_tag) + \
    tokens[10] + str(row.velmedia_tag) + tokens[11] + str(row.racha_tag) + \
    tokens[12] + str(row.tmed_tag) + tokens[13] + str(row.tmin_tag) + \
    tokens[14] + str(row.tmax_tag) + '<ini>' 
    return prompt

def get_target_generated(generated, prompt,tokens):
    generated = str(generated.lstrip())
    for token in tokens:
        prompt = prompt.replace(token,'')  
    prompt = prompt.replace('<ini>','')
    target_generated = generated.replace(prompt,'')
    return target_generated


def main():
    for i in range(0,len(df_sample)):
        df_tmp = df_sample.iloc[i] 
        reference = str(df_tmp.prediccion)
        tokens = setup_tokens(special_tokens)
        prompt = get_prompt(df_tmp,tokens)
        generated = ai.generate_one(prompt = prompt, temperature = 0.7)
        target_generated = get_target_generated(generated, prompt, tokens)
        try:
            print('#'*70)
            print('Computing metrics for instance number {}'.format(i))
            print('#'*70)
            target_generated = target_generated.lstrip()
            reference = reference.lstrip()
            metrics_dict = compute_individual_metrics(reference, target_generated, no_skipthoughts=True)
            print('Metrics succesfully competed')
            lst.append([reference, target_generated, metrics_dict['Bleu_1'], metrics_dict['Bleu_2'],
                        metrics_dict['Bleu_3'],  metrics_dict['Bleu_4'],metrics_dict['ROUGE_L'], 
                        metrics_dict['EmbeddingAverageCosineSimilairty'],
                        metrics_dict['VectorExtremaCosineSimilarity'], metrics_dict['GreedyMatchingScore'],
                        df_tmp.provincia, df_tmp.mes, df_tmp.sol_tag, df_tmp.prec_tag, df_tmp.tmed_tag_tmp, df_tmp.tmin_tag_tmp,
                        df_tmp.horatmin_tag, df_tmp.tmax_tag_tmp, df_tmp.horatmax_tag, df_tmp.dir_tag, df_tmp.velmedia_tag,
                        df_tmp.racha_tag, df_tmp.tmed_tag,df_tmp.tmin_tag,df_tmp.tmax_tag, df_tmp.sol, df_tmp.prec, df_tmp.tmed,
                        df_tmp.tmin, df_tmp.horatmin,df_tmp.tmax,df_tmp.horatmax, df_tmp.dir, df_tmp.velmedia, df_tmp.racha])

        except:
            print('Sequence is shorter than the required number of steps, for instance {}'.format(i))
            pass
    
    df = pd.DataFrame(lst, columns=cols) 
    df.to_excel('Evaluation_{}.xlsx'.format(model))


if __name__ == "__main__":
   main()