from setuptools import setup

setup(
    name="Find Maxima",
    install_requires=['numpy', 'cython>=0.29'],
    from Cython.Build import cythonize
    ext_modules=cythonize("findmaxima/cy_findmaxima.pyx"),
    zip_safe=False,
)