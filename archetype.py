##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np
from math import ceil

##-----------------------------------------------------------------------------
##  Function archetype(norm_iris, x, y)
##-----------------------------------------------------------------------------
##  Description:
##      Generate the archetype:
##      - divide the normalized iris image in pixel blocks
##      - for each block, calculate the mean of all the pixel values in it
##  
##  Input:
##      norm_iris       - The normalized iris image.
##      x	            - x-dimension of a pixel block.
##      y	            - y-dimension of a pixel block.
##  
##  Output:
##      arc             - The archetype
##-----------------------------------------------------------------------------
def archetype(norm_iris, x, y):

    row = len(norm_iris)//y
    col = len(norm_iris[0])//x

    # Split the normalized iris image in x*y pixel blocks
    norm_iris_split = pixel_blocks(norm_iris, x, y)
    
    # Generate the archetype
    arc = np.zeros((row, col), dtype=float)
    z = 0
    
    for i in range(row):
        for j in range(col):
            arc[i][j] = np.mean(norm_iris_split[z])
            z += 1
    
    return arc


##-----------------------------------------------------------------------------
##  Function pixel_blocks(norm_iris, x, y)
##-----------------------------------------------------------------------------
##  Description:
##      Split the normalized iris image in x*y pixel blocks.
##  
##  Input:
##      norm_iris       - The normalized iris image.
##      x	            - x-dimension of a pixel block.
##      y	            - y-dimension of a pixel block.
##  
##  Output:
##      norm_iris_split	- The normalized iris image split in x*y pixel blocks
##-----------------------------------------------------------------------------
def pixel_blocks(norm_iris, x, y):
    row = len(norm_iris)
    col = len(norm_iris[0])

    norm_iris_array = np.array(norm_iris)

    # Split the normalized iris image in x*y pixel blocks
    # Source: https://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays

#    norm_iris_split = np.array_split(norm_iris_array, ceil(col/y), axis=1)
#    for i in range(len(norm_iris_split)):
#        norm_iris_split[i] = np.array_split(norm_iris_split[i], row/x, axis=0)

    return (norm_iris_array.reshape(row//y, y, -1, x).swapaxes(1,2).reshape(-1, y, x))
