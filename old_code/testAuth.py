##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from authentication import authentication

import json

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
img_name = ["./img/casia1.jpg", "./img/casia2.jpg", "./img/casia_alt.jpg", "./img/casia_alt_1.jpg"]

file = open("./test/helper_data_rs.txt", "r")
helper_data = json.load(file)

for i in range(len(helper_data)):
    helper_data[i] = bytearray.fromhex(helper_data[i])

file.close()

file = open("./test/hash_rs.txt", "r")
hash = file.read()
file.close()

for i in img_name:
    key = authentication(i, hash, helper_data)

    print(key)

    print("-------------------------------------------------------------------------------------------------")
print("\n\n")
