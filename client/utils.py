import os


def get_image_path(file_name, folder_name="./img"):
    return os.path.join(folder_name, file_name)
