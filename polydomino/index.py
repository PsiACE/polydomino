# import the necessary packages
import argparse
import glob

import cv2

from polydomino.colordescriptor import ColorDescriptor

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-d",
    "--dataset",
    required=True,
    help="Path to the directory that contains the images to be indexed",
)
ap.add_argument(
    "-i",
    "--index",
    required=True,
    help="Path to where the computed index will be stored",
)
ap.add_argument(
    "-m", "--method", required=True, help="Method to get features of pics",
)
args = vars(ap.parse_args())
# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))
# open the output index file for writing
output = open(args["index"], "w")
# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # extract the image ID (i.e. the unique filename) from the image
    # path and load the image itself
    # imageID = imagePath[imagePath.rfind("/") + 1 :]
    imageID = imagePath
    image = cv2.imread(imagePath)
    # describe the image
    if args["method"] == "color-moments":
        features = cd.color_moments(image)
    elif args["method"] == "hsv-describe":
        features = cd.hsv_describe(image)
    elif args["method"] == "gray-matrix":
        features = cd.gray_matrix(image)
    elif args["method"] == "humoments":
        features = cd.humoments(image)
    elif args["method"] == "ahash":
        features = cd.ahash(image)
    elif args["method"] == "phash":
        features = cd.phash(image)
    elif args["method"] == "dhash":
        features = cd.dhash(image)
    elif args["method"] == "mse":
        features = cd.mse(image)
    elif args["method"] == "hog":
        # img = cv2.resize(image,(192,192))
        features = cd.hog(image)
    else:
        print("Sorry, we don't support this method.")
        exit(1)
    # write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageID, ",".join(features)))
# close the index file
output.close()
