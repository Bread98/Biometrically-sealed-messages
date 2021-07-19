##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np
from math import log10


##-----------------------------------------------------------------------------
##  Function bit_mask(norm_iris_split1, n_features, norm_iris_split)
##-----------------------------------------------------------------------------
##  Description:
##      Calculate the peak signal-to-noise ratio (PSNR) for each pixel block
##      Generate a 2-D bit mask that points at the most reliable features
##  
##  Input:
##      norm_iris_split1 - The first iris image, normalized and split in pixel blocks.
##      n_features	     - The number of features to be selected.
##      norm_iris_split	 - The acquired iris images (except the first), normalized and split in pixel blocks.
##  
##  Output:
##      bit_mask	     - The 2-D bit mask.
##      psnr_mean	     - A 2-D array with the PSNR values of each pixel block.
##-----------------------------------------------------------------------------
def bit_mask(archetype, n_features, norm_iris_split):
    
    n = len(archetype)
    m = len(archetype[0])
    maxI = np.zeros(len(norm_iris_split), dtype=float)   # maximum pixel value
    maxI1 = np.amax(archetype)   # maximum pixel value of the first iris image acquired
    niris = 0   # iris in 'norm_iris_split' currently being processed
    psnr = np.zeros((n,m), dtype=float)

    # For each iris texture Ii calculate:
    # - the mean squared error between each pixel block of I1 and Ii (MSE) 
    # - the maximum pixel value of both images (maxI) 
    # and use them to calculate the peak signal-to-noise ratio for each pixel block and each image (PSNR)
    for iris in norm_iris_split:
        n_block = 0

        maxI[niris] = max(maxI1, np.amax(iris))
 
        for y in range(n):
            for x in range(m):
                mse = ((np.linalg.norm(archetype[y,x] - iris[n_block]))**2) / (n*m)
                psnr[y, x] = 10 * log10((maxI[niris]**2)/mse)

                n_block += 1

        niris += 1
    
    # For each pixel block calculate the mean of the PSNR values
    psnr_mean = np.zeros((n,m), dtype=float) 

    for y in range(n):
        for x in range(m):
            psnr_mean[y, x] = np.mean(psnr[y, x])


    # For each pixel block calculate a PSNR value as mean of the PSNR values of the 8 adjacent pixel blocks
    psnr_adjacent = np.zeros((n,m), dtype=float) 

    for y in range(1, n-1):
        for x in range(1, m-1):
            psnr_adjacent[y, x] = np.mean([psnr_mean[y-1, x-1], psnr_mean[y, x-1], psnr_mean[y+1, x-1], psnr_mean[y-1, x], psnr_mean[y+1, x], psnr_mean[y-1, x+1], psnr_mean[y, x+1], psnr_mean[y+1, x+1]])

    # Create a bit mask by selecting the blocks with high PSNR and surrounded by blocks with high PSNR       
    bit_mask = np.zeros((n,m), dtype=bool)
    candidates = np.zeros((n,m), dtype=int)
    mean1 = np.mean(psnr_mean[y, x])
    mean2 = np.mean(psnr_adjacent[y, x])

    for y in range(n):
        for x in range(m):
            if(psnr_mean[y, x] >= mean1 and psnr_adjacent[y, x] >= mean2):
                candidates[y, x] = 3
                bit_mask[y,x] = True
            elif(psnr_mean[y, x] >= mean1):
                candidates[y, x] = 2
            elif(psnr_adjacent[y, x] >= mean2):
                candidates[y, x] = 1

    tmp = np.where(bit_mask == True)
    l = len(tmp[0])

    if l < n_features:
        rows2, cols2 = np.where(candidates == 2)
        rows1, cols1 = np.where(candidates == 1)
        rows0, cols0 = np.where(candidates == 0)
        i = j = z = 0

        while l < n_features:
            if i < len(rows2):
                bit_mask[rows2[i], cols2[i]] = True
                i += 1
            elif j < len(rows1):
                bit_mask[rows1[j], cols1[j]] = True
                j += 1
            else:
                bit_mask[rows0[z], cols0[z]] = True
                z += 1
        
            l += 1
    elif l > n_features:
        rows3, cols3 = np.where(candidates == 3)
        i = 0

        while l > n_features:
            bit_mask[rows3[i], cols3[i]] = False
            i += 1
            l -= 1
    
    return bit_mask, psnr_mean