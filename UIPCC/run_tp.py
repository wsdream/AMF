########################################################
# run_tp.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/6/15
# Implemented approaches: [UMEAN, IMEAN, UPCC, IPCC,  
# and UIPCC]
# Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
########################################################

import numpy as np
import os, sys, time
sys.path.append('src')
# Build external model
if not os.path.isfile('src/UIPCC.so'):
	print 'Lack of UIPCC.so. Please first build the cpp code into UIPCC.so: '
	print 'python setup.py build_ext --inplace'
	sys.exit()
from utilities import *
from predict import *
 

#########################################################
# config area
#
para = {'dataPath': '../data/processedData/tpData/tpTimeSlot',
		'outPath': 'result/',
		'metrics': ['MAE', 'NMAE', 'RMSE', 'MRE', 'NPRE'], # delete where appropriate
		# matrix density
		'density': list(np.arange(0.05, 0.51, 0.05)),
		'timeSlice': 64, # number of time dimensions
		'rounds': 20, # how many runs are performed at each matrix density
		'topK': 10, # the parameter of TopK similar users or services, the default value is
					# topK = 10 as in the reference paper
		'lambda': 0.4, # the combination coefficient of UPCC and IPCC
		'saveTimeInfo': False, # whether to keep track of the running time
		'saveLog': False, # whether to save log into file
		'debugMode': False # whether to record the debug info
		}

initConfig(para)
#########################################################


startTime = time.clock() # start timing
logger.info('==============================================')
logger.info('[UMEAN, IMEAN, UPCC, IPCC, UIPCC]')

for timeslice in range(para['timeSlice']):
	logger.info('==============================================')
	logger.info('Time slice %02d starts.'%(timeslice + 1))
	para['outPath'] = 'result/%02d_tpResult_'%(timeslice + 1)
	datafile = '%s%02d.txt'%(para['dataPath'], timeslice + 1)
	logger.info('Load data: %s'%datafile)
	dataMatrix = np.loadtxt(datafile)

	# run for each density
	for density in para['density']:
		predict(dataMatrix, density, para)
		logger.info('Time slice %02d, density %.2f done.'%(timeslice + 1, density))
		
	logger.info('Time slice %02d done.'%(timeslice + 1))
	logger.info('==============================================')

logger.info(time.strftime('All done. Total running time: %d-th day - %Hhour - %Mmin - %Ssec.',
         time.gmtime(time.clock() - startTime)))
logger.info('==============================================')
sys.path.remove('src')