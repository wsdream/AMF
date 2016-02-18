########################################################
# run_rt.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2016/02/15
# Implemented approach: AMF (Adaptive Matrix Factorization)
########################################################

import numpy as np
import os, sys, time
import multiprocessing
from commons.utils import logger
from commons import utils
from commons import evaluator
from commons import dataloader
 

# parameter config area
para = {'dataPath': '../data/',
        'dataName': 'dataset#2',
        'dataType': 'tp', # set the dataType as 'rt' or 'tp'
        'outPath': 'result/',
        'metrics': ['MAE', 'MRE', 'NPRE'], # delete where appropriate      
        'density': np.arange(0.05, 0.51, 0.05), # matrix density
        'rounds': 20, # how many runs are performed at each matrix density
        'dimension': 10, # dimenisionality of the latent factors
        'eta': 0.8, # learning rate
        'lambda': 0.0002, # regularization parameter
        'maxIter': 50, # the max iterations
        'convergeThreshold': 5e-3, # stopping criteria for convergence
        'beta': 0.3, # the controlling weight of exponential moving average
        'saveTimeInfo': False, # whether to keep track of the running time
        'saveLog': True, # whether to save log into file
        'debugMode': False, # whether to record the debug info
        'parallelMode': True # whether to leverage multiprocessing for speedup
        }


startTime = time.time() # start timing
utils.setConfig(para) # set configuration
logger.info('==============================================')
logger.info('AMF: Adaptive Matrix Factorization [TPDS]')

# load the dataset
dataTensor = dataloader.load(para)

# evaluate QoS prediction algorithm
evaluator.execute(dataTensor, para)

logger.info('All done. Elaspsed time: ' + utils.formatElapsedTime(time.time() - startTime)) # end timing
logger.info('==============================================')
