from setuptools import setup
import setuptools
from Cython.Build import cythonize

setup(
    name="Find Maxima",
    install_requires=['numpy'],
    ext_modules=cythonize("findmaxima/cy_findmaxima.pyx"),
    packages=setuptools.find_packages(),
    zip_safe=False,
)