from PIL import Image
from pillow_heif import register_heif_opener
from flask import Flask, request, send_file
from flask_cors import CORS
import os
import io
import zipfile

app = Flask(__name__)
CORS(app)
register_heif_opener()


def heic_to_jpg(heic_file):
    heic_img = Image.open(heic_file)

    # Convert to RGB
    rgb_image = heic_img.convert("RGB")

    # Save as JPEG to a byte IO
    jpg_io = io.BytesIO()
    rgb_image.save(jpg_io, "JPEG")

    jpg_io.seek(0)
    return jpg_io


# HANDLE MULTIPLE
@app.route("/upload", methods=['POST'])
def upload_files():
    heic_files = request.files.getlist('files')
    jpg_files = []

    for heic_file in heic_files:
        img_name = os.path.splitext(heic_file.filename)[0]
        img_io = heic_to_jpg(heic_file)
        jpg_files.append((img_name + ".jpg", img_io))

    zip_buff = io.BytesIO()
    with zipfile.ZipFile(zip_buff, 'w') as zip_file:
        for jpg_name, jpg_io in jpg_files:
            zip_file.writestr(jpg_name, jpg_io.getvalue())

    zip_buff.seek(0)
    return send_file(zip_buff, mimetype='application/zip', as_attachment=True, download_name="pics.zip")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5100)
