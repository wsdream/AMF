########################################################
# evallib.py: common functions for evaluator.py
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2015/8/17
# Last updated: 2015/8/30
########################################################

import numpy as np 
from numpy import linalg as LA
import os, sys, time
from commons.utils import logger
import cPickle as pickle
import random


#======================================================#
# Function to compute the evaluation metrics
#======================================================#
def evaluate(testMatrix, recoveredMatrix, para):
    (testVecX, testVecY) = np.where(testMatrix > 0)
    testVec = testMatrix[testVecX, testVecY]
    estiVec = recoveredMatrix[testVecX, testVecY]
    evalResult = errMetric(testVec, estiVec, para['metrics'])
    return evalResult


#======================================================#
# Function to remove the entries of data tensor
# Return the trainTensor and the corresponding testTensor
#======================================================#
def removeTensor(tensor, density, round, para):
    numTime = tensor.shape[2]
    trainTensor = np.zeros(tensor.shape)
    testTensor = np.zeros(tensor.shape)
    for i in range(numTime):
        seedID = round + i * 100
        (trainMatrix, testMatrix) = removeEntries(tensor[:, :, i], density, seedID)
        trainTensor[:, :, i] = trainMatrix
        testTensor[:, :, i] = testMatrix
    return trainTensor, testTensor


#======================================================#
# Function to remove the entries of data matrix
# which uses guassian random sampling
# Return trainMatrix and testMatrix
#======================================================#
def removeEntries(matrix, density, seedID):
    numAll = matrix.size
    numTrain = int(numAll * density)
    (vecX, vecY) = np.where(matrix > -1000)
    np.random.seed(seedID % 100)
    randPermut = np.random.permutation(numAll)  
    np.random.seed(seedID)
    randSequence = np.random.normal(0, numAll / 6.0, numAll * 10)

    trainSet = []
    flags = np.zeros(numAll)
    for i in xrange(randSequence.shape[0]):
        sample = int(abs(randSequence[i]))
        if sample < numAll:
            idx = randPermut[sample]
            if flags[idx] == 0 and matrix[vecX[idx], vecY[idx]] > 0:
                trainSet.append(idx)
                flags[idx] = 1
        if len(trainSet) == numTrain:
            break
    if len(trainSet) < numTrain:
        logger.critical('Exit unexpectedly: not enough data for density = %.2f.', density)
        sys.exit()

    trainMatrix = np.zeros(matrix.shape)
    trainMatrix[vecX[trainSet], vecY[trainSet]] = matrix[vecX[trainSet], vecY[trainSet]]
    testMatrix = np.zeros(matrix.shape)
    testMatrix[matrix > 0] = matrix[matrix > 0]
    testMatrix[vecX[trainSet], vecY[trainSet]] = 0

    # ignore invalid testing users or services             
    idxX = (np.sum(trainMatrix, axis=1) == 0)
    testMatrix[idxX, :] = 0
    idxY = (np.sum(trainMatrix, axis=0) == 0)
    testMatrix[:, idxY] = 0    
    return trainMatrix, testMatrix


#======================================================#
# Function to compute the evaluation metrics
#======================================================#
def errMetric(realVec, predVec, metrics):
    result = []
    absError = np.abs(predVec - realVec) 
    mae = np.sum(absError)/absError.shape
    for metric in metrics:
        if 'MAE' == metric:
            result = np.append(result, mae)
        if 'NMAE' == metric:
            nmae = mae / (np.sum(realVec) / absError.shape)
            result = np.append(result, nmae)
        if 'RMSE' == metric:
            rmse = LA.norm(absError) / np.sqrt(absError.shape)
            result = np.append(result, rmse)
        if 'MRE' == metric or 'NPRE' == metric:
            relativeError = absError / realVec
            relativeError = np.sort(relativeError)
            if 'MRE' == metric:
                mre = np.median(relativeError)
                result = np.append(result, mre)
            if 'NPRE' == metric:
                npre = relativeError[np.floor(0.9 * relativeError.shape[0])] 
                result = np.append(result, npre)
    return result


#======================================================#
# Dump the raw result into tmp file
#======================================================#
def dumpresult(outFile, result):
    try:
        with open(outFile, 'wb') as fid:
                pickle.dump(result, fid)
    except Exception, e:
        logger.error('Dump file failed: ' + outFile)
        logger.error(e)
        sys.exit()


