##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import cv2
import numpy as np

from segment import segment
from normalize import normalize
from archtype import archetype
from archtype import pixel_blocks
from bit_mask import bit_mask


##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
img_name = "./img/casia.jpg"
eyelashes_thres = 80
use_multiprocess = False
block_x = 8
block_y = 4
n_features = 64
c = 15
d = 3.5

# Read the images
img = cv2.imread(img_name, 0)

cv2.imwrite("./img/greyeye.jpg", img)
cv2.imshow("greyeye", img)
cv2.waitKey(0)

# Identify the iris and the pupil
ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

cv2.imshow("noisyeye", img_with_noise)
cv2.waitKey(0)

output = np.clip(img_with_noise * 255, 0, 255) # proper [0..255] range
output = output.astype(np.uint8)  # safe conversion
cv2.imwrite("./img/noisyeye.jpg", output)

# Normalize iris region by unwraping the circular region into a rectangular block of constant dimensions
polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], ciriris[2], 
                                    cirpupil[1], cirpupil[0], cirpupil[2],
                                    64, 256)

cv2.imshow("polar", polar_array)
cv2.waitKey(0)

output = np.clip(polar_array * 255, 0, 255) # proper [0..255] range
output = output.astype(np.uint8)  # safe conversion
cv2.imwrite("./img/polar.jpg", output)

# Create the archtype from the first image
arc = archetype(polar_array, block_x, block_y)

out = """Archetype:

       {}

       """
print(out.format(arc))

cv2.imshow("Archetype", arc)
cv2.waitKey(0)

output = np.clip(arc * 255, 0, 255) # proper [0..255] range
output = output.astype(np.uint8)  # safe conversion
cv2.imwrite("./img/Archetype.jpg", output)