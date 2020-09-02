# %%
import autoreload
%load_ext autoreload
%autoreload 2

import sys
# sys.path.append('/Users/cjw/Code/simrutils')
from simr_io.nd2read import nikonImage
import tifffile
import numpy as np
from matplotlib import pyplot as plt
import findmaxima
import time
# %%
def runtest():
    filename = "/Users/cjw/Desktop/Mitosis/nd2/Top1-SC2--GapR-Nhp2-006.nd2"
    nd2 = nikonImage(filename)
    return nd2()
    

# %%
x = runtest()
# %%
tol = 300
w = 1024
x0 = 256
y0 = 256
sz = x[9, 1] #, y0:y0+w, x0:x0+w]
t1 = time.time()
mx = findmaxima.MaximumFinder(sz, tol)
mx.all_local_max()
res, plst = mx.findmax()
print(time.time() - t1)

# %%
len(mx.sorted_p), mx.img.max()
# %%
t1 = time.time()
print(time.time() - t1)
for i, p in enumerate(plst):
    xi = p % mx.w
    yi = p // mx.w
    print("{:4} {:6}  {:6} {:8}".format(i, xi, yi, mx.img[yi, xi]))
#print(len(res[1]))

# %%
plt.figure(figsize=(12,12))
plt.imshow(res.reshape(mx.h, mx.w) ==8, cmap='gray' )
res.max()
# %%
np.where(res > 0)
# %%
mx.tol
# %%
for p  in mx.sorted_p:
    print(p, mx.img.reshape((-1))[p], p // mx.w, p % mx.w)
# %%
num = 0
for k, v in z:
    print(k, v)
    num += 1
    if num > 20:break
# %%
from skimage.measure import block_reduce

plt.imshow(block_reduce(x[8,1,...], (4,4), np.max))
# %%
br = block_reduce(x[8, 1, ...], (4,4), np.max)
# %%
br.shape
# %%
