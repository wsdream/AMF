% ***************************************************************
% run_tp.m: the scripts to run experiments on throughput data
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/5/5
% Implemented approach: AMF
% Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
% ***************************************************************


clc; close all; clear;

addpath('src');
logger('===============================');
logger('AMF: Adaptive Matrix Factorization.');
logger('===============================');

% ***************************************************************
% config area 
numUser = 142;
numService = 4500;
timeSlices = 64;
dataPath = '../data/processedData/tpData/tp';
outPath = 'result/';
density = 0.05 : 0.05 : 0.5; % matrix density
rounds = 20; % how many runs are performed at each matrix density
dimension = 10; % dimensionality of the latent factors
eta = 0.8; % learning rate
beta = 0.3; % weight
lambda = 0.0002; % regularization parameter
maxIter = 50; % the max iterations
debugMode = false; % whether to log some debugging info
% ***************************************************************

% --- set parameters of the approach
paraStruct = struct('rounds', rounds, 'dimension', dimension, 'eta', eta, 'beta', ...
    beta, 'lambda', lambda, 'maxIter', maxIter, 'debugMode', debugMode); 

% --- create result folder
if exist('result', 'dir') == 0
    system('mkdir result');
end

startTime = tic;  % start timing

% --- loop for each matrix density
for i = 1 : length(density)
    evalResults = zeros(rounds, 5, timeSlices);
    
    % --- loop for each round
    for j = 1 : rounds
        logger('----------------------------------------------');
        logger(sprintf('%d-round starts.', j));
        
        % --- loop for each time slice (64 slices in total)
        U0 = rand(numUser, dimension)';        
        S0 = rand(numService, dimension)';
        for k = 1 : timeSlices
            logger(sprintf('density %f, %d-round, time slice %d starts.', density(i), j, k));
            
            % --- load one data slice 
            filepath = sprintf('%sTimeSlot%02d.txt', dataPath, k);
            logger(sprintf('Load data: %s', filepath));
            
            % --- load the data matrix from .txt file
            fid = fopen(filepath, 'r');
            celldata = textscan(fid, '%f', 'Delimiter', '\t'); % textscan is faster than load function
            fclose(fid);
            dataMatrix = reshape(celldata{1}, numService, numUser);
            dataMatrix = dataMatrix';

            % --- data transformation
            normalDataMatrix = dataMatrix;
            transVector = normalDataMatrix(:);
            [transdat, alpha] = boxcox(transVector(transVector > 0));
            minValue = min(transdat);
            maxValue = max(transdat);
            normalDataMatrix(normalDataMatrix ~= -1) = ...
                boxcox(alpha, normalDataMatrix(normalDataMatrix ~= -1));
            normalDataMatrix(normalDataMatrix ~= -1) = ...
                (normalDataMatrix(normalDataMatrix ~= -1) - minValue) / (maxValue - minValue);

            % --- run for each slice under each density
            seed = j; % control the random seed for fair comparison
            [evalResults(j, :, k), U, S] = execute(dataMatrix, normalDataMatrix, U0, S0, ...
                alpha, minValue, maxValue, density(i), seed, paraStruct);
            
            % --- keep the U and S at each time slice as the initial solution of the next time slice
            U0 = U;
            S0 = S;
            
        end
        logger(sprintf('%d-round done. ', j));
        logger('----------------------------------------------');
    end
    
    for k = 1 : timeSlices
        outFile = sprintf('%s%02d_tpResult_%.2f.txt', outPath, k, density(i));
        saveResult(outFile, evalResults(:, :, k));
    end
      
    logger(sprintf('density = %.2f done.', density(i)));
    logger('===============================');
end

logger('===============================');
logger(sprintf('All done. Total running time: %f s', toc(startTime)));
logger('===============================');
rmpath('src');

 
