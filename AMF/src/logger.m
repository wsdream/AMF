% ***************************************************************
% logger.m
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/5/5
% ***************************************************************


% ***************************************************************
function [] = logger( logMessage, debugMode )
    % log the runtime information for behaviour monitoring    
    if nargin < 2
        debugMode = true;
    end

    if debugMode == true
        time = now;
        timeStr = datestr(time, 31);
        fprintf('%s: %s\n', timeStr, logMessage);    
    end
end
% ***************************************************************

