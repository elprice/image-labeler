import os

from flask import Flask, jsonify, render_template, url_for

app = Flask(__name__)

IMAGE_DIR = "images"


@app.route("/")
def index():
    images = [
        f
        for f in os.listdir(os.path.join(app.static_folder, "images"))
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]
    print(images)
    url_for("static", filename=f"{IMAGE_DIR}/{images[0]}")
    url_for("static", filename=f"{IMAGE_DIR}/{images[1]}")

    url_for("static", filename=f"{IMAGE_DIR}/{images[2]}")

    image_urls = [url_for("static", filename=f"{IMAGE_DIR}/{f}") for f in images]
    return render_template("index.html", image_urls=image_urls)


@app.route("/get_image_info/<image_name>")
def get_image_info(image_name):
    image_info = {
        "name": image_name,
        "size": os.path.getsize(os.path.join(IMAGE_DIR, image_name)),
    }
    return jsonify(image_info)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
