# -*- coding: utf-8 -*-
"""
Created on Mon May 17 21:22:06 2021

@author: pepe
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:28:03 2021

@author: pepe

This simple script is for get all the information of a trained model

"""
import pandas as pd
from nlgeval import compute_individual_metrics
import os
from aitextgen import aitextgen

os.chdir('/home/gth07a/home/jbzapata/Work/DATABASE')
print("Current Working Directory " , os.getcwd())

model = 'trained_model_scratch'
ai = aitextgen(model_folder=model, tokenizer_file="aitextgen.tokenizer.json", to_gpu=True)
# disable tokenizer paralelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    report = ai.__repr__()
    print(report)

if __name__ == "__main__":
   main()

