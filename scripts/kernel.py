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

    dset = dataset.dataset('data/basil/front', dtype=float)

    
    #h, s, v = cv2.split(cv2.cvtColor(dset[1], cv2.COLOR_BGR2HSV))

    past = np.copy(dset[1])
    current = np.copy(dset[2])
    future = np.copy(dset[3])

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

    dset.set_dtype(np.uint8)

    cvutil.comp_images(dset[2], result.astype(np.uint8))


def main() :

    current_dset = dataset.dataset('data/basil/front', dtype=float)
    comp_dset = dataset.dataset('data/basil/front', dtype=float)


    kernel = np.array([[0,0,0], 
                       [0,18,0], 
                       [0,0,0]], dtype=float)

    time_kernel = np.array([[-1,-1,-1], 
                            [-1,-1,-1], 
                            [-1,-1,-1]], dtype=float)


    for i in comp_dset :
        i[...] = cv2.filter2D(i, -1, time_kernel)

    for i in current_dset :
        i[...] = cv2.filter2D(i, -1, kernel)

    for i in range(1, len(current_dset) -1 ) :
        current_dset[i] = comp_dset[i-1] + current_dset[i] + comp_dset[i+1] 

        mask = ((current_dset[i] > 100) | (current_dset[i] < -100))
        current_dset[i][mask] = 0

        mask = (current_dset[i] != 0)
        current_dset[i][mask] = 255

        mask = ((current_dset[i][:,:,0] == 0) & (current_dset[i][:,:,1] == 0) & (current_dset[i][:,:,2] == 0))
        mask = np.invert(mask)
        current_dset[i][mask] = 255 

        current_dset[i] = current_dset[i].astype(np.uint8)

    current_dset.set_dtype(np.uint8)

    current_dset.write_images('movement3')

main()
