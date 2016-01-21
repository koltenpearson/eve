import cv2
import numpy as np
from matplotlib import pyplot as pp


def display_image(img) :

    pp.imshow(img[:,:,::-1], interpolation='bicubic')
    pp.xticks([])
    pp.yticks([])
    pp.show()
