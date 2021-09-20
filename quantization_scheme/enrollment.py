##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey

from pre_processing_classic.segment import segment
from pre_processing_classic.normalize import normalize

from quantization_scheme.archetype import archetype
from quantization_scheme.archetype import pixel_blocks
from quantization_scheme.bit_mask import bit_mask
from quantization_scheme.intervals import intervals

from fastecdsa import keys, curve

import hashlib

##-----------------------------------------------------------------------------
##  Function enrollment(img_name)
##-----------------------------------------------------------------------------
##  Description:
##      Enrol a new user
##  
##  Input:
##      img_name    - A list of file names
##  
##  Output:
##      private_key     - The user's private key
##      public_key      - The user's public key
##      hash            - The hash of the private key
##      mask            - A 2D bit-mask pointing to the most reliable features
##      interval        - An array of points, representing the intervals
##      n_bits          - Number of bits used to encode an interval
##-----------------------------------------------------------------------------
def enrollment(img_name):

    # Parameters for segmentation
    eyelashes_thres = 80
    use_multiprocess = False

    # Pixel-block dimention
    block_x = 8 
    block_y = 4

    # Number of valuable features
    n_features = 64

    c = 15
    d = 3.5

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

    # Create the archtype from the first image
    arc = archetype(first_polar_array, block_x, block_y)

    #imshow("Archetype", arc/255)
    #waitKey(0)

    # Split the other images in x*y pixel blocks
    splitted_images = []

    for i in polar_array:
        splitted_images.append(pixel_blocks(i, block_x, block_y))

    # Create the bit mask
    mask, psnr = bit_mask(arc, n_features, splitted_images)

    # Generate the intervals and the private key
    priv_key, interval, n_bits = intervals(arc, mask, psnr, c, d)

    # Hash the private key
    hash = hashlib.sha384(priv_key.encode()).hexdigest()

    # Format the key as a decimal value of appropriate size
    private_key = int(priv_key, 2)
    
    # Generate the public key using ECC
    public_key = keys.get_public_key(private_key, curve.P256)

    return private_key, public_key, hash, mask, interval, n_bits