from setuptools import Extension, setup
import setuptools
from Cython.Build import cythonize

extensions = Extension("cy_findmaxima", ["findmaxima/cy_findmaxima.pyx"])
setup(
    name="pyfindmaxima",
    version="0.1.1.1",
    #setup_requires=["cython", "numpy"],
    #install_requires=['numpy'],
    ext_modules=cythonize(["findmaxima/cy_findmaxima.pyx"]),
    #ext_modules=cythonize(extensions),
    package_data = {'findmaxima':['*.pyx']},
    packages=setuptools.find_packages(),
    zip_safe=False,
    license="APACHE",
    #license_files=["LICENSE"],
    author="Chris Wood",
    url="https://github.com/cwood1967/pyfindmaxima",
    ##long_description="Find local maxima in a 2D image, similar to ImageJ Find Maxima."
)