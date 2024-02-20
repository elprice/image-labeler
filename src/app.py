import json
import logging
import os

from flask import Flask, jsonify, render_template, url_for

app = Flask(__name__)

IMAGE_DIR = "images"
RESOURCE_DIR = "resource"


@app.route("/")
def index():
    data = {}
    images = [
        f
        for f in os.listdir(os.path.join(app.static_folder, "images"))
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]
    image_urls = [url_for("static", filename=f"{IMAGE_DIR}/{f}") for f in images]
    data["image_urls"] = image_urls
    data["categories"] = categories()
    return render_template("index.html", data=data)


@app.route("/get-categories")
def categories():
    # TODO needs to select the one that has been set in file.. not first in html
    with app.open_resource(f"{RESOURCE_DIR}/categories.json") as f:
        categories = json.loads(f.read())
        # logging.info(categories)
    return categories


@app.route("/get_image_info/<image_name>")
def get_image_info(image_name):
    image_info = {
        "name": image_name,
        "size": os.path.getsize(os.path.join(IMAGE_DIR, image_name)),
    }
    return jsonify(image_info)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
