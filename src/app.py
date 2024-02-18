import base64
import logging
import os

from flask import Flask, jsonify, render_template, url_for, request

app = Flask(__name__)

# Define the path to your image directory
IMAGE_DIR = "images"


@app.route("/", defaults={"image": None})
def index(image):
    image = request.args.get('image')
    # Get a list of image filenames
    # images_path = os.path.join(os.getcwd(), IMAGE_DIR)
    # images = [
    #    url_for("static", filename=f"{IMAGE_DIR}/{f}")
    #    for f in os.listdir(os.path.join(app.static_folder, "images"))
    #    if f.endswith((".jpg", ".png", ".jpeg"))
    # ]
    # print(images)
    data = {}
    logging.error(image)
    images = [
        f
        for f in os.listdir(os.path.join(app.static_folder, "images"))
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]
    image_urls = [url_for("static", filename=f"{IMAGE_DIR}/{f}") for f in images]
    if not image:
        f = open(f"S:\image-viewer\src\static\images\images.jpg", "rb").read()
        b = bytearray(f)

        base64_encoded_image = base64.b64encode(b).decode("utf-8")
        data["current"] = base64_encoded_image
        data["next"] = image_urls[1]
    else:
        logging.info(images)
        idx = images.index(image)
        f = open(f"S:\image-viewer\src\static\images\{image}", "rb").read()
        b = bytearray(f)

        base64_encoded_image = base64.b64encode(b).decode("utf-8")
        data["current"] = base64_encoded_image
        if idx - 1 >= 0:
            data["prev"] = image_urls[idx - 1]
        if idx + 1 < len(images):
            data["next"] = image_urls[idx + 1]

    return render_template("index.html", data=data)


@app.route("/get_image_info/<image_name>")
def get_image_info(image_name):
    # Get image information (optional)
    # You can extract dimensions, size, etc. here
    image_info = {
        "name": image_name,
        "size": os.path.getsize(os.path.join(IMAGE_DIR, image_name)),
    }
    return jsonify(image_info)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
