import os
import sys
import time
from datetime import timedelta

import cv2
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from colordescriptor import ColorDescriptor
from searcher import Searcher

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(["png", "jpg", "JPG", "PNG", "bmp"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), "index.csv")


# main route
@app.route("/")
def index():
    return render_template("index.html")


# search route
@app.route("/search", methods=["POST"])
def search():

    if request.method == "POST":

        RESULTS_ARRAY = []

        # get url
        image_url = request.form.get("img")

        try:
            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))

            import cv2

            image_url = "polydomino/" + image_url[1:]
            query = cv2.imread(image_url)
            features = cd.hsv_describe(query)

            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features)

            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append({"image": str(resultID), "score": str(score)})

            # return success
            return jsonify(results=(RESULTS_ARRAY[:5]))

        except:

            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
