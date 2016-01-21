##This is a dataset object
# it is a wrapper around a folder of image files
# it will facilite converting them to and from numpy arrays
# it will also allow operatoins on the file set at a time

import os
import re
from datetime import datetime
import cv2
import numpy as np


class dataset :

    def __init__ (self, directory, file_format=r".png", date_format=r"%m-%d-%y_%H-%M-%S"):

        self.directory = directory
        self.date_format=date_format
        self.file_format = file_format
        self._initialize_data()

    def _initialize_data(self) :
        self.data = []
        for f in os.listdir(self.directory) :
            f = re.match(r'(.*)\..*$', f).group(1) # take of file extension
            self.data.append(datetime.strptime(f, self.date_format)) #make a list of datetime objects, one for each picture

        self.data.sort()

    def __repr__(self) :
        return "<dataset object from '{}', {} - {}>".format(self.directory, self.data[0].strftime(self.date_format), self.data[-1].strftime(self.date_format))


    def __len__(self) :
        return len(self.data)

    ##you can either retreive it by sequential index, like a list 
    # or you can put in a string with the same format as it is saved in
    def __getitem__(self, key) : 

        if (type(key) == type(0)) :
            return self._get_array(self.data[key].strftime(self.date_format))

        else :
            return self._get_array(key)


    ##helper function gets the numpy array
    def _get_array(self, filename) :

        return cv2.imread(os.path.join(self.directory, filename + self.file_format))
