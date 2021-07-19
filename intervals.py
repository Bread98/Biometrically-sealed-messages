##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np
from math import log2
import random
import secrets
from sklearn.utils import shuffle

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
def intervals(archetype, bit_mask, psnr, c, d):
    key = ""
    interval = []

    # Apply the bitmask to extract the most reliable features and their psnr
    features = apply_bitmask(archetype, bit_mask)
    features_psnr = apply_bitmask(psnr, bit_mask)

    # Generate the intervals
    n = len(features)
    left = np.zeros(n, dtype=float)
    right = np.zeros(n, dtype=float)

    for i in range(n):
        left[i] = features[i] - pow(2, (c/features_psnr[i])) * d 
        right[i] = features[i] + pow(2, (c/features_psnr[i])) * d 

    # Calculate the number of bits necessary to encode an interval
    interval_range = int(np.mean(right - left))
    n_bits = int(log2(256/interval_range)) - 1
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
        x = [features[i]]
        y = [c+1]

        # Define the line going through (left[i], c) and (features[i], c+1)
        ml = 1 / (x[0] - left[i])
        ql = (x[0]*c - left[i]*y[0]) / (x[0] - left[i])

        # Define the line going through (right[i], c) and (features[i], c+1)
        mr = 1 / (x[0] - right[i])
        qr = (x[0]*c - right[i]*y[0]) / (x[0] - right[i])

        # Choose 2 random points in the lines such that y < c (negative peaks)
        y.append(random.randint(-max_int, (c-1)))
        x.append((y[-1] - ql) / ml)

        y.append(random.randint(-max_int, (c-1)))
        x.append((y[-1] - qr) / mr)

        # Define the lines symmetric with respect to x = x[-1] | x = x[-2]
        ql += 2*ml*x[-2]
        ml *= -1

        qr += 2*mr*x[-1]
        mr *= -1

        # Add as many fake intervals (peaks) as necessary
        peak = True
        
        while len(y) < 2**(n_bits+1):

            if peak:
                # Choose 2 random points (peaks) in the lines such that y < y[-2] (y of the last added left/right negative peak)
                y.append(random.randint(y[-2], max_int))
                x.append((y[-1] - ql) / ml)

                y.append(random.randint(y[-2], max_int))
                x.append((y[-1] - qr) / mr)

                peak = False
            else:
                # Choose 2 random points (negative peaks) in the lines such that y < y[-2] (y of the last added left/right peak)
                y.append(random.randint(-max_int, y[-2]))
                x.append((y[-1] - ql) / ml)

                y.append(random.randint(-max_int, y[-2]))
                x.append((y[-1] - qr) / mr)

                peak = True
            
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

def apply_bitmask(features, bit_mask):

    row, col = np.where(bit_mask == True)
    valuable_features = []
    
    for i in range(len(row)):
        valuable_features.append(features[row[i], col[i]])

    return valuable_features
