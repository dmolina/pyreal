pyreal
======

Implementation in Python of evolutionary algorithms, used to make an study
of the performance in Python using Cython. 
This code is GPLv3. 

You can read a post about that in http://dmolina.github.com/blog/2012/07/15/increasing-performance-python/, this is the 
source code used in this comparisons. 

Install
=======

To install, you need Python 2.6, [Boost::python] (http://www.boost.org/doc/libs/1_50_0/libs/python/doc/ "Boost::Python"), 
and [CMake] (http://cmake.org/ "CMake") to compile. 

The install process has several steps, but you can only run the ./compile script:

./compile

and everything should be compiled. 

Run
===

You can use the algorithm 

Python and Cython versions
==========================

By default, the algorithm uses the cython version. If you want to repeat the experiments
of the post, or you want to study the differences, these methods are implemented in
two modules:

- utils.py : performance critic methods using python. 
- cutils.py: performance critic method using cython. 

To set the the slow (utils.py) or fast (cutils.py) you only have to comment (or uncomment) 
one of the following lines:

   from cutils import getParentByNAM,crossBLX,getBestWorst #uncomment for fast version (cython)
   #from utils import getParentByNAM,crossBLX,getBestWorst #uncomment for slow version (python)
