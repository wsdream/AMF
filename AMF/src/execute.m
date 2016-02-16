% ***************************************************************
% predict.m
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/5/5
% ***************************************************************


% ***************************************************************
% Function to make prediction by AMF at each density for serveral rounds
%
function [evalResult, U, S] = execute(matrix, normalMatrix, U0, S0, alpha, minValue, ...
    maxValue, density, seed, paraStruct)
    
    [trainIdxMatrix, testIdxMatrix] = remove(matrix, density, seed);
    trainMatrix = normalMatrix .* trainIdxMatrix;
    
    % --- AMF updates
    [U, S] = AMF( trainMatrix, U0, S0, paraStruct ); 
        
    % --- calculate the prediction matrix
    predictedNormalMatrix = sigmoid(U' * S);
    
    % --- recover from data transformation
    predictedMatrix = predictedNormalMatrix;
    predictedMatrix = (maxValue - minValue) * predictedMatrix + minValue;
    predictedMatrix = argBoxcox(alpha, predictedMatrix);
        
    [testVec(:, 1), testVec(:, 2)] = find(testIdxMatrix);		
    realVec = matrix(sub2ind(size(matrix), testVec(:,1), testVec(:,2)));
    predVec = predictedMatrix(sub2ind(size(matrix), testVec(:,1), testVec(:,2)));

    % --- Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
    [MAE, NMAE, RMSE, MRE, NPRE] = errMetric(realVec, predVec);
    evalResult = [MAE, NMAE, RMSE, MRE, NPRE];
   
end
% ***************************************************************


% ***************************************************************
% Function to compute the evaluation metrics
%
function [mae, nmae, rmse, mre, npre] = errMetric(realVec, predVec)
    % --- get mae, nmae, rmse, mre, npre
    absError = abs(predVec - realVec);  
    mae = sum(absError)/length(absError);
    nmae = mae / (sum(realVec) / length(absError));
    rmse = sqrt(absError' * absError / length(absError));
    relativeError = absError ./ realVec;
    relativeError = sort(relativeError);
    mre = median(relativeError);
    npre = relativeError(floor(0.9*length(relativeError)));  
end
% ***************************************************************


% ***************************************************************
% Function to remove the entries of the input matrix with certain density
%
function [trainIdxMatrix, testIdxMatrix] = remove(matrix, density, seed)
        [rtVec(:, 1), rtVec(:, 2)] = find(matrix ~= -1);
        numRecords = size(rtVec, 1);
        numAll = numel(matrix);
        stream = RandStream('swb2712', 'Seed', seed);
        RandStream.setGlobalStream(stream); % rand seeds
		randomSequence = randperm(numRecords); % one random sequence per round
        
		numTrain = floor( numAll * density );               
	    numTest = numRecords - numTrain; % by default, we set the remaining QoS records as testing data
	
		trainVec = rtVec(randomSequence(1 : numTrain), :);
        testVec = rtVec(randomSequence(end - numTest + 1 : end), :);      
        trainIdxMatrix = zeros(size(matrix));
		trainIdxMatrix(sub2ind(size(trainIdxMatrix), trainVec(:, 1), trainVec(:, 2))) = 1;
        testIdxMatrix = zeros(size(matrix));
		testIdxMatrix(sub2ind(size(testIdxMatrix), testVec(:, 1), testVec(:, 2))) = 1;
        
        % ignore invalid testing data
        idxX = (sum(trainIdxMatrix, 2) == 0);
        testIdxMatrix(idxX, :) = 0;
        idxY = (sum(trainIdxMatrix, 1) == 0);
        testIdxMatrix(:, idxY) = 0;          
end
% ***************************************************************


% ***************************************************************
% Function to get the reflection of function boxcox(x)
%
function x = argBoxcox( alpha, y )
    if alpha ~= 0
        x = (alpha * y + 1) .^ (1 / alpha);
    else
        x = exp(y);
    end
end
% ***************************************************************


% ***************************************************************
% Function to get the logistic function g(x)
%
function g = sigmoid( x )
    g = 1./ (1 + exp(-x));
end
% ***************************************************************






