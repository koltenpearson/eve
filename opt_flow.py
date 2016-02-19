from eve import dataset
import cv2
from eve import cvutil
import numpy as np

def dense_optical_flow() :
    dset = dataset.dataset('data/basil/front')

    prev = cv2.cvtColor(dset[1],cv2.COLOR_BGR2GRAY)
    canvas = np.zeros_like(dset[1])

    canvas[...,1] = 255

    for i in range(2, len(dset)) :
        next = cv2.cvtColor(dset[i], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev, next, flow=None, pyr_scale=0.5,levels= 3, winsize=15, iterations=2, poly_n=5, poly_sigma=1.1, flags=0)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

        canvas[...,0]  = ang * 180/np.pi/2
        canvas[...,2] = cv2.normalize(mag, None, 0, 255,cv2.NORM_MINMAX)

        prev = np.copy(next)
        dset[i] = cv2.cvtColor(np.copy(canvas), cv2.COLOR_HSV2BGR)


    dset.write_images('denseflow')



def sparse_optical_flow() :
    dset = dataset.dataset('data/basil/front')

    tracking = cv2.goodFeaturesToTrack(cv2.cvtColor(dset[1], cv2.COLOR_BGR2GRAY), maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7)

    old = None

    for d in range(2,len(dset)) :

        very_old = old

        old = np.copy(tracking)

        tracking, status, error = cv2.calcOpticalFlowPyrLK(cv2.cvtColor(dset[d - 1],cv2.COLOR_BGR2GRAY), cv2.cvtColor(dset[d], cv2.COLOR_BGR2GRAY), old, None, winSize=(15,15), maxLevel= 2)

        for i in range(old.shape[0]) :

            for j in range(old.shape[1]) :

                if (very_old != None) :
                    cv2.line(dset[d-1], (very_old[i][j][0], very_old[i][j][1]), (old[i][j][0], old[i][j][1]), (0,0,255), thickness=4)

                cv2.circle(dset[d-1], (old[i][j][0], old[i][j][1]), 4, (255,0,0), thickness=-1)


    dset.write_images('optflowbw')



def poc() :
    dset = dataset.dataset('data/basil/front')

    display = np.copy(dset[-1])

    tracking = cv2.goodFeaturesToTrack(cv2.cvtColor(dset[1], cv2.COLOR_BGR2GRAY), maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7)

    old = tracking


    for i in range(2,len(dset)) :
        result, status, error = cv2.calcOpticalFlowPyrLK(dset[i - 1], dset[i], old, None, winSize=(15,15), maxLevel= 2)
        old = result

        for i in range(tracking.shape[0]) :

            for j in range(tracking.shape[1]) :

                cv2.circle(display, (old[i][j][0], old[i][j][1]), 4, (0,0,255))


    cvutil.display_image(display)


    #for i in range(tracking.shape[0]) :

    #    for j in range(tracking.shape[1]) :

    #        cv2.circle(dset[1], (tracking[i][j][0], tracking[i][j][1]), 10, (255,0,0))


    #for i in range(old.shape[0]) :

    #    for j in range(old.shape[1]) :

    #        cv2.circle(dset[-1], (old[i][j][0], old[i][j][1]), 10, (255,0,0))

    #cvutil.comp_images(dset[1], dset[-1])

def poc_dense() :

    dset = dataset.dataset('data/basil/front')
    first = cv2.cvtColor(dset[1],cv2.COLOR_BGR2GRAY, dstCn=1)
    last = cv2.cvtColor(dset[2], cv2.COLOR_BGR2GRAY, dstCn=1)

    canvas = np.zeros_like(dset[1])

    canvas[...,1] = 255

    flow = cv2.calcOpticalFlowFarneback(first,last ,flow=None, pyr_scale=0.5,levels= 3, winsize=15, iterations=2, poly_n=5, poly_sigma=1.1, flags=0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

    canvas[...,0]  = ang * 180/np.pi/2
    canvas[...,2] = cv2.normalize(mag, None, 0, 255,cv2.NORM_MINMAX)

    print(canvas)
    cvutil.display_image(cv2.cvtColor(canvas, cv2.COLOR_HSV2BGR))
    


dense_optical_flow()
