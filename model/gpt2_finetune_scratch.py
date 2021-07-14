# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:16:53 2021

@author: pepe

This script is for fine-tuning the GPT-2 from scratch model. The input data is 
the processed text data from the database. The processing of the data consists
of adding the input seeds with its corresponding values, followed by the 
beggining and ending tokens: '<bos>' and '<eos>', where in between lays the
text prediction. 

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
file_name = 'training_experiment_5.csv'
vocab_file = 'aitextgen.tokenizer.json'
model_path = 'trained_model_scratch'
os.environ["TOKENIZERS_PARALLELISM"] = "false"
special_tokens = ["<prov>","<mes>","<sol>","<prec>","<tmed>","<tmin>","<htmin>","<tmax>","<htmax>","<dir>","<vmed>","<racha>","<itmed>","<itmin>","<itmax>","<ini>"]


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
       
    train_tokenizer(file_name, vocab_size=4000, save_path=model_path, min_frequency = 5, bos_token ="<bos>", eos_token = "<eos>", added_tokens =special_tokens)
    ai = aitextgen(model_folder=model_path, tokenizer_file=vocab_file, to_gpu=True)
    data = TokenDataset(file_name, tokenizer_file=vocab_file, block_size=100, line_by_line = True)

    # GPT-2 Model size is directly proportional to vocab_size * embeddings.
    tb_logger = loggers.TensorBoardLogger('logs/')
    epochs = int(207875/16) * 15 
    ai.train(data,
             num_steps=epochs, 
             generate_every=207875/4,
             save_every=207875/4,
             learning_rate=1e-4,
             loggers=tb_logger,
             batch_size=16,
             outputdir=model_path
             )    
    ai.save()
    
if __name__ == "__main__":
   main()