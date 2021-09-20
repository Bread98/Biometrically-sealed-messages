##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from segment import segment
from normalize import normalize
from encode import encode

from cv2 import imread

import numpy as np

import hashlib

from reedsolo import RSCodec, ReedSolomonError

import traceback

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def authentication(img_name, hash, pad):

    eyelashes_thres = 80
    use_multiprocess = False
    nsym = 169

    # Read the images
    img = imread(img_name, 0)

    # Identify the iris and the pupil
    ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

    # Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
    polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], 
                                        ciriris[2], cirpupil[1], cirpupil[0], 
                                        cirpupil[2], 64, 256)

    template, mask = encode(polar_array, noise_array, 18, 1, 0.5)

    str_template = ""
    for i in template:
        for j in i:
            str_template += str(int(j))

    features = int(str_template, 2).to_bytes((len(str_template) + 7) // 8, byteorder="big")

    padded_features = bytearray()
    j = 0

    chunksize = 255 - nsym #nsyze - nsym
    for i in range(0, len(features), chunksize):
        # Split the long message in a chunk
        chunk = features[i:i+chunksize]
        padded_features.extend(chunk + pad[j])
        j += 1

    rsc = RSCodec(nsym)

    try:
        decoded_features = rsc.decode(padded_features)[0]
    except ReedSolomonError:
        print(traceback.format_exc())
        return "Wrong user!"

    key = hashlib.sha512(decoded_features).hexdigest()
    private_key = int(key, 16)
    new_hash = hashlib.sha512(key.encode()).hexdigest()

    if new_hash == hash:
        print("Successfully authenticated!")
        return private_key
    else:
        return "Wrong user!"