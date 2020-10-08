import os
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Find Maxima",
    ext_modules=cythonize("simple/sumpy_cy.pyx"),
    zip_safe=False,
)