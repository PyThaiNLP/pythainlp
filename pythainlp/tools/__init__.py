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
        This function joins path of :mod:`pythainlp` data directory and the
        given path, and returns the full path.

        :return: full path given the name of dataset
        :rtype: str

        :Example:

            >>> from pythainlp.tools import get_full_data_path
            >>>
            >>> get_full_data_path('ttc_freq.txt')
            '/root/pythainlp-data/ttc_freq.txt'
    """
    return os.path.join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path() -> str:
    """
        This function returns full path where PyThaiNLP keeps its
        (downloaded) data

        :return: full path of directory for :mod:`pythainlp` downloaded data
        :rtype: str

        :Example:

            >>> from pythainlp.tools import get_pythainlp_data_path
            >>>
            >>> get_pythainlp_data_path()
            '/root/pythainlp-data'
    """
    path = os.getenv('PYTHAINLP_DATA_DIR',
                     os.path.join("~", PYTHAINLP_DATA_DIR))
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_pythainlp_path() -> str:
    """
        This function returns full path of PyThaiNLP code

        :return: full path of :mod:`pythainlp` code
        :rtype: str

        :Example:

            >>> from pythainlp.tools import get_pythainlp_path
            >>>
            >>> get_pythainlp_path()
            '/usr/local/lib/python3.6/dist-packages/pythainlp'
    """
    return os.path.dirname(pythainlp.__file__)
