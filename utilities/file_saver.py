import os
import imghdr
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ['jpg', 'gif', 'jpeg', 'png']


def validate_image(stream):
    """
    Reads the first 512 bytes from the input stream and attempts to determine
    the image format
    Returns a file extension based on the detected format
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return format


def is_allowed_file(image_file):
    filename = image_file.filename
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
        # Check if the extension is allowed or image is valid
        if extension in ALLOWED_EXTENSIONS or \
                extension == validate_image(image_file.stream):
            return True
        print("Level 2")
        return False
    print("Level 3")
    return False


def save_image(image_file, folder = None):
    if image_file and folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = secure_filename(image_file.filename)
        image_path = os.path.join(folder, filename)
        image_file.save(image_path)

        return image_path

    return None
