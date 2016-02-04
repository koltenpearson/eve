from eve import dataset
from eve import cvutil
import numpy as np
import scipy.stats as stats

def pofconcept() :

    dset = dataset.dataset('data/basil/front')

    buffer = np.copy(dset[2])

    buffer -= dset[1]

    buffer2 = np.copy(dset[2])

    buffer2 = buffer2.astype(float)

    buffer2 -= dset[1]

    bmask = ((buffer2 > 0) & (buffer2 < 255))
    buffer2[bmask] = 0
    bmask = (buffer2 != 0)
    buffer2[bmask] = 255

    bmask = (buffer2[:,:,0] == 255) & (buffer2[:,:,1] == 255) & (buffer2[:,:,2] == 255)
    bmask = np.invert(bmask)
    buffer2[bmask] = 0

    cvutil.comp_images(buffer, buffer2.astype(np.uint8))


##this will modify whatever is passed into it
# \param a numpy image array like what opencv makes
#  it will set all values (0, 255) to zero, and all outside of that range to max
def threshold(im) :
    mask = ((im > -10) & (im < 10)) # this creates an numpy array of the same shape as boolean values
    im[mask] = 0

    mask = (im != 0)
    im[mask] = 255

    #mask = ((im[:,:,0] == 255) & (im[:,:,1] == 255) & (im[:,:,2] == 255)) #this will set any non white leftovers to black
    #mask = np.invert(mask)
    #im[mask] = 0


def main() :

    dset = dataset.dataset('data/basil/front')

    for i in range(len(dset) - 1, 0, -1) :

        dset[i] = dset[i].astype(float)

        dset[i] -= dset[i - 1]
        threshold(dset[i])
        
        dset[i] = dset[i].astype(np.uint8)

    cvutil.comp_images(dset[1], dset[2])

    dset.write_images('movement')


pofconcept()
main()

