import numpy as np
import tifffile
import time

from findmaxima.cy_findmaxima import all_local_max, findmaxima

tr = time.time()
x = tifffile.imread("findmaxima/Images/test_09_02.tif")
x = x.astype(np.float32)
t0 = time.time()
tol = 200
#res = all_local_max(x, tol)
pk, pklist = findmaxima(x, tol)
if 596732 in pklist:
    print("yes!")
else:
    print("no???")
#print(pklist)
print(len(pklist))

for i, p in enumerate(pklist):
    xi = p % x.shape[1]
    yi = p // x.shape[1]
    #if xi==778:
    print("{:4} {:6}  {:6} {:8}".format(i, xi, yi, x[yi, xi]))

tf = time.time()
print(tf - tr, tf - t0)