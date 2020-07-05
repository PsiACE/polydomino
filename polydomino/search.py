# import the necessary packages
from polydomino.colordescriptor import ColorDescriptor
from polydomino.searcher import Searcher
import argparse
import numpy as np
import cv2


def show_in_one(images, show_size=(1980, 1080), blank_size=2, window_name="merge"):
    small_h, small_w = images[0].shape[:2]
    column = int(show_size[1] / (small_w + blank_size))
    row = int(show_size[0] / (small_h + blank_size))
    shape = [show_size[0], show_size[1]]
    for i in range(2, len(images[0].shape)):
        shape.append(images[0].shape[i])

    merge_img = np.zeros(tuple(shape), images[0].dtype)

    max_count = len(images)
    count = 0
    for i in range(row):
        if count >= max_count:
            break
        for j in range(column):
            if count < max_count:
                im = images[count]
                t_h_start = i * (small_h + blank_size)
                t_w_start = j * (small_w + blank_size)
                t_h_end = t_h_start + im.shape[0]
                t_w_end = t_w_start + im.shape[1]
                merge_img[t_h_start:t_h_end, t_w_start:t_w_end] = im
                count = count + 1
            else:
                break
    if count < max_count:
        print("图片总数为： %s" % (max_count - count))
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, merge_img)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i",
    "--index",
    required=True,
    help="Path to where the computed index will be stored",
)
ap.add_argument("-q", "--query", required=True, help="Path to the query image")
# ap.add_argument("-r", "--result-path", required=True, help="Path to the result path")
args = vars(ap.parse_args())
# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))
# load the query image and describe it
query = cv2.imread(args["query"])
features = cd.describe(query)
# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)
print(results)
# display the query
cv2.namedWindow("Query", 0)
cv2.resizeWindow("Query", 640, 480)
cv2.imshow("Query", query)
# loop over the results
ans = []
for (score, resultID) in results:
    ans.append(cv2.imread(resultID))

show_in_one(ans)
cv2.waitKey(0)
