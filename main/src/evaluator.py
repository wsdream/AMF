########################################################
# evaluator.py
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/11/14
########################################################

import numpy as np 
from numpy import linalg as LA
from scipy.stats import logistic
from scipy import stats
import cPickle as pickle
import time, sys
import random
import core
from utilities import *


########################################################
# Function to run the prediction approach at each density
# 
def execute(tensor, density, roundId, para):
    startTime = time.clock()
    (numUser, numService, numTime) = tensor.shape
    dim = para['dimension']
    logger.info('matrix density = %.2f, %d-round starts.'%(density, roundId + 1))
    logger.info('----------------------------------------------') 

    U = np.random.rand(numUser, dim)
    S = np.random.rand(numService, dim)

    # run for each time slice
    for sliceId in xrange(numTime):
        # boxcox data transform
        matrix = tensor[:, :, sliceId]
        dataVector = matrix[:]
        (transfVector, alpha) = stats.boxcox(dataVector[dataVector > 0])
        maxV = np.max(transfVector)
        minV = np.min(transfVector)

        transfMatrix = matrix.copy()
        transfMatrix[transfMatrix != -1] = stats.boxcox(transfMatrix[transfMatrix != -1], alpha)
        transfMatrix[transfMatrix != -1] = (transfMatrix[transfMatrix != -1] - minV) / (maxV - minV)

        # remove the entries of data matrix to generate trainMatrix and testMatrix  
        seedID = roundId + sliceId * 100
        (trainMatrix, testMatrix) = removeEntries(matrix, density, seedID)
        trainMatrix = np.where(trainMatrix > 0, transfMatrix, 0)

        (testVecX, testVecY) = np.where(testMatrix)     
        testVec = matrix[testVecX, testVecY]

        # invocation to the prediction function
        sliceStartTime = time.clock() # to record the running time for one slice            
        predictedMatrix = core.predict(trainMatrix, U, S, para)     
        timeResult = time.clock() - sliceStartTime

        # calculate the prediction error
        predVec = predictedMatrix[testVecX, testVecY]
        predVec = (maxV - minV) * predVec + minV
        predVec = argBoxcox(predVec, alpha)
        evalResult = errMetric(testVec, predVec, para['metrics'])

        # dump the intermediate result
        result = (evalResult, timeResult)
        outFile = '%s%02d_%sResult_%.2f.round%02d'\
            %(para['outPath'], sliceId + 1, para['dataType'], density, roundId + 1)
        with open(outFile, 'wb') as fid:
            pickle.dump(result, fid)
        logger.info('SliceId = %02d done.'%(sliceId + 1))

    logger.info('Matrix density = %.2f, %d-round done. Running time: %.2f sec'
            %(density, roundId + 1, time.clock() - startTime))
    logger.info('----------------------------------------------') 
########################################################


########################################################
# Function to remove the entries of data matrix
# Return the trainMatrix and the corresponding testing data
#
def removeEntries(matrix, density, seedID):
    (vecX, vecY) = np.where(matrix > 0)
    vecXY = np.c_[vecX, vecY]
    numRecords = vecX.size
    numAll = matrix.size
    random.seed(seedID)
    randomSequence = range(0, numRecords)
    random.shuffle(randomSequence) # one random sequence per round
    numTrain = int( numAll * density)
    # by default, we set the remaining QoS records as testing data                     
    numTest = numRecords - numTrain
    trainXY = vecXY[randomSequence[0 : numTrain], :]
    testXY = vecXY[randomSequence[- numTest :], :]

    trainMatrix = np.zeros(matrix.shape)
    trainMatrix[trainXY[:, 0], trainXY[:, 1]] = matrix[trainXY[:, 0], trainXY[:, 1]]
    testMatrix = np.zeros(matrix.shape)
    testMatrix[testXY[:, 0], testXY[:, 1]] = matrix[testXY[:, 0], testXY[:, 1]]

    # ignore invalid testing data
    idxX = (np.sum(trainMatrix, axis=1) == 0)
    testMatrix[idxX, :] = 0
    idxY = (np.sum(trainMatrix, axis=0) == 0)
    testMatrix[:, idxY] = 0    
    return trainMatrix, testMatrix
########################################################


########################################################
# Function to compute the evaluation metrics
#
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
########################################################


########################################################
# Function to compute the reflection of boxcox() function 
#
def argBoxcox(y, alpha):
    if alpha != 0:
        x = (alpha * y + 1) ** (1 / alpha)
    else:
        x = np.exp(y)
    return x
########################################################