#======================================================#
# Process the raw result files 
#======================================================#
def summarizeResult(para, numTimeSlice):
    path = '%s%s_%s_result'%(para['outPath'], para['dataName'], para['dataType'])
    evalResults = np.zeros((len(para['density']), para['rounds'], len(para['metrics']), numTimeSlice)) 
    timeResults = np.zeros((len(para['density']), para['rounds'], numTimeSlice))   

    k = 0
    for den in para['density']:
        for rnd in xrange(para['rounds']):
            for tid in xrange(numTimeSlice):
                inputfile = path + '_%02d_%.2f_round%02d.tmp'%(tid + 1, den, rnd + 1)
                with open(inputfile, 'rb') as fid:
                    data = pickle.load(fid)
                os.remove(inputfile)
                (evalResults[k, rnd, :, tid], timeResults[k, rnd, tid]) = data
        k += 1
    saveSummaryResult(path, evalResults, timeResults, para)  


#======================================================#
# Save the summary evaluation results into file
#======================================================#
def saveSummaryResult(outfile, result, timeinfo, para):
    fileID = open(outfile + '.txt', 'w')
    print ('Average result: [%s]'%outfile)
    print 'Metrics:', para['metrics'] 
    fileID.write('======== Results summary ========\n')
    fileID.write('Metrics:    ')
    for metric in para['metrics']:
        fileID.write('|   %s  '%metric)
    fileID.write('\n')
    fileID.write('[Average]\n')
    
    k = 0
    for den in para['density']:
        den_result = result[k, :, :, :]
        evalResults = np.average(den_result, axis=2)
        fileID.write('density=%.2f: '%den)
        avgResult = np.average(evalResults, axis=0)
        np.savetxt(fileID, np.matrix(avgResult), fmt='%.4f', delimiter='  ')
        print 'density=%.2f: '%den, avgResult
        k += 1

    fileID.write('\n[Standard deviation (std)]\n')
    k = 0
    for den in para['density']:
        den_result = result[k, :, :, :]
        evalResults = np.average(den_result, axis=2)
        fileID.write('density=%.2f: '%den)
        np.savetxt(fileID, np.matrix(np.std(evalResults, axis=0)), fmt='%.4f', delimiter='  ')
        k += 1

    fileID.write('\n======== Detailed results ========\n')
    k = 0
    for den in para['density']:
        den_result = result[k, :, :, :]
        fileID.write('[density=%.2f, %2d rounds]\n'%(den, para['rounds']))
        np.savetxt(fileID, np.matrix(np.average(den_result, axis=2)), fmt='%.4f', delimiter='  ')
        fileID.write('\n')
        k += 1
    k = 0
    for den in para['density']:
        den_result = result[k, :, :, :]
        fileID.write('[density=%.2f, %2d slices]\n'%(den, result.shape[3]))
        np.savetxt(fileID, np.matrix(np.average(den_result, axis=0).T), fmt='%.4f', delimiter='  ')
        fileID.write('\n')
        k += 1
    fileID.close()

    if para['saveTimeInfo']:
        fileID = open(outfile + '_time.txt', 'w')
        fileID.write('======== Summary ========\n')
        fileID.write('Average running time (second):\n')
        k = 0
        for den in para['density']:
            den_time = timeinfo[k, :, :]
            timeResults = np.average(den_time, axis=1)
            fileID.write('density=%.2f: '%den)
            np.savetxt(fileID, np.matrix(np.average(timeResults)), fmt='%.4f', delimiter='  ')
            k += 1
        
        fileID.write('\n======== Details ========\n')
        k = 0
        for den in para['density']:
            den_time = timeinfo[k, :, :]
            fileID.write('[density=%.2f]\n'%den)
            np.savetxt(fileID, np.matrix(np.average(den_time, axis=0)).T, fmt='%.4f', delimiter='  ')
            fileID.write('\n')
            k += 1

        fileID.close()


#======================================================#
# Compute the reflection of boxcox() function
#======================================================#
def argBoxcox(y, alpha):
    if alpha != 0:
        x = (alpha * y + 1) ** (1 / alpha)
    else:
        x = np.exp(y)
    return x

