import os
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

setup(
    name="Find Maxima",
    ext_modules=cythonize("simple/sumpy_cy.pyx"),
    zip_safe=False,
)