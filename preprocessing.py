##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread
from cv2 import imshow
from cv2 import waitKey

from pre_processing_classic.segment import segment
from pre_processing_classic.normalize import normalize
from pre_processing_classic.encode import encode

from pre_processing_enhanced.IrisLocalization import IrisLocalization
from pre_processing_enhanced.IrisNormalization import IrisNormalization
from pre_processing_enhanced.ImageEnhancement import ImageEnhancement
from pre_processing_enhanced.FeatureExtraction import FeatureExtraction

import numpy as np

##-----------------------------------------------------------------------------
##  Function preprocessing(img, method)
##-----------------------------------------------------------------------------
##  Description:
##      Enrol a new user
##  
##  Input:
##      img             - The image to be processed
##      method          - Pre-processing method, can be "classic" or "enhanced"
##  
##  Output:
##      features        - Array containing the extracted features
##-----------------------------------------------------------------------------
def preprocessing(img_name, method):

    # Integro-Differential operator and Log-Gabor filters
    if method == "classic":

        # Read the image
        img = imread(img_name, 0)
        
        # Parameters for segmentation
        eyelashes_thres = 80
        use_multiprocess = False

        # Identify the iris and the pupil
        ciriris, cirpupil, img_with_noise = segment(img, eyelashes_thres, use_multiprocess)

        #imshow("noisyeye", img_with_noise[0])
        #waitKey(0)

        # Normalize the iris region by unwraping the circular region into a rectangular block of constant dimensions
        polar_array, noise_array = normalize(img_with_noise, ciriris[1], ciriris[0], ciriris[2], 
                                            cirpupil[1], cirpupil[0], cirpupil[2], 8, 128)

        #imshow("polar", polar_array/255)
        #waitKey(0)

        # Extract the features from the normalized image
        template, mask = encode(polar_array, noise_array, 18, 1, 0.5)
            
        # Format the features
        str_template = ""

        for i in template:
            for j in i:
                str_template += str(int(j))

        features = int(str_template, 2).to_bytes((len(str_template) + 7) // 8, byteorder="big")
        
        # Alternative formatting method
        # features = np.array(template).tobytes()

        return features

    # Hough transform and 2D Gabor filters
    else:

        # Read the image
        if type(img_name) == str:
            img = [imread(img_name)]
        else:
            img = [imread(file) for file in img_name]
        #print(img)

        # Identify the iris and the pupil
        boundary, center = IrisLocalization(img)

        # Normalize the iris region
        normalized_iris = IrisNormalization(boundary,center)

        # Enhance the image with Hinstogram equalization
        enhanced_iris = ImageEnhancement(normalized_iris)

        # Extract the features from the normalized image
        template = np.array(FeatureExtraction(enhanced_iris)[0])
        
        # Format the features
        features = np.around(template, 2).tobytes()

        return features