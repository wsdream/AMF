##AMF

This repository maintains the implementation of an adaptive matrix factorization approach to online QoS prediction of cloud services, which has been published in ICDCS'2014.

Read more information from our paper: 

>Jieming Zhu, Pinjia He, Zibin Zheng, and Michael R. Lyu, "**Towards Online, Accurate, and Scalable QoS Prediction for Runtime Service Adaptation**," *in Proc. of IEEE ICDCS*, 2014. [[Paper](http://jiemingzhu.github.io/pub/jmzhu_icdcs2014.pdf)][[Project page](http://wsdream.github.io/AMF)]


###Related Links

- [Publication list of Web service recommendation research](https://github.com/wsdream/WSRec/blob/master/paperlist.md)

- [WS-DREAM QoS datasets](https://github.com/wsdream/dataset)


###Dependencies
- Python 2.7 (https://www.python.org)
- Cython 0.20.1 (http://cython.org)
- numpy 1.8.1 (http://www.scipy.org)
- scipy 0.13.3 (http://www.scipy.org)

The benchmarks are implemented with a combination of Python and C++. The framework is built on Python for simplicity, and the core functions of each algorithm are written in C++ for efficiency consideration. To achieve so, [Cython](http://cython.org/ "Cython's Web page") (a language to write C/C++ extensions for Python) has been employed to compile the C++ extensions to Python-compatible modules. 

**Note**: Our code is directly executable on Linux platform. Re-compilation with Cython is required to execute them on Windows platform: See [how to run on Windows](https://github.com/wsdream/WSRec#usage).


###Feedback
For bugs and feedback, please post to [our issue page](https://github.com/wsdream/AMF/issues). For any other enquires, please drop an email to our team (wsdream.maillist@gmail.com).


###Copyright &copy; [WS-DREAM Team](http://wsdream.github.io), CUHK
Permission is granted for anyone to copy, use, modify, or distribute this program and accompanying programs and documents for any purpose, provided this copyright notice is retained and prominently displayed, along with a note saying that the original programs are available from our web page (https://wsdream.github.io). The program is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. All use of these programs is entirely at the user's own risk.

