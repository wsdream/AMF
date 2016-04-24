########################################################
# core.pyx
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2016/02/15
########################################################

import time
import numpy as np
cimport numpy as np # import C-API
from libcpp cimport bool


#########################################################
# Make declarations on functions from cpp file
#
cdef extern from "c_AMF.h":
    void AMF(double *removedData, int numUser, int numService, int dim, double lmda, 
        int maxIter, double convergeThreshold, double eta, double beta, bool debugMode, 
        double *Udata, double *Sdata, double *predData)
#########################################################


#########################################################
# Function to perform the prediction algorithm
# Wrap up the C++ implementation
#
def predict(removedMatrix, U, S, para):  
    cdef int numService = removedMatrix.shape[1] 
    cdef int numUser = removedMatrix.shape[0] 
    cdef int dim = para['dimension']
    cdef double lmda = para['lambda']
    cdef int maxIter = para['maxIter']
    cdef double convergeThreshold = para['convergeThreshold']
    cdef double eta = para['eta']
    cdef double beta = para['beta']
    cdef bool debugMode = para['debugMode']
    cdef np.ndarray[double, ndim=2, mode='c'] predMatrix = \
        np.zeros((numUser, numService), dtype=np.float64)

    # wrap up c_AMF.cpp
    AMF(
        <double *> (<np.ndarray[double, ndim=2, mode='c']> removedMatrix).data,
        numUser,
        numService,
        dim,
        lmda,
        maxIter,
        convergeThreshold,
        eta,
        beta,
        debugMode,
        <double *> (<np.ndarray[double, ndim=2, mode='c']> U).data,
        <double *> (<np.ndarray[double, ndim=2, mode='c']> S).data,
        <double *> predMatrix.data
        )

    return predMatrix
#########################################################




