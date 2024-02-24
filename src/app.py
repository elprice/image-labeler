import json
import os

from flask import Flask, jsonify, render_template, url_for

app = Flask(__name__)

IMAGE_DIR = "images"
RESOURCE_DIR = "resource"

LABELS_FILENAME = "labels.json"


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
    data["labels"] = get_labels(image_urls)
    return render_template("index.html", data=data)


@app.route("/update-labels")
def update_labels():
    pass


def get_labels(image_urls):
    with app.open_resource(f"{RESOURCE_DIR}/{LABELS_FILENAME}") as f:
        labels = json.loads(f.read())
        labels["images"] = labels.get("images", {})
        for url in image_urls:
            labels["images"][url] = labels["images"].get(url, labels["types"][0])

        print(labels)
    return labels


@app.route("/get_image_info/<image_name>")
def get_image_info(image_name):
    image_info = {
        "name": image_name,
        "size": os.path.getsize(os.path.join(IMAGE_DIR, image_name)),
    }
    return jsonify(image_info)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
