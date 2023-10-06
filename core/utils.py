import uuid


def get_filename(filename):
    name, ext = filename.split(".")

    return f"{name}-{uuid.uuid4()}.{ext}"
