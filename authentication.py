##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread

import numpy as np

from segment import segment
from normalize import normalize
from archetype import archetype
from intervals import apply_bitmask

from bisect import bisect

from math import floor

import hashlib

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def authentication(img_name, hash, bit_mask, intervals, n_bits):

    eyelashes_thres = 80
    use_multiprocess = False
    block_x = 8
    block_y = 4
    #n_features = 64
    #c = 15
    #d = 3.5

    # Read the images
    img = imread(img_name, 0)

    # Identify the iris and the pupil
    ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

    # Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
    polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], 
                                        ciriris[2], cirpupil[1], cirpupil[0], 
                                        cirpupil[2], 64, 256)

    # Create the archtype
    arc = archetype(polar_array, block_x, block_y)

    # Apply the bitmask to extract the most reliable features
    features = apply_bitmask(arc, bit_mask)

    key = ""
    format_bits = "{0:0" + str(n_bits) + "b}"

    for i in range(len(features)):

        x, y = intervals[i]

        # Find the x-values such that x1 <= features[i] <= x2
        index = bisect(x, features[i])
        x1 = x[index-1]
        x2 = x[index]

        if features[i] == x1:
            key += format_bits.format(y[index-1])
        elif features[i] == x2:
            key += format_bits.format(y[index])
        else:
            # Linear interpolation
            y_feature = y[index-1] + (features[i] - x[index-1]) * ((y[index] - y[index-1]) / (x[index] - x[index-1]))
            y_feature = floor(abs(y_feature))

            key += format_bits.format(y_feature)

    if hashlib.sha384(key.encode()).hexdigest() == hash:
        key_formatted = int(key, 2)
        return key_formatted
    else:
        return "Try again!"