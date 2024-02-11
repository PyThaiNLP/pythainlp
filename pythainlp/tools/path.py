# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
PyThaiNLP data tools

For text processing and text conversion, see pythainlp.util
"""
import os

from pythainlp import __file__ as pythainlp_file

PYTHAINLP_DEFAULT_DATA_DIR = "pythainlp-data"


def get_full_data_path(path: str) -> str:
    """
    This function joins path of :mod:`pythainlp` data directory and the
    given path, and returns the full path.

    :return: full path given the name of dataset
    :rtype: str

    :Example:
    ::

        from pythainlp.tools import get_full_data_path

        get_full_data_path('ttc_freq.txt')
        # output: '/root/pythainlp-data/ttc_freq.txt'
    """
    return os.path.join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path() -> str:
    """
    Returns the full path where PyThaiNLP keeps its (downloaded) data.
    If the directory does not yet exist, it will be created.
    The path can be specified through the environment variable
    :envvar:`PYTHAINLP_DATA_DIR`. By default, `~/pythainlp-data`
    will be used.

    :return: full path of directory for :mod:`pythainlp` downloaded data
    :rtype: str

    :Example:
    ::

        from pythainlp.tools import get_pythainlp_data_path

        get_pythainlp_data_path()
        # output: '/root/pythainlp-data'
    """
    pythainlp_data_dir = os.getenv(
        "PYTHAINLP_DATA_DIR", os.path.join("~", PYTHAINLP_DEFAULT_DATA_DIR)
    )
    path = os.path.expanduser(pythainlp_data_dir)
    os.makedirs(path, exist_ok=True)
    return path


def get_pythainlp_path() -> str:
    """
    This function returns full path of PyThaiNLP codes

    :return: full path of :mod:`pythainlp` codes
    :rtype: str

    :Example:
    ::

        from pythainlp.tools import get_pythainlp_path

        get_pythainlp_path()
        # output: '/usr/local/lib/python3.6/dist-packages/pythainlp'
    """
    return os.path.dirname(pythainlp_file)
