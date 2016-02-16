----------------------------------------------------------------------------
README file for AMF
----------------------------------------------------------------------------

Author: Jamie Zhu <jimzhu@GitHub>
Last updated: 2015/4/30.

This package implements an online QoS prediction approach, adaptive matrix 
factorization (AMF) [Zhu et al., ICDCS'14].

The approach is implemented based on Matlab(8.3).

----------------------------------------------------------------------------
List of contents of package
----------------------------------------------------------------------------

AMF/
  - run_rt.m                  - script file for running the experiments on 
                                response-time QoS data 
  - run_tp.m                  - script file for running the experiments on 
                                throughput QoS data
  - readme.txt                - descriptions of this package 
  - src/                      - directory of the source files
      - logger.m              - a function to perform logging
      - saveResult.m          - a function to compute and save the average results
      - execute.m             - control execution and results collection of  
                                the specific algorithm
      - AMF.m                 - the core algorithm to perform AMF
  - scripts/
      - resultHandler.py      - a script file to compute the average values of 
                                the raw results in "result/"
  - result/                   - directory for storing evaluation results
                                available metrics: (MAE, NMAE, RMSE, MRE, NPRE)
      - 01_rtResult_0.05.txt  - E.g., the reponse-time prediction result with 
                                20 runs, performed for time slice = 01, under 
                                matrix density = 5%
      - [...]                 - many other results
	  - average/
          - avg_rtResult_0.05.txt  - the average result over 64 time slices
          - [...]                  - results for other densities
		  
----------------------------------------------------------------------------
Using the package
----------------------------------------------------------------------------

For ease of reproducing and compare with other approaches, we provide the 
detailed experimental results with five metrics (MAE, NMAE, RMSE, MRE, NPRE), 
under the "result/" directory, after running the above five QoS prediction 
approaches on "data/". E.g.,"result/average/avg_rtResult_0.05.txt" records the 
evaluation results under matrix density = 5%. In particular, each experiment 
under each time slice is run for 20 times and the average result (including 
std value) over 20*64 runs is reported. These results can be directly used 
for your research work.

On the other hand, if you want to reproduce our experiments, you can run the 
program with our provided Matlab scripts "run_rt.m" and "run_tp.m".

>> run_rt.m
>> run_tp.m

----------------------------------------------------------------------------
Reference paper
----------------------------------------------------------------------------

Please refer to the following papers for the detailed descriptions of the 
implemented algorithms:

- Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "Towards Online, 
  Accurate, and Scalable QoS Prediction for Runtime Service Adaptation," in 
  Proc. of IEEE ICDCS, 2014.

IF YOU USE THIS PACKAGE IN PUBLISHED RESEARCH, PLEASE CITE THE ABOVE PAPER. 
THANKS!

----------------------------------------------------------------------------
Issues
----------------------------------------------------------------------------

In case of questions or problems, please do not hesitate to report to our 
issue page (https://github.com/WS-DREAM/AMF/issues). We will help ASAP. 
In addition, we will appreciate any contribution to refine and optimize this 
package.

----------------------------------------------------------------------------
Copyright
----------------------------------------------------------------------------

Copyright (c) WS-DREAM@GitHub, CUHK.

Permission is granted for anyone to copy, use, modify, or distribute this 
program and accompanying programs and documents for any purpose, provided 
this copyright notice is retained and prominently displayed, along with a 
note saying that the original programs are available from our web page 
(https://wsdream.github.io). The program is provided as-is, and there are 
no guarantees that it fits your purposes or that it is bug-free. All use 
of these programs is entirely at the user's own risk. For any enquiries, 
please feel free to contact Jamie Zhu <jmzhu AT cse.cuhk.edu.hk>.

