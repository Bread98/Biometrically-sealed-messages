# coding: utf-8
##----------------------------------------------------------------------------------------------
##  Import
##----------------------------------------------------------------------------------------------
import cv2
import numpy as np
import glob
import math
from scipy.spatial import distance
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics

##---------------------------------------------------------------------------------------------
##  Functions
##---------------------------------------------------------------------------------------------
#Equalizes the histogram of the image
def ImageEnhancement(normalized):
    enhanced=[]
    for res in normalized:
        res = res.astype(np.uint8)
        im=cv2.equalizeHist(res)
        enhanced.append(im)
    return enhanced