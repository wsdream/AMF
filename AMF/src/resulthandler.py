########################################################
# resulthandler.py: get the average values of the results
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/11/14
########################################################

import numpy as np
import linecache
import os, sys, time
import cPickle as pickle
from utilities import *
 

########################################################
# Process the raw results to get the average statistics
#
def process(para, numTimeSlice):
    resultFolder = para['outPath'].split('/')[0] + '/'
    rounds = para['rounds']
    skippedHeader = 6
            
    for den in para['density']:
        result = np.zeros((rounds, len(para['metrics']), numTimeSlice))
        for timeslice in xrange(numTimeSlice):
            evalResults = np.zeros((rounds, len(para['metrics']))) 
            timeResults = np.zeros((rounds, 1))
            for rnd in xrange(rounds):
                inputfile = para['outPath'] + '%02d_%sResult_%.2f.round%02d'\
                    %(timeslice + 1, para['dataType'], den, rnd + 1)
                with open(inputfile, 'rb') as fid:
                    data = pickle.load(fid)
                os.remove(inputfile)
                (evalResults[rnd, :], timeResults[rnd]) = data
            outFile = '%s%02d_%sResult_%.2f.txt'\
                %(para['outPath'], timeslice + 1, para['dataType'], den)
            saveResult(outFile, evalResults, timeResults, para) 
            result[:, :, timeslice] = evalResults
        resultOfRounds = np.average(result, axis=2)
        outfile = resultFolder + 'avg_%sResult_%.2f.txt'%(para['dataType'], den)
        saveAvgResult(outfile, resultOfRounds, para)
        avgResult = np.average(resultOfRounds, axis=0)
        print avgResult
########################################################


########################################################
# Save the average results into file
#
def saveAvgResult(outfile, result, para):
    fileID = open(outfile, 'w')
    fileID.write('Metric: ')
    for metric in para['metrics']:
        fileID.write('| %s\t'%metric)
    avgResult = np.average(result, axis=0)         
    fileID.write('\nAvg:\t')
    np.savetxt(fileID, np.matrix(avgResult), fmt='%.4f', delimiter='\t')
    stdResult = np.std(result, axis=0)
    fileID.write('Std:\t')
    np.savetxt(fileID, np.matrix(stdResult), fmt='%.4f', delimiter='\t')
    fileID.write('\n==========================================\n')
    fileID.write('Detailed results for %d rounds:\n'%result.shape[0])
    np.savetxt(fileID, result, fmt='%.4f', delimiter='\t')     
    fileID.close()
########################################################
