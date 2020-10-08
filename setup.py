from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Find Maxima",
    install_requires=['numpy', 'cython'>=0.29],
    ext_modules=cythonize("findmaxima/cy_findmaxima.pyx"),
    zip_safe=False,
)