########################################################
# dataloader.py
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2015/8/29
########################################################

import numpy as np 
from utils import logger
import os


#======================================================#
# Function to load the dataset
#======================================================#
def load(para):
    if para['dataName'] == 'dataset#1':
        datafile = para['dataPath'] + para['dataName'] + '/' + para['dataType'] + 'Matrix.txt'
        logger.info('Loading data: %s'%os.path.abspath(datafile))
        logger.info('Loading data: %s'%os.path.abspath(datafile))
        dataMatrix = np.loadtxt(datafile)
        logger.info('Data size: %d users * %d services'\
            %(dataMatrix.shape[0], dataMatrix.shape[1]))
    elif para['dataName'] == 'dataset#2':
        datafile = para['dataPath'] + para['dataName'] + '/' + para['dataType'] + 'data.txt'
        logger.info('Loading data: %s'%os.path.abspath(datafile))
        dataMatrix = -1 * np.ones((142, 4500, 64))
        fid = open(datafile, 'r')
        for line in fid:
            data = line.split(' ')
            rt = float(data[3])
            if rt > 0:
                dataMatrix[int(data[0]), int(data[1]), int(data[2])] = rt
        fid.close()
        logger.info('Data size: %d users * %d services * %d timeslices'\
            %(dataMatrix.shape[0], dataMatrix.shape[1], dataMatrix.shape[2]))      
    dataMatrix = preprocess(dataMatrix, para)
    logger.info('Loading data done.')
    logger.info('----------------------------------------------') 
    return dataMatrix


#======================================================#
# Function to preprocess the dataset which
# deletes the invalid values
#======================================================#
def preprocess(matrix, para):
    if para['dataType'] == 'rt':
        matrix = np.where(matrix == 0, -1, matrix)
        matrix = np.where(matrix >= 19.9, -1, matrix)
    elif para['dataType'] == 'tp':
        matrix = np.where(matrix == 0, -1, matrix)
    return matrix
