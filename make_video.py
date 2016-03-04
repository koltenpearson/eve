from eve import dataset
import os

source_root = os.path.join("data","current", "basil")

sources = ["front", "side", "top"]

dest = "data"

dest_prefix = "vid_"

def main() :
    
    for s in sources :

        print("starting " + s)
        dset = dataset.dataset(os.path.join(source_root, s))
        final_dest = os.path.join(dest, dest_prefix + s)

        for f in dataset.buffered_iterator(dset, final_dest, video=True, fps=40) :
            pass

        print("finished " + s)

main()
