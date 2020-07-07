# import the necessary packages
import argparse

import cv2
import numpy as np

from polydomino.colordescriptor import ColorDescriptor
from polydomino.searcher import Searcher

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i",
    "--index",
    required=True,
    help="Path to where the computed index will be stored",
)
ap.add_argument("-q", "--query", required=True, help="Path to the query image")
ap.add_argument(
    "-fm", "--features", required=True, help="Method to get features of pics",
)
ap.add_argument(
    "-sm", "--searcher", required=True, help="Method to search pics",
)
# ap.add_argument("-r", "--result-path", required=True, help="Path to the result path")
args = vars(ap.parse_args())
# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))
# load the query image and describe it
query = cv2.imread(args["query"])
if args["features"] == "color-moments":
    features = cd.color_moments(query)
elif args["features"] == "hsv-describe":
    features = cd.hsv_describe(query)
elif args["features"] == "gray-matrix":
    features = cd.gray_matrix(query)
elif args["features"] == "humoments":
    features = cd.humoments(query)
elif args["features"] == "dhash":
    features = cd.dhash(query)
else:
    print("Sorry, we don't support this method.")
    exit(1)
# perform the search
method = args["searcher"]
searcher = Searcher(args["index"])
results = searcher.search(features, method)
print(results)
# display the query
cv2.namedWindow("Query", 0)
cv2.resizeWindow("Query", 640, 480)
cv2.imshow("Query", query)
# loop over the results
ans = []
for (score, resultID) in results:
    result = cv2.imread(resultID)
    cv2.imshow("Result", result)
    cv2.waitKey(0)
