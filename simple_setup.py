import os
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

setup(
    name="Find Maxima",
    ext_modules=cythonize("simple/sumpy_cy.pyx"),
    zip_safe=False,
)
# setup(
#     name='sumpyx',
#     ext_modules=cythonize(
#         Extension(
#             "simple.sumpy_cy",
#             sources=["simple/sumpy_cy.pyx"],
#             include_dirs=[np.get_include()]
#         )
#     ),
#     install_requires=["numpy"],
#     zip_safe=False,
# )