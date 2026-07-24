import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in current_app.config["ALLOWED_EXTENSIONS"]


def save_image(file):

    if file is None:
        return None

    if file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    extension = file.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4()}.{extension}"

    filename = secure_filename(filename)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    return filename