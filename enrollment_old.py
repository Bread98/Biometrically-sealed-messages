##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey

from segment import segment
from normalize import normalize
from archetype import archetype
from archetype import pixel_blocks
from bit_mask import bit_mask
from extract_features import extract_features

from fastecdsa import keys, curve

import hashlib

import numpy as np

import sys

from encode import encode

from reedsolo import RSCodec, ReedSolomonError

import itertools

from array import array

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def enrollment(img_name):

    eyelashes_thres = 80
    use_multiprocess = False
    block_x = 8
    block_y = 4
    n_features = 32
    hamming_error = 8

    # Read the images
    img = []

    for i in img_name:
        img.append(imread(i, 0))

    # Identify the iris and the pupil
    ciriris = []
    cirpupil = []
    img_with_noise = []

    for i in range(len(img)):
        ciriris_tmp, cirpupil_tmp, img_with_noise_tmp = segment(img[i], eyelashes_thres, use_multiprocess)

        ciriris.append(ciriris_tmp)
        cirpupil.append(cirpupil_tmp)
        img_with_noise.append(img_with_noise_tmp)

    #imshow("noisyeye", img_with_noise[0])
    #waitKey(0)

    # Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
    polar_array = []
    noise_array = []

    for i in range(len(img)):
        polar_array_tmp, noise_array_tmp = normalize(img_with_noise[i], ciriris[i][1], ciriris[i][0], ciriris[i][2], 
                                                    cirpupil[i][1], cirpupil[i][0], cirpupil[i][2],
                                                    64, 256)
        polar_array.append(polar_array_tmp)
        noise_array.append(noise_array_tmp)

    first_polar_array = polar_array.pop(0)

    #imshow("polar", first_polar_array/255)
    #waitKey(0)

    template, mask = encode(first_polar_array, noise_array[0], 18, 1, 0.5)

    
    str_t = ""
    for i in template:
        for j in i:
            str_t += str(int(j))

    bytes_features = int(str_t, 2).to_bytes((len(str_t) + 7) // 8, byteorder="big")
    
    tmp_features = list(itertools.chain.from_iterable(template))
    features = [int(i) for i in tmp_features]

    rsc = RSCodec(250)
    #rsc = RSCodec(500, c_exp=10)

    encoded_features, pad = rsc.encode(bytes_features)
    #print(encoded_features)
    print(len(encoded_features))
    #print(type(encoded_features))
    #print(features)
    #print(len(features))

    #key = hashlib.sha512(encoded_features + bytes_features).hexdigest()
    #key = hashlib.sha512(encoded_features.tobytes() + bytes_features).hexdigest()
    key = 0
    
    # Hash the private key
    #hash = hashlib.sha384(key).hexdigest()

    # Format the key as a decimal value of appropriate size
    #private_key = int(key, 16)
    private_key = 0

    # Generate the public key using EC
    #public_key = keys.get_public_key(private_key, curve.P256)

    t, m = encode(polar_array[1], noise_array[2], 18, 1, 0.5)

    st = ""
    for i in t:
        for j in i:
            st += str(int(j))

    bf = int(st, 2).to_bytes((len(st) + 7) // 8, byteorder="big")
    f = bytearray()
    j = 0

    chunksize = 255 - 250 #nsyze - nsym
    for i in range(0, len(bf), chunksize):
        # Split the long message in a chunk
        chunk = bf[i:i+chunksize]
        f.extend(chunk + pad[j])
        j += 1
    
    #tmp_f = list(itertools.chain.from_iterable(t))
    #f = [int(i) for i in tmp_f]
    print(f)
    print(len(f))

    dec_features = rsc.decode(f)[0]
    print(bytes_features)
    print(dec_features)
    print(len(dec_features))

    if dec_features == bytes_features:
        print("NICE!")

    return private_key, key, encoded_features