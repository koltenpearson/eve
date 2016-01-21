import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
import numpy as np
import math
from . import cvutil
import random

def sample_random_points(array, m, n) :

    to_fill = np.zeros((m, n, 3))

    #I feel like there is a better way to do it but I guess not
    for x in range(m) :
        for y in range(n) :

            r1 = random.randint(0,array.shape[0] - 1)
            r2 = random.randint(0,array.shape[1] - 1)

            to_fill[x][y] = array[r1][r2]


    return to_fill

def number_to_hexcolor(r, g, b) :

    result = "#"

    for i in (r, g, b) :
        result += format(int(i), '02x')

    return result

def create_color_from_sample(array) :

    b,g,r = cv2.split(array)


    result = []
    for i in range(array.shape[0]) :
        for j in range(array.shape[1]) :
            result.append(number_to_hexcolor(r[i][j], g[i][j], b[i][j]))


    return result


def main() :

    image_name="ch82.jpg"

    image = cv2.imread(image_name)

    sample = sample_random_points(image, 100, 100) 

    fig = plt.figure()
    ax = fig.add_subplot(1,2,1,projection="3d")

    b,g,r = cv2.split(sample)

    x, y = (b,g)

    z = r

    ax.set_xlabel('blue')
    ax.set_ylabel('green')
    ax.set_zlabel('red')

    ax.scatter(x,y,z, linewidth=0, c=create_color_from_sample(sample))

    ax2 = fig.add_subplot(1,2,2)
    ax2.imshow(image[:,:,::-1], interpolation='bicubic')
    #ax2.xticks([])
    #ax2.yticks([])

    plt.show()
    



main()
