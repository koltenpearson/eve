from eve import dataset
from eve import cvutil
from scipy import ndimage
import numpy as np
import cv2


def poc() :

    dset = dataset.dataset('data/basil/front')
    converted = cv2.cvtColor(dset[1], cv2.COLOR_BGR2HSV)


    h, s, v = cv2.split(converted)

    mask = (h > 45) & (h < 90)

    mask = np.invert(mask)

    v[mask] = 0

    converted = cv2.merge([h,s,v])

    cvutil.display_image(cv2.cvtColor(converted, cv2.COLOR_HSV2BGR))



def main() :
    dset = dataset.dataset('data/basil/front')

    for i in dset :
        converted = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(converted)
        mask = (h > 45) & (h < 90)
        mask = np.invert(mask)
        v[mask] = 0
        converted = cv2.merge([h,s,v])

        i[...] = cv2.cvtColor(converted, cv2.COLOR_HSV2BGR)


    dset.write_images('colorf')

main()
