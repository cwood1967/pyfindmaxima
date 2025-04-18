import numpy as np
from .cy_findmaxima import findmaxima as findmx

def findmaxima(x, tol):
    if len(x.shape) != 2:
        raise ValueError(
            f"Input image has {len(x.shape)} dimensions - must only have two dimensions"
        )
    x = x.astype(np.float32)
    pkimg, pklist = findmx(x, tol)
    
    xc = pklist % x.shape[-1]
    yc = pklist // x.shape[-1]
    
    return yc, xc

