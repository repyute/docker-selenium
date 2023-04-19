ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
