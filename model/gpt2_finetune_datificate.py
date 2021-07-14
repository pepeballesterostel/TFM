# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:48:52 2021

@author: pepe

This script fine-tunes the available model in HuggingFace called Datificate:
    https://huggingface.co/datificate/gpt2-small-spanish

The input data to the model are the text predictions of the database. 
    
"""

import os
import logging
logging.basicConfig(
        format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )
from aitextgen import aitextgen
from aitextgen.TokenDataset import TokenDataset
from transformers import AutoTokenizer, AutoModelWithLMHead
import torch

# Get to the wanted data
os.chdir('/home/gth07a/home/jbzapata/Work/DATABASE')
print('#'*70)
print("Current Working Directory " , os.getcwd())
print('#'*70)
file_name = 'training_linebyline.csv'
model_path = '/home/gth07a/home/jbzapata/Work/models'
# disable tokenizer paralelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def main():
    # Check for CUDA
    if torch.cuda.is_available():
       print('#'*70)
       print('CUDA is available for training')
       print('#'*70)
    else:
       print('#'*70)
       print('CUDA not availabe, please check it')
       print('#'*70)
    #tokenizer = AutoTokenizer.from_pretrained("datificate/gpt2-small-spanish")
    #ai = aitextgen(model="datificate/gpt2-small-spanish", to_gpu=True)  
    ai = aitextgen(model_folder='trained_model_datificate', to_gpu=True)
    epochs = int(213955/2)*3
    ai.train(file_name,
             line_by_line=True,
             num_steps=epochs, 
             generate_every=213955/4,
             save_every=213955/4, 
             learning_rate=1e-4,
             batch_size=2,
             outputdir=model_path
             )    
    ai.save()
    
if __name__ == "__main__":
   main()

