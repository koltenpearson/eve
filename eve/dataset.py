import os
import re
from datetime import datetime
import cv2
import numpy as np
import sys

def print_status_bar(current, total, size=100) :

    ratio = current / total
    amount = int(ratio * size)

    bar = '-' * size
    completed = '|' * amount
    sys.stdout.write('\r' + bar + '\r' + completed)



class vidset :

    def __init__(self, filename, fourcc=False) :
        self.filename = filename
        if fourcc :
            self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        else :
            self.fourcc = cv2.VideoWriter_fourcc(*'FFV1') 
        self.camera_in = cv2.VideoCapture(self.filename)
        self.index = 0

    def __len__(self) :
        return int(self.camera_in.get(cv2.CAP_PROP_FRAME_COUNT))

    def __getitem__(self, key) :
        pos = self.camera_in.get(cv2.CAP_PROP_POS_FRAMES)
        self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, key)
        result = self.camera_in.read()[1]
        self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, pos)
        return result

    def time_slice(self, starttime, endtime, outfile, fps=30, verbose = False) :
        pos = self.camera_in.get(cv2.CAP_PROP_POS_FRAMES)
        self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, 0) 

        timestamp = self.camera_in.get(cv2.CAP_PROP_POS_MSEC) #in case it does not start at zero
        starttime = starttime * 1000 + timestamp  #convert from seconds
        endtime = endtime * 1000 + timestamp

        self.camera_in.set(cv2.CAP_PROP_POS_MSEC, starttime) #Get the indices of the frames from the timestamp
        start = self.camera_in.get(cv2.CAP_PROP_POS_FRAMES)
        self.camera_in.set(cv2.CAP_PROP_POS_MSEC, endtime)
        end = self.camera_in.get(cv2.CAP_PROP_POS_FRAMES)

        self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, pos)

        to_write = self.loop(None, outfile = outfile, fps = fps, start = start, end = end, verbose = verbose)

        while (to_write is not None) :
            to_write = self.loop(to_write, verbose=verbose)


    def tloop(self, array, outfile = "default", fps=30, verbose = False) : #TODO refractor
        if array is None :
            self.index = 1
            self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.camera_out = cv2.VideoWriter(outfile + '.avi', self.fourcc, fps, (self[0].shape[1], self[0].shape[0]))
            self.buffer = [self.camera_in.read()[1], self.camera_in.read()[1], self.camera_in.read[1]]
            return tuple(self.buffer)

        if self.index >= len(self) - 1 :
            del self.buffer
            return None

        self.camera_out.write(array)
        self.index += 1

        self.buffer.append(self.camera_in.read()[1])
        self.buffer.pop(0)

        if (verbose) :
            print_status_bar(self.index, len(self))
        return tuple(self.buffer)

    def loop(self, array, outfile = "default", fps=30, start=0, end=-1, verbose = False) :
        if array is None :
            self.index = start
            self.start = start
            if end == -1 :
                self.end = len(self)
            else :
                self.end = end
            self.camera_in.set(cv2.CAP_PROP_POS_FRAMES, start)
            self.camera_out = cv2.VideoWriter(outfile + '.avi', self.fourcc, fps, (self[0].shape[1], self[0].shape[0]))
            return self.camera_in.read()[1]

        if self.index >= self.end :
            del self.end
            return None

        self.camera_out.write(array)
        self.index += 1
        if (verbose) :
            print_status_bar(self.index - self.start, self.end - self.start)
        return self.camera_in.read()[1]


