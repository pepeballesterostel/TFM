# -*- coding: utf-8 -*-
"""
Created on Mon May 17 21:22:06 2021

@author: pepe

This script evaluates the generations on the test set of a Baseline model. The
procedure is to split the reference text in half, so that the first half is the
prompt for the generations, and the second half is evaluated against the second
half of the generation. 

Finally, it returns a csv with the reference, the generated output and the 
obtained metrics.

"""

import pandas as pd
from nlgeval import compute_individual_metrics
import os
from aitextgen import aitextgen

os.chdir('/home/gth07a/home/jbzapata/Work/DATABASE')
print("Current Working Directory " , os.getcwd())

model = 'trained_model_scratch'
df_test = pd.read_excel('UPDATED_DATABASE_TEST.xlsx', engine = 'openpyxl') 
lst = []
cols = ['CompleteReference','reference', 'generated', 'BLEU_1','BLEU_2', 'BLEU_3', 'BLEU_4','ROUGE_L', 
        'EmbeddingAverageCosineSimilairty', 'VectorExtremaCosineSimilarity',
        'GreedyMatchingScore']
# First, lets do the try with much less data.
#df_sample = df_test.sample(n=3)
ai = aitextgen(model_folder=model, tokenizer_file="aitextgen.tokenizer.json", to_gpu=True)
# disable tokenizer paralelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def get_prompt_ref(reference):
    reference_split = reference.split(' ')
    prompt_length = int(len(reference_split)/2)
    target_length = len(reference_split)
    prompt = reference_split[:prompt_length]
    target_reference = reference_split[prompt_length:target_length]
    prompt = ' '.join(prompt)
    target_reference = ' '.join(target_reference)
    prompt = prompt.lstrip()
    return prompt, target_reference

def get_target_generated(generated, prompt):
    generated = str(generated.lstrip())
    target_generated = generated.replace(prompt,'')
    return target_generated

def main():
    for i in range(0,len(df_test)):
        df_tmp = df_test.iloc[i] 
        reference = str(df_tmp.prediccion)
        prompt, target_reference = get_prompt_ref(reference)
        generated = ai.generate_one(prompt = prompt, temperature = 0.8)
        target_generated = get_target_generated(generated, prompt)
        try:
            print('#'*70)
            print('Computing metrics for instance number {}'.format(i))
            print('#'*70)
            target_generated = target_generated.lstrip()
            target_reference = target_reference.lstrip()
            metrics_dict = compute_individual_metrics(target_reference, target_generated, no_skipthoughts=True)
            print('Metrics succesfully competed')
            lst.append([reference ,target_reference, target_generated, metrics_dict['Bleu_1'], metrics_dict['Bleu_2'],
                        metrics_dict['Bleu_3'],  metrics_dict['Bleu_4'],metrics_dict['ROUGE_L'], 
                        metrics_dict['EmbeddingAverageCosineSimilairty'],
                        metrics_dict['VectorExtremaCosineSimilarity'], metrics_dict['GreedyMatchingScore']])

        except:
            print('Sequence is shorter than the required number of steps, for instance {}'.format(i))
            pass
    
    df = pd.DataFrame(lst, columns=cols) 
    df.to_excel('Evaluation_{}.xlsx'.format(model))


if __name__ == "__main__":
   main()

