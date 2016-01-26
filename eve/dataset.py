##This is a dataset object
# it is a wrapper around a folder of image files
# it will facilite converting them to and from numpy arrays
# it will also allow operatoins on the file set at a time

import os
import re
from datetime import datetime
import cv2
import numpy as np

#TODO maybe add cacheing, seems like it would be a good idea, speed up a lot of operations
# in fact it will be necessary, I think. so I will add it next


class dataset :

    def __init__ (self, directory, file_format=r".png", date_format=r"%m-%d-%y_%H-%M-%S"):

        self.directory = directory
        self.date_format=date_format
        self.file_format = file_format
        self._initialize_data()
        self.cache = {}

    def _initialize_data(self) :
        self.data = []
        for f in os.listdir(self.directory) :
            f = re.match(r'(.*)\..*$', f).group(1) # take of file extension
            self.data.append(datetime.strptime(f, self.date_format)) #make a list of datetime objects, one for each picture

        self.data.sort()

    def __repr__(self) :
        return "<dataset object from '{}', {} - {}>".format(self.directory, self.data[0].strftime(self.date_format), self.data[-1].strftime(self.date_format))

    class dataset_iter :

        def __init__(self, dset) :
            self.dset = dset
            self.counter = 0

        def __iter__(self) :
            return self

        def next(self) :
            if self.counter >= len(self.dset) :
                raise StopIteration
            else :
                self.counter += 1
                return self.dset[self.counter - 1]

    def __iter__(self) :
        return dataset_iter(self)

    def __len__(self) :
        return len(self.data)

    ##you can either retreive it by sequential index, like a list 
    # or you can put in a string with the same format as it is saved in
    def __getitem__(self, key) : 
        if (type(key) == type(0)) :
            key = self.data[key]

        if not (key in self.cache) :
            self.cache[key] = self._get_array(key.strftime(self.date_format))
        return self.cache[key]


    ##helper function gets the numpy array from a file
    def _get_array(self, filename) :
        return cv2.imread(os.path.join(self.directory, filename + self.file_format))

    ##will write out all images with the modifications made to a new directory
    # will create the directory if it does not exist
    # will overwrite images of the same name that it finds there
    # \param fill, if set to false, will only write images that have been modified, otherwise will also copy over unmodified images
    # defaults to false
    def write_images(self, directory, fill = False) :
        to_write = []
        os.makedirs(directory, exist_ok =True)

        if fill :
            to_write = self.data
        else :
            to_write = list(self.cache.keys())
            to_write.sort()

        for i in to_write :
            cv2.imwrite(os.path.join(directory, i.strftime(self.date_format) + self.file_format), self[i])