## careful about trying to make in place changes that then reflect on other in place changes with the buffered dataset.
# the cache is cleared every so often and retrieving it again will revert changes
# try to not need the intermediate things, or if you do to make intermediate datasets to handle it for now
class buffered_iterator :

    ##bufsize does not gaurentee that there will strictly be that many in the cache, rather that it will be cleared after that many iterations
    # feel free to snag elements like index to get the current index in the dset
    # set filename to none if you do not want to save it anywhere
    def __init__ (self, dset, filename, bufsize = 100, start=0, end_offset=0, video = False, fps=20.0, outtype=None) :
        self.dset = dset
        self.bufsize = bufsize
        self.bufcount = 0
        self.video = video
        self.index = start -1
        self.end = len(dset) - end_offset
        self.filename = filename
        self.outtype = outtype

        if (video) :
            fourcc = cv2.VideoWriter_fourcc(*'FFV1') #is there a better format? this will be avi
            self.camera = cv2.VideoWriter(filename + '.avi',fourcc, fps, (self.dset[0].shape[1], self.dset[0].shape[0]))



    def __iter__ (self) :
        return self

    def _flush(self) :
        if (self.filename and not self.video) :
            oldtype = self.dset.dtype
            if (self.outtype) :
                self.dset.set_dtype(self.outtype)
            self.dset.write_images(self.filename)

            self.dset.set_dtype(oldtype)

        self.dset._clear_cache()

    def __next__(self) :
        if (self.video) :
            self.camera.write(self.dset[self.index])

        self.index += 1
        self.bufcount += 1

        if (self.bufcount >= self.bufsize) :
            self._flush()
            self.bufcount = 0

        if (self.index >= self.end) :
            self._flush()
            raise StopIteration
            if (self.video) :
                self.camera.release()

        return self.dset[self.index]


class dataset :

    def __init__ (self, directory, file_format=r".png", date_format=r"%m-%d-%y_%H-%M-%S", dtype = np.uint8):

        self.directory = directory
        self.date_format=date_format
        self.file_format = file_format
        self._initialize_data()
        self.cache = {}
        self.dtype = dtype

    def _initialize_data(self) :
        self.data = []
        for f in os.listdir(self.directory) :
            f = re.match(r'(.*)\..*$', f).group(1) # take of file extension
            self.data.append(datetime.strptime(f, self.date_format)) #make a list of datetime objects, one for each picture

        self.data.sort()

    def __repr__(self) :
        return "<dataset object from '{}', {} - {}>".format(self.directory, self.data[0].strftime(self.date_format), self.data[-1].strftime(self.date_format))

    def set_dtype(self, dtype) :
        self.dtype = dtype

    def _clear_cache(self) :
        self.cache.clear()

    class dataset_iter :

        def __init__(self, dset) :
            self.dset = dset
            self.counter = 0

        def __iter__(self) :
            return self

        def __next__(self) :
            if self.counter >= len(self.dset) :
                raise StopIteration
            else :
                self.counter += 1
                return self.dset[self.counter - 1]

    def __iter__(self) :
        return self.dataset_iter(self)

    def __len__(self) :
        return len(self.data)

    ##you can either retreive it by sequential index, like a list 
    # or you can put in a string with the same format as it is saved in
    def __getitem__(self, key) : 
        if (type(key) == type(0)) :
            key = self.data[key]

        if not (key in self.cache) :
            self.cache[key] = self._get_array(key.strftime(self.date_format))

        if (self.cache[key].dtype != self.dtype) :
            self.cache[key] = self.cache[key].astype(self.dtype)

        return self.cache[key]

    def __setitem__(self, key, value) :
        if (type(key) == type(0)) :
            key = self.data[key]
        self.cache[key] = value


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


    ##will write out a video composed of all files in dataset as individual frames to given filename
    # \param fill, if true will use all files, otherwise will only put in modified files
    # defaults to True
    def write_video(self, filename, fill=True, fps=20.0) :
        to_write = []
        if fill :
            to_write = self.data
        else :
            to_write = list(self.cache.keys())
            to_write.sort()

        fourcc = cv2.VideoWriter_fourcc(*'XVID') #is there a better format? this will be avi
        camera = cv2.VideoWriter(filename + '.avi',fourcc, fps, (self[to_write[0]].shape[1], self[to_write[0]].shape[0]))

        for i in to_write :
            camera.write(self[i])

        camera.release()

        
