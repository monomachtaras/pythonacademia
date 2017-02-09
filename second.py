from PIL import Image
import imagehash
import argparse
import shelve
import glob

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to images")
ap.add_argument("-s", "--shelve", required=True, help="path to shelve database")
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"], writeback=True)

for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # load the image and compute the difference hash
    image = Image.open(imagePath)
    h = imagehash.dhash(image)

    filename = imagePath[imagePath.rfind("/") + 1:]
    db[h] = db.get(h, []) + [filename]
db.close()
