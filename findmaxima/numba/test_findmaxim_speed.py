import sys
from simr_io.nd2read import nikonImage
import tifffile
import numpy as np
from matplotlib import pyplot as plt
import findmaxima
import time

def openimage():
    filename = "/Users/cjw/Desktop/Mitosis/nd2/Top1-SC2--GapR-Nhp2-006.nd2"
    nd2 = nikonImage(filename)
    return nd2()

x = openimage()
#tol = np.arange(100,1000,50)
sz = x[9, 1] #, 200:300, 200:300] #, y0:y0+w, x0:x0+w]
t1 = time.time()
mx = findmaxima.MaximumFinder()
res, plst = mx.run(sz, 400)
print(time.time() - t1, len(plst))
#del res
#del plst

tol = 400
tt =0
t0 = time.time()
pklist = list()
for i in range(x.shape[0]):
    t1 = time.time()
    mx = findmaxima.MaximumFinder() #x[i,1,:,:], tol)
    #mx.all_local_max()
    res, plst = mx.run(x[i,1,:,:], tol)
    t2 = time.time()
    print("{:6}  {:8.1f} {:6}".format(i,1000*(t2 - t1), len(plst)))
    pklist.append(plst.copy())
    del res
    del plst
  
print(time.time() - t0)
for i, p in enumerate(pklist[9]):
    xi = p % mx.w
    yi = p // mx.w
    print("{:4} {:6}  {:6} {:8}".format(i, xi, yi, x[9,1, yi, xi]))
    