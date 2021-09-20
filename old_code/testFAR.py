##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from authentication import authentication
from enrollment import enrollment

import json

import random

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------

far = 0

for i in range(1, 109):
    img_format = "./CASIA1/{}/{:03d}_2_{}.jpg"

    # Enroll
    img_to_enroll = img_format.format(i,i,1)

    hash, public_key, helper_data = enrollment(img_to_enroll)

    # Authenticate
    u = random.randint(1, 108)

    while u == i:
        u = random.randint(1, 108)
    
    img_to_auth = [img_format.format(u,u,1), img_format.format(u,u,2), img_format.format(u,u,3), img_format.format(u,u,4)]

    for j in img_to_auth:
        key = authentication(j, hash, helper_data)

        if key != "Wrong user!":
            far += 1

        print(key)

        print("-------------------------------------------------------------------------------------------------")

    print("\n\n")

far = far / (108*4)

print(("The FAR is: {}").format(far))