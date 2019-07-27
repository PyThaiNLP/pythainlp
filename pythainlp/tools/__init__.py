# -*- coding: utf-8 -*-
"""
PyThaiNLP data tools

For text processing and text conversion, see pythainlp.util
"""
import os

import pythainlp

PYTHAINLP_DATA_DIR = "pythainlp-data"


def get_full_data_path(path: str) -> str:
    """
    Get filename/path of a dataset, return full path of that filename/path
    """
    return os.path.join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path() -> str:
    """
    Return full path where PyThaiNLP keeps its (downloaded) data
    """
    path = os.getenv('PYTHAINLP_DATA_DIR',
                     os.path.join("~", PYTHAINLP_DATA_DIR))
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_pythainlp_path() -> str:
    """
    Return full path of PyThaiNLP code
    """
    return os.path.dirname(pythainlp.__file__)
