
# %%
import numpy as np
import time
import math
from simple.sumpy_cy import sum as sumcy
# %%
def sum(x):
    s = 0
    for k in x:
        s += k*k
    return math.sqrt(s)


# %%
z = np.random.rand(50000000)
t0 = time.time()
z0sum = sum(z)
dt0 = time.time() - t0
print(z0sum, dt0)
# %%
t1 = time.time()

z2 = np.sqrt((z*z).sum())

dt1 = time.time() - t1
print(z1sum, dt1)
# %%

t2 = time.time()
z2sum = sumcy(z)
dt2 = time.time() - t2
print(z2sum, dt2)
# %%
