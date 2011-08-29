from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(cmdclass={'build_ext': build_ext},
#ext_modules = [Extension("ccross", ["ccross.pyx"]),Extension("ccross2", ["ccross2.pyx"])])
ext_modules = [Extension("cutils", ["cutils.pyx"])])
