import os
from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

here = os.path.abspath(os.path.dirname(__file__))

extensions = Extension("cy_findmaxima", ["findmaxima/cy_findmaxima.pyx"])
setup(
    ext_modules=cythonize(["findmaxima/cy_findmaxima.pyx"]),
)

