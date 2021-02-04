from setuptools import Extension, setup
import setuptools
from Cython.Build import cythonize

extensions = Extension("cy_findmaxima", ["findmaxima/cy_findmaxima.pyx"])
setup(
    name="pyfindmaxima",
    version="0.1.0.1",
    setup_requires=["cython", "numpy"],
    install_requires=['numpy'],
    ext_modules=cythonize(["findmaxima/cy_findmaxima.pyx"]),
    #ext_modules=cythonize(extensions),
    package_data = {'findmaxima':['*.pyx']},
    packages=setuptools.find_packages(),
    zip_safe=False,
)