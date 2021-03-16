#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:52:10 2021

@author: Jonathan Robinson [@robin0025]
"""

import numpy as np
from math import fmod

# Function generate accurate sinusoid
# Point distance based on desired frequency by frameR to give best reliability
# Inputs:
# - freq [freq=4] = the desired frequency
# - amp [amp=0.5] = the desire signal amplitude from a centre point
# - frameR [frameR=60] = the refresh rate of your system
# - offset [offset=0.5] = the offset. This default is used so as to fit opacity gradient
# Ouput:
# - sinw = a sinusoid that fits your parameters
def sinOp(freq=4,amp=0.5,frameR=60,offset=0.5):
    # extend the array length based on the level of fineness required
    time = np.arange(0,1,1.0/(frameR*freq)) 
    phi = np.pi*4
    sinw = (amp*np.cos(2*np.pi*freq*time + phi))+offset #makesign values
    
    return(sinw)


# Function set up to deal with N length values and select the most appropriate data point
# This can be used with function above to fit second or 
# Inputs:
# - t = time in seconds    
# - s_array = an s_array of numbers that need to be select according to the time
# - totTime [totTime=1.0] = time over which the s_array has been charted
# - type [type=0] = type of output
#       - 0 = just give the best index in the s_array
#       - 1 = set opacity based on best index in the s_array
#       - 2 = set constrast based onbest index in the s_array
# - imObj [imObj=None] = object to set the value of
# Ouput:
# - default: sample = most appropriate sample in array
# - based on type change in stimulus value
def selectgradient(t,s_array,totTime=1.0,types=0, imObj=None):
    dec= fmod(t,totTime)  
    sample = int(round(len(s_array)*(dec/totTime)))
    if types == 1 and imObj != None: 
       imObj.setOpacity(s_array[sample])
    elif types == 2 and imObj != None:
       imObj.setContrast(s_array[sample])
    else:
        return(sample)

