##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np


##-----------------------------------------------------------------------------
##  Function intervals(archetype, psnr, c, d)
##-----------------------------------------------------------------------------
##  Description:
##      Divide the feature space into several intervals
##  
##  Input:
##      archetype   - The archetype.
##      psnr	    - A 2-D array with the PSNR values of each pixel block.
##      c, d	    - Pre-defined parameters.
##  
##  Output:
##      tbd.
##-----------------------------------------------------------------------------
def intervals(archetype, psnr, c, d):
    n = len(archetype)
    m = len(archetype[0])
    left = np.zeros((n, m), dtype=float)
    right = np.zeros((n, m), dtype=float)

    for y in range(n):
        for x in range(m):
            left[y, x] = archetype[y, x] - pow(2, (c/psnr[y, x])) * d 
            right[y, x] = archetype[y, x] + pow(2, (c/psnr[y, x])) * d 

    # Fake intervals