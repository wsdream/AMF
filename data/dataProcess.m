% ***************************************************************
% dataProcess.m: the scripts for data preprocessing
% Author: Jamie Zhu <jimzhu@GitHub>
% Created: 2013/9/20
% Last updated: 2014/6/13
% ***************************************************************


clc; clear; close all;
fprintf('Data processing...\n');

% --- create processedData folder
if exist('processedData', 'dir') == 0
    system('mkdir processedData');
    system('mkdir processedData/rtData');
    system('mkdir processedData/tpData');
end

% --- process rtData
rtData = load('rtData');
fprintf('Loading rtData done.\n');
rtMatrix =  -1 * ones(142, 4500, 64);
for i = 1 : size(rtData, 1)
    rt = rtData(i, 4);
    if rt == 0 || rt >= 19.9 % filter out the invalid values
        rt = -1;
    end
    rtMatrix(rtData(i, 1) + 1, rtData(i, 2) + 1, rtData(i, 3) + 1) = rt; % base-0 to base-1
end
clear rtData;

% --- save to 64 txt files
for i = 1 : 64
    dlmwrite(sprintf('processedData/rtData/rtTimeSlot%02d.txt', i), rtMatrix(:, : , i), 'delimiter', '\t', 'precision', '%.3f');
    fprintf('Writing rtTimeSlot%02d.txt done.\n', i);
end
clear rtMatrix;

% --- process tpData
tpData = load('tpData');
fprintf('Loading tpData done.\n');
tpMatrix =  -1 * ones(142, 4500, 64);
for i = 1 : size(tpData, 1)
    tp = tpData(i, 4);
    if tp == 0 % filter out the invalid values
        tp = -1;
    end
    tpMatrix(tpData(i, 1) + 1, tpData(i, 2) + 1, tpData(i, 3) + 1) = tp; % base-0 to base-1
end
clear tpData;

% --- save to 64 txt files
for i = 1 : 64
    dlmwrite(sprintf('processedData/tpData/tpTimeSlot%02d.txt', i), tpMatrix(:, : , i), 'delimiter', '\t', 'precision', '%.3f');
    fprintf('Writing tpTimeSlot%02d.txt done.\n', i);
end
clear tpMatrix;
fprintf('All done.\n');


