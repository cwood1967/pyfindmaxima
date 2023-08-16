import numpy as np
from .cy_findmaxima import findmaxima as findmx

def findmaxima(x, tol, napari_points=False):
    ''' Find local maxima in the image, similar to ImageJ Find Maxima.

    Parameters:
    x : np.array
        The single plane image
    tol : float
        The noise tolerance (or prominance) of the peaks
    napari_points : bool
        If True, return the points in the format required by napari
        [[y1, x1], [y2, x2], ...]
        
    Returns:
        yc : np.array
            The y coordinates of the maxima
        xc : np.array
            The x coordinates of the maxima
        
        If napari_points is True, returns a np.array of points in the format
        [[y1, x1], [y2, x2], ...]
    '''
    if len(x.shape) != 2:
        raise ValueError(
            f"Input image has {len(x.shape)} dimensions - must only have two dimensions"
        )
    x = x.astype(np.float32)
    pkimg, pklist = findmx(x, tol)
    
    xc = pklist % x.shape[-1]
    yc = pklist // x.shape[-1]
    
    if napari_points:
        points_list = list()
        for j, i in zip(yc, xc):
            points_list.append([j, i])
        return np.array(points_list)
            
    else: 
        return yc, xc

