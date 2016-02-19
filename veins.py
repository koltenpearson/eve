import numpy as np
import cv2
from eve import dataset
from eve import cvutil

def poc() :

    dset = dataset.dataset('data/basil/front', dtype=float)

    image = np.copy(dset[1])

    antia = np.array( [[1, 2, 4, 2 ,1],
                       [2, 4, 8, 4, 2],
                       [4, 8, 16, 8, 4],
                       [2, 4, 8, 4, 2],
                       [1, 2, 4, 2, 1]], dtype=float)
    
    big_antia = np.array( [[1, 2, 4, 8 ,4, 2, 1],
                           [2, 4, 8, 16, 8, 4, 2],
                           [4, 8, 16, 32, 16, 8, 4],
                           [8, 16, 32, 64, 32, 16, 8],
                           [4, 8, 16, 32, 16, 8, 4],
                           [2, 4, 8, 16, 8, 4, 2],
                           [1, 2, 4, 8 ,4, 2, 1]], dtype=float)

    med = np.array( [   [1,1,1],
                        [1,0,1],
                        [1,1,1]], dtype=float)

    big_med = np.array( [  [1, 1, 1, 1 ,1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 0, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1], ], dtype = float)

    sharp = np.array( [   [0,-1,0],
                          [-1,5,-1],
                          [0,-1,0]], dtype=float)

    big_sharp = np.array( [  [-1, 0, 0, -1 ,0, 0, -1],
                             [0, -1, 0, -1, 0, -1, 0],
                             [0, 0, -1, -1, -1, 0, 0],
                             [-1, -1, -1, 25, -1, -1, -1],
                             [0, 0, -1, -1, -1, 0, 0],
                             [0, -1, 0, -1, 0, -1, 0],
                             [-1, 0, 0, -1, 0, 0, -1], ], dtype = float)



    med *= (1/8)
    big_med *= (1/48)
    antia *= (1/104)
    big_antia *= (1/np.sum(big_antia))

    sharp_image = cv2.filter2D(image, -1, big_sharp)

    blur_image = cv2.filter2D(image, -1, big_med)

    sharp_image = np.clip(sharp_image, 0, 255)
    blur_image = np.clip(blur_image, 0, 255)

    cvutil.comp_images(sharp_image.astype(np.uint8), blur_image.astype(np.uint8))


    result1 = dset[1] - blur_image

    result1[result1 < -3] = 0 
    result1[result1 > 3] = 0 
    result1[result1 != 0] = 255

    mask = (result1[...,0] == 0) & (result1[...,1] == 0) & (result1[...,2] == 0)
    mask = np.invert(mask)
    result1[mask] = 255

    result2 = sharp_image - blur_image

    result2[result2 < -40] = 0 
    result2[result2 > 40] = 0 
    result2[result2 != 0] = 255

    mask = (result2[...,0] == 0) & (result2[...,1] == 0) & (result2[...,2] == 0)
    mask = np.invert(mask)
    result2[mask] = 255


    cvutil.comp_images(result1.astype(np.uint8), result2.astype(np.uint8))

poc()

