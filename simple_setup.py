import os
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

#print(np.get_include())
# setup(
#     name="sumpyx",
#     ext_modules=cythonize("simple/sumpy_cy.pyx",
#                            include_path=[np.get_include(), "dgfdfdfd"]),
#     zip_safe=False,
# )

setup(
    name='sumpyx',
    ext_modules=cythonize(
        Extension(
            "simple.sumpy_cy",
            sources=["simple/sumpy_cy.pyx"],
            include_dirs=[np.get_include()]
        )
    ),
    install_requires=["numpy"],
    zip_safe=False,
)