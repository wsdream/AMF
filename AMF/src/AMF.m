% ***************************************************************
% AMF.m
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/5/5
% ***************************************************************


% ***************************************************************
function [U, S] = AMF( removedMatrix, U0, S0, paraStruct )

    % --- get the parameters
    d = paraStruct.dimension;                 % dimensionality 
    eta = paraStruct.eta;                         % learning rate eta
    maxIter = paraStruct.maxIter;                 % max iteration rounds
    lambda = paraStruct.lambda;
    beta = paraStruct.beta;

    numService = size(removedMatrix, 2);            %number of services
    numUser = size(removedMatrix, 1);                %number of users

    % --- transform the data samples into triplets
    [idxU, idxS] = find(removedMatrix > 0);
    dataTriples = [idxU, idxS, removedMatrix(removedMatrix > 0)];  

    % --- initialization
    U = U0;        
    S = S0;
    gradU = zeros(numUser, d)';
    gradS = zeros(numService, d)';
    eu = ones(numUser, 1);
    es = ones(numService, 1);
      
    iter = 1;  
    % --- loop for updates
    while iter <= maxIter    
        randDataTriples = dataTriples(randperm(size(dataTriples, 1)), :);      % randomly permutate the data samples
        for dataID = 1:length(randDataTriples)
            % --- get one data sample
            i = randDataTriples(dataID, 1);
            j = randDataTriples(dataID, 2);
            Rij = randDataTriples(dataID, 3);
            
            % --- confidence update
            eij = abs(sigmoid(U(:, i)' * S(:, j)) - Rij) / Rij;
            wi = eu(i) / (eu(i) + es(j));
            wj = es(j) / (eu(i) + es(j));
            
            eu(i) = beta * wi * eij + (1 - beta * wi) * eu(i);
            es(j) = beta * wj * eij + (1 - beta * wj) * es(j);
                       
            % --- gradient descent update 
            gradU(:, i) =  wi * (((sigmoid(U(:, i)' * S(:, j)) - Rij).*gradSigmoid(U(:, i)' * S(:, j))) ./ (Rij.^2))' * S(:, j) + lambda * U(:, i);
            gradS(:, j) = wj * (((sigmoid(U(:, i)' * S(:, j)) - Rij).*gradSigmoid(U(:, i)' * S(:, j))) ./ (Rij.^2)) * U(:, i) + lambda * S(:, j);
            U(:, i) = U(:, i) - eta * gradU(:, i);
            S(:, j) = S(:, j) - eta * gradS(:, j);
        end
        iter = iter + 1;
    end
    
    logger(sprintf('convergence after %d iterations.', iter));   
end
% ***************************************************************


% ***************************************************************
% Function to compute the loss value 
%
function lossValue = loss( U, S, removedMatrix, paramStruct )
    lambda = paramStruct.lambda; % regularization parameter
    I = zeros(size(removedMatrix));
    I(removedMatrix ~= 0) = 1;
    lossValue = 0.5 * (sum(sum(I.*(((removedMatrix - sigmoid(U'*S)) ./ (removedMatrix + eps)).^2))) ...
        + lambda * sum(sum(U.^2)) + lambda * sum(sum(S.^2)));
    logger(sprintf('cost = %f, regularization = %f', 0.5 * (sum(sum(I.*(((removedMatrix - sigmoid(U'*S)) ./ (removedMatrix + eps)).^2)))), ... 
        0.5 * (lambda * sum(sum(U.^2)) + lambda * sum(sum(S.^2)))), paramStruct.debugMode);
end
% ***************************************************************


% ***************************************************************
function g = sigmoid( x )
    % logistic function g(x)
    g = 1./ (1 + exp(-x));

end
% ***************************************************************


% ***************************************************************
function g_prime = gradSigmoid( x )
    % gradients of logistic function g(x)
    g_prime = 1./ (2 + exp(-x) + exp(x));

end
% ***************************************************************






