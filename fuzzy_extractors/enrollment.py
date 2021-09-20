##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread

from preprocessing import preprocessing

from fastecdsa import keys, curve

import hashlib

import numpy as np

from fuzzy_extractor import FuzzyExtractor

##-----------------------------------------------------------------------------
##  Function enrollment(img_name, pre_processing)
##-----------------------------------------------------------------------------
##  Description:
##      Enrol a new user
##  
##  Input:
##      img_name        - The name of the eye image file
##      pre_processing  - Pre-processing method, can be "classic" or "enhanced"
##  
##  Output:
##      private_key     - The user's private key
##      public_key      - The user's public key
##      hash            - The hash of the private key
##      helper_data     - Helper data from the fuzzy extractor
##      extractor_dim   - Size of the fuzzy extractor
##-----------------------------------------------------------------------------
def enrollment(img_name, pre_processing):

    # Pre-process the image
    features = preprocessing(img_name, pre_processing)

    # Define the Fuzzy extractor
    extractor_dim = len(features)
    hamming_error = 8
    extractor = FuzzyExtractor(extractor_dim, hamming_error)

    # Generate the private key
    key, helper_data = extractor.generate(features)

    # Hash the private key
    hash = hashlib.sha384(key).hexdigest()

    # Format the key as a decimal value of appropriate size
    private_key = int.from_bytes(key, byteorder="big")
    
    # Generate the public key using EC
    public_key = keys.get_public_key(private_key, curve.P256)

    return private_key, public_key, hash, helper_data, extractor_dim