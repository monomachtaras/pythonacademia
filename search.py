from PIL import Image
import imagehash
import argparse
import shelve

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--difference", required=True, help="difference beetween images")
ap.add_argument("-s", "--shelve", required=True, help="output shelve database")
ap.add_argument("-q", "--query", required=True, help="path to the query image")
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"])
query = Image.open(args["query"])
difference = int(args["difference"])


h = imagehash.dhash(query)

# loop over the images
for key in db.keys():
    if key - h < difference:
        print db[key]

# close the shelve database
db.close()
