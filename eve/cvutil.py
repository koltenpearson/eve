import cv2
import numpy as np
from matplotlib import pyplot as pp
import sys

def comp_images(img1, img2) :

    f = pp.figure()
    f.add_subplot(2,1,1)
    pp.imshow(img1[:,:,::-1], interpolation='none')
    pp.xticks([])
    pp.yticks([])

    f.add_subplot(2,1,2)
    pp.imshow(img2[:,:,::-1], interpolation='none')
    pp.xticks([])
    pp.yticks([])

    pp.show()

def display_image(img) :

    pp.imshow(img[:,:,::-1], interpolation='none')
    pp.xticks([])
    pp.yticks([])
    pp.show()


