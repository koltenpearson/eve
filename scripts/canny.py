import cv2
import numpy as np
from eve import dataset
from eve import cvutil


def process(image) :
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(image, 100,200)

    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def poc() :
    image = dataset.dataset('data//basil/front')[2]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 100,200)

    cvutil.display_image(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))


if __name__ == '__main__' :
    poc()
