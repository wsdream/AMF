****************************************************************************
* README file 
* Author: Jamie Zhu <jimzhu@GitHub>
* Last updated: 2016/02/22           
****************************************************************************

This package implements an online QoS prediction approach, adaptive matrix 
factorization (AMF), presented in the work [Zhu et al., ICDCS'14].

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
Usage of this package
****************************************************************************

For ease of reproducing and compare with other approaches, we provide the 
detailed experimental results with the metrics (MAE, MRE, NPRE), under the
"result/" directory, after running the above QoS prediction approach on our
dataset. In particular, each experiment is run for 20 times and the average 
result (including std value) is reported. These results can be directly used 
for your research work.

On the other hand, if you want to reproduce our experiments, you need to:

1. Install the package "libAMF"

>> python setup.py install --user

2. Run our provided Python scripts "run_rt.py" and "run_tp.py". In particular,
you can turn on the "parallelMode" in the config area for speedup if you use 
a multi-core computer.

>> python run_rt.py
>> python run_tp.py

****************************************************************************
Copyright (c) WS-DREAM Team, CUHK
****************************************************************************


