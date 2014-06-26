% ***************************************************************
% saveResult.m
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/5/5
% ***************************************************************


% ***************************************************************
function [] = saveResult(outfile, result, dataType)
    % save the evaluation results into file
    fileID = fopen(outfile, 'wt');
    if nargin < 3
        fprintf(fileID, 'Metric:  MAE\t| NMAE\t| RMSE\t| MRE\t| NPRE\n');
    elseif (strcmp(dataType, 'time'))
        fprintf(fileID, 'Running time: 1 - 64 slices\n');  
    end
    avgResult = mean(result, 1);         
    fprintf(fileID, 'Avg:\t');
    fprintf(fileID, [repmat('%.4f\t', 1, size(avgResult, 2)) '\n'], avgResult');
    stdResult = std(result, 1, 1);
    fprintf(fileID, 'Std:\t');
    fprintf(fileID, [repmat('%.4f\t', 1, size(stdResult, 2)) '\n'], stdResult');
    fprintf(fileID, '\n==========================================\n');
    fprintf(fileID, 'Detailed results for %d rounds:\n', size(result, 1));   
    fprintf(fileID, [repmat('%.4f\t', 1, size(result, 2)) '\n'], result');    
    fclose(fileID);
end
% ***************************************************************
