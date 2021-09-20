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

img_name = "./CASIA1/1/001_2_1.jpg"

scheme_to_test = "f" # Can be "q", "f" or "p"
pre_processing_method = "enhanced" # Can be "classic" or "enhanced"

# Enrolment for Quantization scheme
if scheme_to_test == "q":
    private_key, public_key, hash, bit_mask, intervals, n_bits = enrollment(img_name)

    # Write on files the helper data to be stored on a server
    file = open("./test/public_key.txt", "w")
    file.write(str(public_key))
    file.close()
    
    file = open("./test/bit_mask.txt", "w")
    json.dump(bit_mask.tolist(), file)
    file.close()

    file = open("./test/intervals.txt", "w")
    json.dump(intervals, file)
    file.close()

    file = open("./test/n_bits.txt", "w")
    file.write(str(n_bits))
    file.close()

    file = open("./test/hash.txt", "w")
    file.write(str(hash))
    file.close()

# Enrolment for Fuzzy Extractor
if scheme_to_test == "f":
    private_key, public_key, hash, helper_data, extractor_dim = enrollment(img_name, pre_processing_method)

    # Write on files the helper data to be stored on a server
    file = open("./test/public_key.txt", "w")
    file.write(str(public_key))
    file.close()

    file = open("./test/helper_data1.txt", "w")
    json.dump(helper_data[0].tolist(), file)
    file.close()

    file = open("./test/helper_data2.txt", "w")
    json.dump(helper_data[1].tolist(), file)
    file.close()

    file = open("./test/helper_data3.txt", "w")
    json.dump(helper_data[2].tolist(), file)
    file.close()

    file = open("./test/extractor_dim.txt", "w")
    file.write(str(extractor_dim))
    file.close()

    file = open("./test/hash.txt", "w")
    file.write(str(hash))
    file.close()

# Enrolment for Private Template scheme
if scheme_to_test == "p":
    private_key, public_key, hash, helper_data = enrollment(img_name, pre_processing_method)

    # Write on files the helper data to be stored on a server
    file = open("./test/public_key.txt", "w")
    file.write(str(public_key))
    file.close()

    file = open("./test/helper_data.txt", "w")

    for i in range(len(helper_data)):
        helper_data[i] = helper_data[i].hex()

    json.dump(helper_data, file)
    file.close()

    file = open("./test/hash.txt", "w")
    file.write(str(hash))
    file.close()

# Release the private key
print("Private key: {}".format(private_key))

# Measure the speed of the enrollment
speed = time.perf_counter() - starting_time
print("Time: {} seconds".format(speed))