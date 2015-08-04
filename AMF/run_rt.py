########################################################
# run_rt.py: response-time prediction 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2015/7/29
# Implemented approach: AMF
# Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
########################################################

import numpy as np
import os, sys, time
import multiprocessing
sys.path.append('src')
# Build external model
if not os.path.isfile('src/core.so'):
	print 'Lack of core.so (built from the C++ module).' 
	print 'Please first build the C++ code into core.so by using: '
	print '>> python setup.py build_ext --inplace'
	sys.exit()
from utilities import *
import evaluator
import dataloader
import resulthandler


#########################################################
# config area
#
para = {'dataType': 'rt', # choose 'rt' for response-time prediction
		'dataPath': '../data/dataset#2/',
		'outPath': 'result/raw/',
		'metrics': ['MAE', 'NMAE', 'RMSE', 'MRE', 'NPRE'], # delete where appropriate		
		'density': list(np.arange(0.05, 0.51, 0.05)), # matrix density
		'rounds': 2, # how many runs are performed at each matrix density
		'dimension': 10, # dimenisionality of the latent factors
		'eta': 0.8, # learning rate
		'lambda': 0.0003, # regularization parameter
		'maxIter': 50, # the max iterations
        'beta': 0.3, # the controlling weight of exponential moving average
		'saveTimeInfo': False, # whether to keep track of the running time
		'saveLog': True, # whether to save log into file
		'debugMode': False, # whether to record the debug info
        'parallelMode': False # whether to leverage multiprocessing for speedup
		}

initConfig(para)
#########################################################


startTime = time.clock() # start timing
logger.info('==============================================')
logger.info('AMF: Adaptive Matrix Factorization [ICDCS\'14].')

# load the dataset
dataTensor = dataloader.load(para)
dataTensor = dataTensor[:,:, 0:1]

# run for each density
if para['parallelMode']: # run on multiple processes
    pool = multiprocessing.Pool()
    for density in para['density']:
        for roundId in xrange(para['rounds']):
			pool.apply_async(evaluator.execute, (dataTensor, density, roundId, para))
    pool.close()
    pool.join()
else: # run on single processes
	for density in para['density']:
		for roundId in xrange(para['rounds']):
			evaluator.execute(dataTensor, density, roundId, para)

# result handling
numTimeSlice = dataTensor.shape[2]
resulthandler.process(para, numTimeSlice)

logger.info(time.strftime('All done. Total running time: %d-th day - %Hhour - %Mmin - %Ssec.',
         time.gmtime(time.clock() - startTime)))
logger.info('==============================================')
sys.path.remove('src')