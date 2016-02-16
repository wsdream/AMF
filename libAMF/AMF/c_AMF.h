/********************************************************
 * AMF.h: header file of c_AMF.cpp
 * Author: Jamie Zhu <jimzhu@GitHub>
 * Created: 2014/5/6
 * Last updated: 2016/02/15
********************************************************/

#include <iostream>
#include <cstring>
using namespace std;


/* Perform the core approach of AMF */
void AMF(double *removedData, int numUser, int numService, int dim, double lmda, 
    int maxIter, double convergeThreshold, double eta, double beta, bool debugMode, 
    double *Udata, double *Sdata, double *predData);

/* Compute the loss value of AMF */
double loss(double **U, double **S, double **removedMatrix, double **predMatrix, double lmda, 
    int numUser, int numService, int dim);

/* Sigmoid function */
double sigmoid(long double x);

/* Compute the gradient of sigmoid function */
long double grad_sigmoid(long double x);

/* Compute predMatrix */
void getPredMatrix(bool flag, double **removedMatrix, double **U, double **S, int numUser, 
        int numService, int dim, double **predMatrix);

/* Transform a vector into a matrix */ 
double **vector2Matrix(double *vector, int row, int col);

/* Compute the dot product of two vectors */
long double dotProduct(double *vec1, double *vec2, int len);

/* Allocate memory for a 2D array */
double **createMatrix(int row, int col);

/* Free memory for a 2D array */ 
void delete2DMatrix(double **ptr); 

/* Copy matrix */
void copyMatrix(double **M1, double **M2, int row, int col);

/* Get current data/time, format is YYYY-MM-DD hh:mm:ss */
const string currentDateTime();
