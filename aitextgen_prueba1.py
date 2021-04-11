# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:48:52 2021

@author: pepe
"""

import os
import time
import logging
logging.basicConfig(
        format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )
from aitextgen import aitextgen


# get to the wanted data
os.chdir('C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo')
print("Current Working Directory " , os.getcwd())
file_name = 'database(hasta03-08).txt'
model_path = 'C:/Users/pepe/httrack/scrapper_elconfidencial/www.elconfidencial.com/espana/tiempo/models'
## TO GET INFO OF THE TRAIN PARAMS: help(aitextgen.train) || aitextgen.train.__doc__

if __name__ == "__main__":

    ai = aitextgen(model="datificate/gpt2-small-spanish",  to_gpu=True)
    
    start_time = time.time()
    ai.train(file_name,
             line_by_line=False,
             num_steps=2000, # cuanras veces has visto los datos. va en relacion a num de batches.
             generate_every=500,
             save_every=1000,
             save_gdrive=False,
             learning_rate=1e-3,
             batch_size=2, # split # un batch un step. 20 veces hay que oasar los datos.
             outputdir=model_path
             )
    
    time = (time.time() - start_time)/60
    print("--- {} minutes ---".format(time))
    
    ai.save()
