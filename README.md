##AMF

This repository maintains the implementation of an adaptive matrix factorization approach to online QoS prediction of cloud services.

Read more information from our papers: 

1. Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "**Online QoS Prediction for Runtime Service Adaptation via Adaptive Matrix Factorization**," *submitted to IEEE Transactions on Parallel and Distributed Systems (TPDS)*, 2016. [[Draft](http://xxx)]

2. Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "**Towards Online, Accurate, and Scalable QoS Prediction for Runtime Service Adaptation**," *in Proc. of the 34th IEEE International Conference on Distributed Computing Systems (ICDCS)*, 2014. [[Paper](http://jiemingzhu.github.io/pub/jmzhu_icdcs2014.pdf)]

###Dependencies
- Python 2.7 (https://www.python.org)
- Cython 0.20.1 (http://cython.org)
- numpy 1.8.1 (http://www.scipy.org)
- scipy 0.13.3 (http://www.scipy.org)

###Versions
The repo maintains three versions of AMF in different branches:
- [master](.): current optimized version in python
- [icdcs14-python](https://github.com/wsdream/AMF/tree/icdcs14-python): python-version code for ICDCS'2014 paper
- [icdcs14-matlab](https://github.com/wsdream/AMF/tree/icdcs14-matlab): matlab-version code for ICDCS'2014 paper


###Usage

The AMF algorithm is implemented in C++ and further wrapped up as a python package for common use.

1. Install `AMF` package
  
  Download the repo: `git clone https://github.com/wsdream/AMF.git`,
  then install the package `python setup.py install --user`.    

2. Change directory `cd` to `"benchmarks/"`, and configure the parameters in benchmark scripts
  
  For example, in `run_rt.py`, you can config the `'parallelMode': True` if you are running a multi-core machine. You can also set `'rounds': 1` for testing, which can make the execution finish soon.

3. Run the benchmark scripts
     
  ```    
    $ python run_rt.py
    $ python run_tp.py 
    ```
    
4. Check the evaluation results in `"benchmarks/result/"` directory. Note that the repository has maintained the results evaluated on [WS-DREAM datasets](https://github.com/wsdream/dataset), which are ready for immediate use.


###Feedback
For bugs and feedback, please post to [our issue page](https://github.com/wsdream/AMF/issues). For any other enquires, please drop an email to our team (wsdream.maillist@gmail.com).


###License
[The MIT License (MIT)](./LICENSE)

Copyright &copy; 2016, [WS-DREAM](https://wsdream.github.io), CUHK

