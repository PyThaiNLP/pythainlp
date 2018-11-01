# -*- coding: utf-8 -*-
"""
PyThaiNLP package installation and data tools
"""
import os
import subprocess
import sys

PYTHAINLP_DATA_DIR = "pythainlp-data"


def install_package(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


def get_path_data(filename):
    return os.path.join(get_path_pythainlp_data(), filename)


def get_path_pythainlp_data():
    path = os.path.join(os.path.expanduser("~"), PYTHAINLP_DATA_DIR)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
