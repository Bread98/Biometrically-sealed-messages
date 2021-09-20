##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

# Quantization scheme
# from quantization_scheme.enrollment import enrollment
# from quantization_scheme.authentication import authentication

# Fuzzy Extractor
from fuzzy_extractors.enrollment import enrollment
from fuzzy_extractors.authentication import authentication

# Private Template scheme
# from private_template_scheme.enrollment import enrollment
# from private_template_scheme.authentication import authentication

import json

import time

##-----------------------------------------------------------------------------
##  Main Function
##-----------------------------------------------------------------------------

# Take the starting time
starting_time = time.perf_counter()

img_name = ["./CASIA1/1/001_2_1.jpg", "./CASIA1/1/001_2_2.jpg", "./CASIA1/1/001_2_3.jpg", "./CASIA1/1/001_2_4.jpg"]

scheme_to_test = "f" # Can be "q", "f" or "p"
pre_processing_method = "classic" # Can be "classic" or "enhanced"

# Authentication for Quantization scheme
if scheme_to_test == "q":
    # Read the helper data
    file = open("./test/hash.txt", "r")
    hash = file.read()
    file.close()

    file = open("./test/n_bits.txt", "r")
    n_bits = int(file.read())
    file.close()

    file = open("./test/bit_mask.txt", "r")
    bit_mask = json.load(file)
    file.close()

    file = open("./test/intervals.txt", "r")
    intervals = json.load(file)
    file.close()

    # Test multiple authentications
    for i in img_name:
        private_key = authentication(i, hash, bit_mask, intervals, n_bits)

# Authentication for Fuzzy Extractor
if scheme_to_test == "f":
    file = open("./test/hash.txt", "r")
    hash = file.read()
    file.close()

    file = open("./test/extractor_dim.txt", "r")
    extractor_dim = int(file.read())
    file.close()

    file = open("./test/helper_data1.txt", "r")
    helper_data1 = np.array(json.load(file), dtype='uint8')
    file.close()

    file = open("./test/helper_data2.txt", "r")
    helper_data2 = np.array(json.load(file), dtype='uint8')
    file.close()

    file = open("./test/helper_data3.txt", "r")
    helper_data3 = np.array(json.load(file), dtype='uint8')
    file.close()

    helper_data = (helper_data1, helper_data2, helper_data3)

    for i in img_name:
        private_key = authentication(i, hash, helper_data, extractor_dim, pre_processing_method)

# Authentication for Private Template scheme
if scheme_to_test == "p":
    file = open("./test/helper_data.txt", "r")
    helper_data = json.load(file)

    for i in range(len(helper_data)):
        helper_data[i] = bytearray.fromhex(helper_data[i])

    file.close()

    file = open("./test/hash.txt", "r")
    hash = file.read()
    file.close()

    for i in img_name:
        private_key = authentication(i, hash, helper_data, pre_processing_method)

# Release the private key
print("Private key".format(private_key))

# Measure the speed of the enrollment
speed = time.perf_counter() - starting_time
print("Time: {} seconds".format(speed))