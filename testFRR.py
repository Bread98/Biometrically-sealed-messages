##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np

from authentication import authentication
from enrollment import enrollment

import json

##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------

frr = 0

for i in range(1, 109):
    img_format = "./CASIA1/{}/{:03d}_2_{}.jpg"

    # Enroll
    img_to_enroll = img_format.format(i,i,1)

    hash, public_key, helper_data = enrollment(img_to_enroll)

    # Authenticate
    img_to_auth = [img_format.format(i,i,1), img_format.format(i,i,2), img_format.format(i,i,3), img_format.format(i,i,4)]

    for j in img_to_auth:
        key = authentication(j, hash, helper_data)

        if key == "Wrong user!":
            frr += 1

        print(key)

        print("-------------------------------------------------------------------------------------------------")

    print("\n\n")

frr = frr / (108*4)

print(("The FRR is: {}").format(frr))