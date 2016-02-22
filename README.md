##AMF

This repository maintains the benchmark of an adaptive matrix factorization approach to online QoS prediction of cloud services, which has been published in ICDCS'2014.

Read more information from our paper: 

>Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "**Towards Online, Accurate, and Scalable QoS Prediction for Runtime Service Adaptation**," *in Proc. of IEEE ICDCS*, 2014. [[Paper](http://jiemingzhu.github.io/pub/jmzhu_icdcs2014.pdf)][[Project page](http://wsdream.github.io/AMF)]


###Related Links

- [Publication list of Web service recommendation research](https://github.com/wsdream/pywsrec/blob/master/docs/paperlist.rst)

- [WS-DREAM QoS datasets](https://github.com/wsdream/dataset)


###Dependencies
- Python 2.7 (https://www.python.org)
- Cython 0.20.1 (http://cython.org)
- numpy 1.8.1 (http://www.scipy.org)
- scipy 0.13.3 (http://www.scipy.org)

###Usage

The benchmark is implemented as a Python package. For efficiency purpose, the core algorithm is written as Python extension using C++, and have been built into `libAMF` package for common use.

1. Install `libAMF` package
  
  Download the repo: `git clone https://github.com/wsdream/AMF.git`,

  Check out branch: `git checkout icdcs14-python`,

  Then install the package `python setup.py install --user`.    

2. Read `benchmarks/readme.txt`
3. Configure the parameters in benchmark script
  
  For example, in `run_rt.py`, you can config the `'parallelMode': True` if you are running a multi-core machine. You can also set `'rounds': 1` for testing, which make the execution finish soon.

3. Run the benchmark scripts
     
  ```    
    $ python run_rt.py
    $ python run_tp.py 
    ```
4. Check the evaluation results in "benchmarks/result/" directory. Note that the repository has maintained the results evaluated on [WS-DREAM datasets](https://github.com/wsdream/dataset), which are ready for immediate use.


###Feedback
For bugs and feedback, please post to [our issue page](https://github.com/wsdream/AMF/issues). For any other enquires, please drop an email to our team (wsdream.maillist@gmail.com).


###License
[The MIT License (MIT)](./LICENSE)

Copyright &copy; 2016, [WS-DREAM](https://wsdream.github.io), CUHK

