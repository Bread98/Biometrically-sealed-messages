##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey

import numpy as np

from pre_processing_classic.segment import segment
from pre_processing_classic.normalize import normalize

from quantization_scheme.archetype import archetype
from quantization_scheme.intervals import apply_bitmask

from bisect import bisect

from math import floor

import hashlib

##-----------------------------------------------------------------------------
##  Function authentication(img_name, hash, bit_mask, intervals, n_bits)
##-----------------------------------------------------------------------------
##  Description:
##      Authenticate a user and re-generate the private key
##  
##  Input:
##      img_name        - The name of the eye image file
##      hash            - The hash of the private key
##      mask            - A 2D bit-mask pointing to the most reliable features
##      interval        - An array of points, representing the intervals
##      n_bits          - Number of bits used to encode an interval
##  
##  Output:
##      key_formatted   - The user's private key
##      "Try again!"    - Default output if the key is not correctly re-generated
##-----------------------------------------------------------------------------
def authentication(img_name, hash, bit_mask, intervals, n_bits):

    # Parameters for segmentation
    eyelashes_thres = 80
    use_multiprocess = False

    # Pixel-block dimention
    block_x = 8
    block_y = 4

    # Read the images
    img = imread(img_name, 0)

    # Identify the iris and the pupil
    ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

    #imshow("A_noisyeye", img_with_noise)
    #waitKey(0)

    # Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
    polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], 
                                        ciriris[2], cirpupil[1], cirpupil[0], 
                                        cirpupil[2], 64, 256)

    #imshow("A_polar", polar_array/255)
    #waitKey(0)

    # Create the archtype
    arc = archetype(polar_array, block_x, block_y)

    #imshow("A_Archetype", arc/255)
    #waitKey(0)

    # Apply the bitmask to extract the most reliable features
    features = apply_bitmask(arc, bit_mask)

    key = ""
    format_bits = "{0:0" + str(n_bits) + "b}"

    for i in range(len(features)):

        x, y = intervals[i]

        # Find the x-values such that x1 <= features[i] <= x2
        index = bisect(x, features[i])

        if index == 0:
            toAdd = format_bits.format(abs(y[index]-1))
        elif index == len(x):
            toAdd = format_bits.format(abs(y[index-1]-1))
        else: 
            x1 = x[index-1]
            x2 = x[index]

            if features[i] == x1:
                toAdd = format_bits.format(y[index-1]-1)
            elif features[i] == x2:
                toAdd = format_bits.format(y[index]-1)
            else:
                # Linear interpolation
                y_feature = y[index-1] + (features[i] - x[index-1]) * ((y[index] - y[index-1]) / (x[index] - x[index-1]))
                y_feature = floor(abs(y_feature))

                toAdd = format_bits.format(y_feature)
        
        key += toAdd

    # Verify the correctness of the key
    if hashlib.sha384(key.encode()).hexdigest() == hash:
        key_formatted = int(key, 2)
        return key_formatted
    else:
        return "Wrong user!"