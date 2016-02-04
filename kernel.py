from eve import dataset
from eve import cvutil
from scipy import ndimage
import numpy as np
import cv2


def poc() :

    dset = dataset.dataset('data/basil/front')

    
    #h, s, v = cv2.split(cv2.cvtColor(dset[1], cv2.COLOR_BGR2HSV))

    result = np.copy(dset[1])


    kernel = np.array([[0,-1,0], 
                       [-1,5,-1], 
                       [0,-1,0]], dtype=float)

    #kernel *= 1/(kernel.shape[0] * kernel.shape[1])


    #for p in (b, g, r) :
    #    p[...] = ndimage.correlate(p, kernel)
    #    p[...] = np.clip(p, 0, 255)
    
    #v = ndimage.convolve(v, kernel)
    result = cv2.filter2D(result, -1, kernel)
    #v = np.clip(v, 0, 255)

    
    #result = cv2.merge((h, s, v))
    #result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    cvutil.comp_images(dset[1], result)

def poc2() :

    dset = dataset.dataset('data/basil/front')

    
    #h, s, v = cv2.split(cv2.cvtColor(dset[1], cv2.COLOR_BGR2HSV))

    past = np.copy(dset[1])
    current = np.copy(dset[2])
    future = np.copy(dset[3])

    past = past.astype(float)
    current = current.astype(float)
    future = future.astype(float)


    kernel = np.array([[0,0,0], 
                       [0,18,0], 
                       [0,0,0]], dtype=float)

    time_kernel = np.array([[-1,-1,-1], 
                             [-1,-1,-1], 
                             [-1,-1,-1]], dtype=float)


    past = cv2.filter2D(past, -1, time_kernel)
    current = cv2.filter2D(current, -1, kernel)
    future = cv2.filter2D(future, -1, time_kernel)

    result = past + current + future

    mask = ((result > 100) | (result < -100))
    result[mask] = 0

    mask = (result != 0)
    result[mask] = 255

    mask = ((result[:,:,0] == 0) & (result[:,:,1] == 0) & (result[:,:,2] == 0))
    mask = np.invert(mask)
    result[mask] = 255 

    cvutil.comp_images(dset[2], result.astype(np.uint8))

poc2()
