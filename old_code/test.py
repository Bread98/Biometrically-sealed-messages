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

# Enroll
for i in range(1, 109):
    img_format = "./CASIA1/{}/{:03d}_2_{}.jpg"

    img_to_enroll = img_format.format(i,i,1)

    hash, public_key, helper_data = enrollment(img_to_enroll)


    # Authenticate
    img_to_auth = [img_format.format(i,i,1), img_format.format(i,i,2), img_format.format(i,i,3), img_format.format(i,i,4)]

    for j in img_to_auth:
        key = authentication(j, hash, helper_data)

        print(key)

        print("-------------------------------------------------------------------------------------------------")

    print("\n\n")
