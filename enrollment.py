##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from segment import segment
from normalize import normalize
from encode import encode

from cv2 import imread

from fastecdsa import keys, curve

import hashlib

import numpy as np

from reedsolo import RSCodec, ReedSolomonError

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def enrollment(img_name):

    eyelashes_thres = 80
    use_multiprocess = False
    nsym = 169
    

    # Read the image
    img = imread(img_name, 0)

    # Identify the iris and the pupil
    ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

    # Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
    polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], ciriris[2], 
                                        cirpupil[1], cirpupil[0], cirpupil[2],
                                        64, 256)

    # Encode the normalized iris region
    template, mask = encode(polar_array, noise_array, 18, 1, 0.5)

    str_template = ""
    for i in template:
        for j in i:
            str_template += str(int(j))

    features = int(str_template, 2).to_bytes((len(str_template) + 7) // 8, byteorder="big")

    rsc = RSCodec(nsym)

    encoded_features, pad = rsc.encode(features)

    # Format the key as a decimal value of appropriate size
    key = hashlib.sha512(features).hexdigest()
    private_key = int(key, 16)
    hash = hashlib.sha512(key.encode()).hexdigest()

    # Generate the public key using EC
    public_key = keys.get_public_key(private_key, curve.P256)

    return hash, public_key, pad