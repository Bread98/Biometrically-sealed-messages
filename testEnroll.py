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

#Write data on files to store on a server
file = open("./test/bit_mask3.txt", "w")
json.dump(bit_mask.tolist(), file)
file.close()

file = open("./test/intervals3.txt", "w")
json.dump(intervals, file)
file.close()

file = open("./test/n_bits3.txt", "w")
file.write(str(n_bits))
file.close()

file = open("./test/hash3.txt", "w")
file.write(str(hash))
file.close()

#print(private_key)
#print(len(str(private_key)))

#print(hash)

#print(public_key)
#print(len(str(public_key)))

#print("--------------------------------------------------------------------------")

#print(intervals)

#print("--------------------------------------------------------------------------")