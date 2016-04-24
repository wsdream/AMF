****************************************************************************
* README file 
* Author: Jamie Zhu <jimzhu@GitHub>
* Last updated: 2016/04/23           
****************************************************************************

This directory maintains the testing code used to benchmark the AMF package.
The code can be also used to reproduce the results in our work [Zhu et al.,
ICDCS'14].

****************************************************************************
Contents of this directory
****************************************************************************

benchmarks/
  - readme.txt       - descriptions of this directory 
  - run_rt.py        - script file for testing AMF on response-time QoS data
  - run_tp.py        - script file for testing AMF on throughput QoS data
  - commons/
    - dataloader.py  - a function to load the dataset with preprocessing
    - evalib.py      - common lib functions used by evaluator.py 
    - evaluator.py   - the main process to control the evaluations on AMF
    - utils.py       - a bag of utilities
    - __init__.py    - a file used to load the source files under commons/ 
  - results/
    - dataset#2_rt_result.txt  - evaluation results on response-time QoS data
    - dataset#2_tp_result.txt  - evaluation results on throughput QoS data

Note that the experimental results are provided with the metrics (MAE, MRE, 
NPRE). Each experiment is run for 20 times and the average result (including
std value) is reported. 

****************************************************************************
Reference and citation
****************************************************************************

Please refer to the following paper for the detailed description of the 
implemented algorithm:

- Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "Towards Online, 
  Accurate, and Scalable QoS Prediction for Runtime Service Adaptation," in 
  Proc. of IEEE ICDCS, 2014, pp. 318-327. 

IF YOU USE THIS PACKAGE IN PUBLISHED RESEARCH, PLEASE CITE THE ABOVE PAPER. 
THANKS!

****************************************************************************
License
****************************************************************************

The MIT License (MIT)
Copyright (c) 2016, WS-DREAM, CUHK


