import logging
import os
import shutil


def create_handler_log_file(log_file, /):
    file_handler = logging.FileHandler(log_file, "w", "utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)7s | %(message)s", datefmt="%H:%M:%S"))
    logging.getLogger(__name__).addHandler(file_handler)
    return file_handler


def create_folder(path, /):
    if os.path.exists(path):
        return
    os.makedirs(path)


def delete_folder(path, /):
    # remove directory and all its content
    if os.path.isdir(path):
        shutil.rmtree(path)


def create_file(file_path):
    open(file_path, 'w')


def delete_file(path):
    # check if file or directory exists
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove file
