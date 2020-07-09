import os
import sys
import time
from datetime import timedelta

import cv2
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from colordescriptor import ColorDescriptor
from searcher import Searcher

load_dotenv(find_dotenv())

INDEX_PATH = os.environ.get("INDEX_PATH")
FEATURES = os.environ.get("FEATURES")
SEARCHER = os.environ.get("SEARCHER")

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(["png", "jpg", "JPG", "PNG", "bmp"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


# create flask instance
app = Flask(__name__)
app.jinja_env.filters["zip"] = zip

INDEX = os.path.join(os.path.dirname(__file__), INDEX_PATH)


# main route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    return render_template("demo.html")


@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        f = request.files["file"]

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path = os.path.join(
            basepath, "static/queries", secure_filename(f.filename)
        )
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        import cv2

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, "static/queries", "test.jpg"), img)

        RESULTS_ARRAY = []
        SCORE_ARRAY = []
        cd = ColorDescriptor((8, 12, 3))
        features = get_features(cd, FEATURES, img)
        searcher = Searcher(INDEX)
        results = searcher.search(features, SEARCHER)
        # loop over the results, displaying the score and image name
        for (score, resultID) in results:
            RESULTS_ARRAY.append(resultID)
            SCORE_ARRAY.append(score)

        return render_template(
            "query_ok.html",
            results=(RESULTS_ARRAY[:5]),
            scores=(SCORE_ARRAY[:5]),
            name=f.filename,
        )

    return render_template("query.html")


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
            features = get_features(cd, FEATURES, query)

            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features, SEARCHER)

            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append({"image": str(resultID), "score": str(score)})

            # return success
            return jsonify(results=(RESULTS_ARRAY[:5]))

        except:

            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


def get_features(cd, method, query):
    if method == "color-moments":
        return cd.color_moments(query)
    elif method == "hsv-describe":
        return cd.hsv_describe(query)
    elif method == "gray-matrix":
        return cd.gray_matrix(query)
    elif method == "humoments":
        return cd.humoments(query)
    elif method == "ahash":
        return cd.ahash(query)
    elif method == "phash":
        return cd.phash(query)
    elif method == "mse":
        return cd.mse(query)
    elif method == "dhash":
        return cd.dhash(query)
    elif method == "hog":
        return cd.hog(query)
    else:
        return


# run!
if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
