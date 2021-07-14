# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:16:53 2021

@author: pepe

This script is for training a GPT-2 from scratch. 
All the information needed to understand the code is available in:
https://docs.aitextgen.io/tutorials/model-from-scratch/

The input data used is the text predictions of the database. Notice that the
'vocab_file' created by the function 'train_tokenizer' must be in the current 
working directory to correctly load the model 'aitextgen'

"""
import os
from aitextgen import aitextgen, tokenizers
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import build_gpt2_config
from aitextgen.TokenDataset import TokenDataset
from transformers import AutoTokenizer, AutoModelWithLMHead
from pytorch_lightning import loggers
import torch

# Get to the wanted data
os.chdir('/home/gth07a/home/jbzapata/Work/DATABASE')
print('#'*70)
print("Current Working Directory " , os.getcwd())
print('#'*70)
file_name = 'database_training_linebyline.csv'
vocab_file = 'aitextgen.tokenizer.json'
model_path = 'trained_model'
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
       
    train_tokenizer(file_name, vocab_size=4000, save_path=model_path, min_frequency = 5, bos_token ="<bos>", eos_token = "<eos>")
    config = build_gpt2_config(vocab_size=4000, max_length=100, dropout=0.0, n_embd=256, n_layer=4, n_head=4)
    ai = aitextgen(tokenizer_file=vocab_file, config=config, to_gpu=True)

    data = TokenDataset(file_name, tokenizer_file=vocab_file, block_size=100, line_by_line = True)

    # GPT-2 Model size is directly proportional to vocab_size * embeddings.
    tb_logger = loggers.TensorBoardLogger('logs/')
    epochs = int(239042/16) * 15 # read 15 times all data
    ai.train(data,
             num_steps=epochs, 
             generate_every=epochs/4,
             save_every=epochs/4,
             learning_rate=1e-3,
             loggers=tb_logger,
             batch_size=16,
             outputdir=model_path
             )    
    ai.save()
    
if __name__ == "__main__":
   main()