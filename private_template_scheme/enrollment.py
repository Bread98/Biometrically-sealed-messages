##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from preprocessing import preprocessing

from fastecdsa import keys, curve

import hashlib

import numpy as np

from reedsolo import RSCodec, ReedSolomonError

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
##      pad             - Error-correcting codes to store as helper data
##-----------------------------------------------------------------------------
def enrollment(img_name, pre_processing):

    # Pre-process the image
    features = preprocessing(img_name, pre_processing)
    
    # Define the Reed-Solomon encoder
    nsym = 160
    rsc = RSCodec(nsym)

    # Encode the features
    encoded_features, pad = rsc.encode(features)

    # Generate and format the private key as a decimal value of appropriate size
    key = hashlib.sha512(features).hexdigest()
    private_key = int(key, 16)

    # Hash the private key
    hash = hashlib.sha512(key.encode()).hexdigest()

    # Generate the public key using ECC
    public_key = keys.get_public_key(private_key, curve.P256)

    return private_key, public_key, hash, pad