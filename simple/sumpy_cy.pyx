import numpy as np
cimport cython

def sum(double[::1] x):
    cdef double s = 0.0
    cdef Py_ssize_t i

    for i in range(len(x)):
        s += x[i]*x[i]
        
    return np.sqrt(s)
