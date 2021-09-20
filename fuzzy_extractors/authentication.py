##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread

from preprocessing import preprocessing

import numpy as np

import hashlib

from fuzzy_extractor import FuzzyExtractor

##---------------------------------------------------------------------------------------------
##  Function authentication(img_name, hash, helper_data, extractor_dim, pre_processing)
##---------------------------------------------------------------------------------------------
##  Description:
##      Authenticate a user and re-generate the private key
##  
##  Input:
##      img_name        - The name of the eye image file
##      hash            - The hash of the private key
##      helper_data     - Helper data for the fuzzy extractor
##      extractor_dim   - Size of the fuzzy extractor
##      pre_processing  - Pre-processing method, can be "classic" or "enhanced"
##  
##  Output:
##      private_key                 - The user's private key
##      "Try again!"/"Wrong user!"  - Default output if the key is not correctly re-generated
##--------------------------------------------------------------------------------------------
def authentication(img_name, hash, helper_data, extractor_dim, pre_processing):

    # Pre-process the image
    features = preprocessing(img_name, pre_processing)

    # Define the Fuzzy extractor
    hamming_error = 8
    extractor = FuzzyExtractor(extractor_dim, hamming_error)

    # Re-generate the private key
    key = extractor.reproduce(features, helper_data)

    if key == None:
        return "Try again!"
    
    # Chek if the key has been correctly re-generated
    if hashlib.sha384(key).hexdigest() == hash:
        private_key = int.from_bytes(key, byteorder="big")
        return private_key
    else:
        return "Wrong user!"