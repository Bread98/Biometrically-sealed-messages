##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from enrollment import enrollment

import json

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
img_name = "./img/casia1.jpg"

hash, public_key, helper_data = enrollment(img_name)

#Write data on files to store on a server
file = open("./test/public_key_rs.txt", "w")
file.write(str(public_key))
file.close()

file = open("./test/helper_data_rs.txt", "w")

for i in range(len(helper_data)):
    helper_data[i] = helper_data[i].hex()

json.dump(helper_data, file)
file.close()

file = open("./test/hash_rs.txt", "w")
file.write(str(hash))
file.close()
