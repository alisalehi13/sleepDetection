import cv2
import numpy as np
def histogram_equalization(image):
    # convert from RGB color-space to YCrCb
    ycrcb_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    # equalize the histogram of the Y channel
    ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])

    # convert back to RGB color-space from YCrCb
    equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
    
    return equalized_img



def hist_equ(image):
    colorimage_b = cv2.equalizeHist(image[:,:,0])
    colorimage_g = cv2.equalizeHist(image[:,:,1])
    colorimage_r = cv2.equalizeHist(image[:,:,2])
    
    # Next we stack our equalized channels back into a single image
    return np.stack((colorimage_b,colorimage_g,colorimage_r), axis=2)