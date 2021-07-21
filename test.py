##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from enrollment import enrollment
from authentication import authentication

import json

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
img_name = ["./img/casia1.jpg", "./img/casia2.jpg", "./img/casia3.jpg"]

private_key, public_key, hash, bit_mask, intervals, n_bits = enrollment(img_name)

"""
#Write data on files to store on a server
file = open("bit_mask1.txt", "w")
json.dump(bit_mask.tolist(), file)
file.close()

file = open("intervals1.txt", "w")
json.dump(intervals, file)
file.close()

file = open("n_bits1.txt", "w")
file.write(str(n_bits))
file.close()

file = open("hash1.txt", "w")
file.write(str(hash))
"""

#print(private_key)
#print(len(str(private_key)))

#print(hash)

#print(public_key)
#print(len(str(public_key)))

#print("--------------------------------------------------------------------------")

#print(intervals)

#print("--------------------------------------------------------------------------")


file = open("./test/hash1.txt", "r")
hash = file.read()
file.close()

file = open("./test/n_bits1.txt", "r")
n_bits = int(file.read())
file.close()

file = open("./test/bit_mask1.txt", "r")
bit_mask = json.load(file)
file.close()

file = open("./test/intervals1.txt", "r")
intervals = json.load(file)
print(intervals)

for i in range(50):
    key = authentication("./img/casia4.jpg", hash, bit_mask, intervals, n_bits)

    print(key)
    print("--------------------------------------------------------------------------")
#print(len(str(key)))

"""
eyelashes_thres = 80
use_multiprocess = False
block_x = 8
block_y = 4
n_features = 64
c = 15
d = 3.5

# Read the images
img = []

for i in img_name:
    img.append(imread(i, 0))

imshow("greyeye", img[0])
waitKey(0)

# Identify the iris and the pupil
ciriris = []
cirpupil = []
img_with_noise = []

for i in range(len(img)):
    ciriris_tmp, cirpupil_tmp, img_with_noise_tmp = segment(img[i], eyelashes_thres, use_multiprocess)

    ciriris.append(ciriris_tmp)
    cirpupil.append(cirpupil_tmp)
    img_with_noise.append(img_with_noise_tmp)

imshow("noisyeye", img_with_noise[0])
waitKey(0)

output = np.clip(img_with_noise * 255, 0, 255) # proper [0..255] range
output = output.astype(np.uint8)  # safe conversion
cv2.imwrite("./img/noisyeye.jpg", output)

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

imshow("polar", first_polar_array)
waitKey(0)

# Create the archtype from the first image
arc = archetype(first_polar_array, block_x, block_y)

out = "Archetype:

       {}

       "
print(out.format(arc))

imshow("Archetype", arc)
waitKey(0)

# Split the other images in x*y pixel blocks
splitted_images = []

for i in polar_array:
    splitted_images.append(pixel_blocks(i, block_x, block_y))

# Create the bit mask
helper_data, psnr = bit_mask(arc, n_features, splitted_images)

out = "Bit mask:

       {}

       "
print(out.format(helper_data))

key, interval = intervals(arc, helper_data, psnr, c, d)

out = "Intervals:

       {}

        KEY:
        {}
       "
print(out.format(interval, key))

print(len(key))
"""