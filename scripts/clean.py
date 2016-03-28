import numpy as np
import random
from eve.blob import trace
from eve import dataset
from eve import cvutil

def gen_bound_checker(image) :

    def bound_checker(x, y) :
        if x >= image.shape[1] or x < 0 or y >= image.shape[0] or y < 0 :
            return True
        elif image[y][x][0] == 255 :
            return True
        else :
            return False

    return bound_checker

def poc() :

    image = dataset.dataset('edge')[2]
    orig = np.copy(image)
    checker = gen_bound_checker(image)

    traces = []

    cvutil.display_image(image)

    for y in range(image.shape[0]) :
        for x in range(image.shape[1]) :
            if not (checker(x, y) or trace.in_any_traces(x, y)) :
                t = trace(x, y, checker)
                t.trace_bounds()
                t.fill_bounds()
                traces.append(t)
                dataset.print_status_bar(y * image.shape[1] + x, image.shape[0] * image.shape[1])

    print('\n coloring')
    for i,t in enumerate(traces) :
        if len(t) < 50 :
            for p in t.points :
                image[p.y][p.x][0] = 200
                image[p.y][p.x][1] = 200
                image[p.y][p.x][2] = 200
        else :
            randcolor = (random.choice(range(255)),random.choice(range(255)),random.choice(range(255)))
            for p in t.points :
                image[p.y][p.x][0] = randcolor[0]
                image[p.y][p.x][1] = randcolor[1]
                image[p.y][p.x][2] = randcolor[2]
            image[t.init_p.y][t.init_p.x][0] = 0
            image[t.init_p.y][t.init_p.x][1] = 0
            image[t.init_p.y][t.init_p.x][2] = 255
        dataset.print_status_bar(i, len(traces))

    cvutil.comp_images(orig, image)
    
poc()
