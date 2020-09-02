from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Find Maxima",
    ext_modules=cythonize("findmaxima/cy_findmaxima.pyx"),
    zip_safe=False,
)