# -*- coding: utf-8 -*-
"""
PyThaiNLP package installation and data tools
"""
import os
import subprocess
import sys
import pythainlp

PYTHAINLP_DATA_DIR = "pythainlp-data"


def install_package(package):
    """
    Install package using pip
    Use with caution.
    User may not like their system to be installed with a package they don't explicitly known about.
    """
    subprocess.call([sys.executable, "-m", "pip", "install", package])


def get_full_data_path(path):
    """
    Get filename/path of a dataset, return full path of that filename/path
    """
    return os.path.join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path():
    """
    Return full path where PyThaiNLP keeps its (downloaded) data
    """
    path = os.path.join(os.path.expanduser("~"), PYTHAINLP_DATA_DIR)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_pythainlp_path():
    """
    Return full path of PyThaiNLP code
    """
    return os.path.dirname(pythainlp.__file__)
