##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from math import log2

import random

import secrets

##-----------------------------------------------------------------------------
##  Function intervals(archetype, psnr, c, d)
##-----------------------------------------------------------------------------
##  Description:
##      Divide the feature space into several intervals
##  
##  Input:
##      archetype   - The archetype created from the first image.
##      psnr	    - A 2-D array with the PSNR values of each pixel block.
##      c, d	    - Pre-defined parameters.
##  
##  Output:
##      key         - The cryptographic key generated
##      interval    - An array of points, representing the intervals
##      n_bits      - Number of bits used to encode an interval
##-----------------------------------------------------------------------------
def intervals(archetype, bit_mask, psnr, c, d):
    key = ""
    interval = []

    # Apply the bitmask to extract the most reliable features and their psnr
    features_main = apply_bitmask(archetype, bit_mask)
    features_psnr = apply_bitmask(psnr, bit_mask)

    # Generate the intervals
    n = len(features_main)
    left = np.zeros(n, dtype=float)
    right = np.zeros(n, dtype=float)

    for i in range(n):
        left[i] = features_main[i] - pow(2, (c/features_psnr[i])) * d 
        right[i] = features_main[i] + pow(2, (c/features_psnr[i])) * d 

    # Calculate the number of bits necessary to encode an interval
    min_feature = min(features_main)
    max_feature = max(features_main)
    feature_space_dim = int((max_feature - min_feature)*255)
    interval_range = int(np.mean(right - left))
    n_bits = 4 # General formula to calculate the minimum value necessary: int(log2(feature_space_dim/interval_range)) - 1
    format_bits = "{0:0" + str(n_bits) + "b}"

    # Define the maximum decimal number that can be generated with n_bits
    max_int = 0

    for i in range(n_bits):
        max_int += 2**i

    # For each feature:
    # - assign a random codeword
    # - use the interval to generate a polygonal chain
    # - add fake intervals (peaks)
    for i in range(n):

        # Generate a random binary codeword and concatenate it to the key
        c = secrets.randbits(n_bits)
        key += format_bits.format(c)

        # Generate a polygonal chain as a set of points {xi, yi}
        x = [features_main[i]]
        y = [c+1]

        # Define the line going through (left[i], c) and (features_main[i], c+1)
        ml = 1 / (x[0] - left[i])
        ql = (x[0]*c - left[i]*y[0]) / (x[0] - left[i])

        # Define the line going through (right[i], c) and (features_main[i], c+1)
        mr = 1 / (x[0] - right[i])
        qr = (x[0]*c - right[i]*y[0]) / (x[0] - right[i])

        # Choose 2 random points in the lines such that y < c (negative peaks)
        min_x = -ql / ml # to keep y > 0
        max_x = (max_int - ql) / ml # to keep y < max_int
        #interval_dim = 2 * abs(features_main[i] - left[i])
        #interval_dim = abs(max(features_main) - min(features_main))
        #interval_dim = 0.025

        x.append(random.uniform(max((min_feature + 0.0000000000000001), min_x), (x[-1] - 0.0000000000000001)))
        #x.append(random.uniform(x[-1] - interval_dim, x[-1]))
        #x.append(random.uniform(x[-1] - interval_dim, x[-1] - 2 * interval_dim))
        #x.append(x[-1] - interval_dim)
        #x.append(random.uniform(min_x, max_x))
        y.append(round(ml * x[-1] + ql))

        min_x = -qr / mr # to keep y > 0 
        max_x = (max_int - qr) / mr # to keep y < max_int

        x.append(random.uniform((x[-2] + 0.0000000000000001), min((max_feature - 0.0000000000000001), max_x)))
        #x.append(random.uniform(x[-2], x[-2] + interval_dim))
        #x.append(random.uniform(x[-2] + interval_dim, x[-2] + 2 * interval_dim))
        #x.append(x[-2] + interval_dim)
        #x.append(random.uniform(min_x, max_x))
        y.append(round(mr * x[-1] + qr))

        # Define the lines symmetric with respect to x = x[-1] | x = x[-2]
        ql += 2*ml*x[-2]
        ml *= -1

        qr += 2*mr*x[-1]
        mr *= -1

        # Add as many fake intervals (peaks) as necessary
        while len(y) < 2**(n_bits+1):

            # Choose 2 random points in the defined lines
            min_x = -ql / ml # to keep y > 0
            max_x = (max_int - ql) / ml # to keep y < max_int

            x.append(random.uniform(max((min_feature + 0.0000000000000001), min_x), (x[-1] - 0.0000000000000001)))
            #x.append(random.uniform(x[-1] - interval_dim, x[-1]))
            #x.append(random.uniform(x[-1] - interval_dim, x[-1] - 2 * interval_dim))
            #x.append(x[-1] - interval_dim)
            #x.append(random.uniform(min_x, max_x))
            y.append(round(ml * x[-1] + ql))

            min_x = -qr / mr # to keep y > 0 
            max_x = (max_int - qr) / mr # to keep y < max_int

            x.append(random.uniform((x[-2] + 0.0000000000000001), min((max_feature - 0.0000000000000001), max_x)))
            #x.append(random.uniform(x[-1], x[-1] + interval_dim))
            #x.append(random.uniform(x[-1] + interval_dim, x[-1] + 2 * interval_dim))
            #x.append(x[-1] + interval_dim)
            #x.append(random.uniform(min_x, max_x))
            y.append(round(mr * x[-1] + qr))
            
            # Define the lines symmetric with respect to x = x[-1] | x = x[-2]
            ql += 2*ml*x[-2]
            ml *= -1

            qr += 2*mr*x[-1]
            mr *= -1

        # Delete the extra point
        y.pop()
        x.pop()

        # Sort the points based on the x-values
        sorted_points = sorted(zip(x, y))
        tuples = zip(*sorted_points)
        x, y = [list(tuple) for tuple in tuples]
        tmp = [x, y]
        interval.append(tmp)

    return key, interval, n_bits

##-----------------------------------------------------------------------------
##  Function apply_bitmask(features, bit_mask)
##-----------------------------------------------------------------------------
##  Description:
##      Apply the bit-mask to extract the relevant features
##  
##  Input:
##      features            - An array of features extracted from an eye image.
##      bit_mask            - A 2-D array with the PSNR values of each pixel block.
##  
##  Output:
##      valuable_features   - An array containing the most reliable features
##-----------------------------------------------------------------------------
def apply_bitmask(features, bit_mask):
    mask = np.array(bit_mask)
    row, col = np.where(mask == True)
    valuable_features = []
    
    for i in range(len(row)):
        valuable_features.append(features[row[i], col[i]])

    return valuable_features
