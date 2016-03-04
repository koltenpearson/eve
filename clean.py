import numpy as np
from eve import dataset
from eve import cvutil



static_bin = set()

class blob :

    @classmethod
    def create_if_valid(class_ref, x, y, image) :

        if (x,y) in static_bin :
            return None
        else :
            return blob(x, y, image)

    def __init__(self, x, y, image) :
        self.x = x
        self.y = y
        self.bin = set()
        self.image = image 
        self.ran = False

        self._add_point(self.x, self.y)

    def __len__(self) :
        return len(self.bin)
        
    def run (self) :
        if not self.ran :
            self._rec_run(self.x, self.y)
            return True
        else :
            return False

    def bounds_condition(self, x, y) :
        try :
            if (self.image[x, y, 0] != 255) :
                return True
            else :
                return False

        except IndexError :
            return False

    def _add_point(self, x, y) :
        self.bin.add((x,y))
        static_bin.add((x,y))

    def _rec_run(self, x, y) :
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :

                if (dx, dy) == (0,0) : #we do not need to check the current point
                    continue

                if (self.bounds_condition(x + dx, y + dy) and (x + dx, y + dy) not in self.bin) :
                    self._add_point(x + dx, y + dy)
                    self._rec_run(x + dx, y + dy)

    def set_blob(self, value) :
        for p in self.bin :
            self.image[p[0], p[1], 0] = value


def poc() :

    image = dataset.dataset('edge')[1]


    blobs = []

    for i in range(image.shape[0]) :
        for j in range(image.shape[1]) :
            if (image[i,j,0] == 0) :
                buf = blob.create_if_valid(i, j, image)

                if (buf != None) :
                    buf.run()
                    blobs.append(buf)


    for b in blobs :
        b.set_blob(255)

    cvutil.display_image(image)



poc()
