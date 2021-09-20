##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from preprocessing import preprocessing

import numpy as np

import hashlib

from reedsolo import RSCodec, ReedSolomonError

import traceback

##---------------------------------------------------------------------------------------------
##  Function authentication(img_name, hash, pad, pre_processing)
##---------------------------------------------------------------------------------------------
##  Description:
##      Authenticate a user and re-generate the private key
##  
##  Input:
##      img_name        - The name of the eye image file
##      hash            - The hash of the private key
##      pad             - Error-correcting codes
##      pre_processing  - Pre-processing method, can be "classic" or "enhanced"
##  
##  Output:
##      private_key                 - The user's private key
##      "Try again!"/"Wrong user!"  - Default output if the key is not correctly re-generated
##--------------------------------------------------------------------------------------------
def authentication(img_name, hash, pad, pre_processing):

    # Pre-process the image
    features = preprocessing(img_name, pre_processing)

    # Define the Reed-Solomon encoder
    nsym = 160
    rsc = RSCodec(nsym)

    # Add the error-correcting codes in the appropriate position
    padded_features = bytearray()
    j = 0
    chunksize = 255 - nsym #nsyze - nsym

    for i in range(0, len(features), chunksize):

        chunk = features[i:i+chunksize]
        padded_features.extend(chunk + pad[j])
        j += 1

    # Decode the features
    try:
        decoded_features = rsc.decode(padded_features)[0]
    except ReedSolomonError:
        print(traceback.format_exc())
        return "Wrong user!"

    # Re-generate the private key
    key = hashlib.sha512(decoded_features).hexdigest()
    private_key = int(key, 16)
    new_hash = hashlib.sha512(key.encode()).hexdigest()

    # Chek if the key has been correctly re-generated
    if new_hash == hash:
        return private_key
    else:
        return "Wrong user!"