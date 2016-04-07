import cv2
import numpy as np
from eve import cvutil

buffer = []

def process(image) :
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(image, 100,200)

    if len(buffer) < 10 :
        buffer.append(edge)
    else :
        buffer.pop(0)
        buffer.append(edge)

    slate = np.zeros_like(image, dtype=float)

    for b in buffer :
        slate += b

    slate //= 255
    slate *= (255/10)

    slate = slate.astype(image.dtype)
    slate = cv2.cvtColor(slate, cv2.COLOR_GRAY2BGR)
    return slate
