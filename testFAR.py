##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

# Quantization scheme
# from quantization_scheme.enrollment import enrollment
# from quantization_scheme.authentication import authentication

# Fuzzy Extractor
# from fuzzy_extractors.enrollment import enrollment
# from fuzzy_extractors.authentication import authentication

# Private Template scheme
from private_template_scheme.enrollment import enrollment
from private_template_scheme.authentication import authentication

import random

import time

import statistics

import json

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
scheme_to_test = "p" # Can be "q", "f" or "p"
pre_processing_method = "enhanced" # Can be "classic" or "enhanced"

img_format = "./CASIA1/{}/{:03d}_2_{}.jpg"

far = 0

time_enroll = []
time_auth = []

# Quantization scheme
if scheme_to_test == "q":
    for i in range(1, 109):

        img_to_enroll = [img_format.format(i,i,1), img_format.format(i,i,2), img_format.format(i,i,3), img_format.format(i,i,4)]

        # Take the starting time for enrollment
        starting_time = time.perf_counter()

        # Enrol the user
        private_key, public_key, hash, bit_mask, intervals, n_bits = enrollment(img_to_enroll)
        
        # Measure the speed of the enrollment
        tmp = time.perf_counter() - starting_time
        time_enroll.append(tmp)
        print("Enrolled in: {} seconds".format(tmp))

        # Select a random impostor
        u = random.randint(1, 108)

        while u == i:
            u = random.randint(1, 108)
        
        img_to_auth = [img_format.format(u,u,1), img_format.format(u,u,2), img_format.format(u,u,3), img_format.format(u,u,4)]

        # Try to authenticate the impostor multiple times
        for j in img_to_auth:

            # Take the starting time for authentication
            starting_time = time.perf_counter()

            # Authenticate the user
            private_key = authentication(j, hash, bit_mask, intervals, n_bits)
        
            # Measure the speed of the authentication
            tmp = time.perf_counter() - starting_time
            time_auth.append(tmp)
            print("Authenticated in: {} seconds".format(tmp))

            if private_key != "Wrong user!":
                far += 1

            print(private_key)
            print("-------------------------------------------------------------------------------------------------")
        print("\n\n")

# Fuzzy Extractor
if scheme_to_test == "f":
    for i in range(1, 109):

        img_to_enroll = img_format.format(i,i,1)

        # Take the starting time for enrollment
        starting_time = time.perf_counter()

        # Enrol the user
        private_key, public_key, hash, helper_data, extractor_dim = enrollment(img_to_enroll, pre_processing_method)
        
        # Measure the speed of the enrollment
        tmp = time.perf_counter() - starting_time
        time_enroll.append(tmp)
        print("Enrolled in: {} seconds".format(tmp))

        # Select a random impostor
        u = random.randint(1, 108)

        while u == i:
            u = random.randint(1, 108)
        
        img_to_auth = [img_format.format(u,u,1), img_format.format(u,u,2), img_format.format(u,u,3), img_format.format(u,u,4)]

        # Try to authenticate the impostor multiple times
        for j in img_to_auth:

            # Take the starting time for authentication
            starting_time = time.perf_counter()

            # Authenticate the user
            private_key = authentication(j, hash, helper_data, extractor_dim, pre_processing_method)
        
            # Measure the speed of the authentication
            tmp = time.perf_counter() - starting_time
            time_auth.append(tmp)
            print("Authenticated in: {} seconds".format(tmp))

            if private_key != "Wrong user!":
                far += 1

            print(private_key)
            print("-------------------------------------------------------------------------------------------------")
        print("\n\n")

# Private Template scheme
if scheme_to_test == "p":
    for i in range(1, 109):

        img_to_enroll = img_format.format(i,i,1)

        # Take the starting time for enrollment
        starting_time = time.perf_counter()

        # Enrol the user
        private_key, public_key, hash, helper_data = enrollment(img_to_enroll, pre_processing_method)
        
        # Measure the speed of the enrollment
        tmp = time.perf_counter() - starting_time
        time_enroll.append(tmp)
        print("Enrolled in: {} seconds".format(tmp))

        # Select a random impostor
        u = random.randint(1, 108)

        while u == i:
            u = random.randint(1, 108)
        
        img_to_auth = [img_format.format(u,u,1), img_format.format(u,u,2), img_format.format(u,u,3), img_format.format(u,u,4)]

        # Try to authenticate the impostor multiple times
        for j in img_to_auth:

            # Take the starting time for authentication
            starting_time = time.perf_counter()

            # Authenticate the user
            private_key = authentication(j, hash, helper_data, pre_processing_method)
        
            # Measure the speed of the authentication
            tmp = time.perf_counter() - starting_time
            time_auth.append(tmp)
            print("Authenticated in: {} seconds".format(tmp))

            if private_key != "Wrong user!":
                far += 1

            print(private_key)
            print("-------------------------------------------------------------------------------------------------")
        print("\n\n")

far = far / (108*4)

print("The FAR is: {}".format(far))

print("The mean execution time for enrollment is: {}".format(statistics.mean(time_enroll)))

print("The mean execution time for authentication is: {}".format(statistics.mean(time_auth)))