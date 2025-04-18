import numpy as np
import tifffile
import pandas as pd
import time

from findmaxima.findmaxima import findmaxima

def test_findmax():
    image = tifffile.imread("findmaxima/_tests/Images/test_image.tif")
    tol = 800
    yc, xc = findmaxima(image, tol)
    assert len(yc) == 4
    assert len(xc) == 4
    
    df = pd.read_csv("findmaxima/_tests/Images/test_results.csv")
    
    for row in df.itertuples():
        i = row.peak
        x = xc[i]
        y = yc[i]
        assert x == row.xm
        assert y == row.ym
        
        assert image[y, x] == row.mean

if __name__ == '__main__':
    test_findmax()