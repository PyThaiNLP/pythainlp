# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""PyThaiNLP data tools

For text processing and text conversion, see pythainlp.util
"""

from __future__ import annotations

import os
from os import PathLike
from sys import version_info
from typing import cast

if version_info >= (3, 11):
    from importlib.resources import files  # Available in Python 3.11+
else:
    from importlib_resources import files  # type: ignore[import-not-found,no-redef]  # noqa: I001

PYTHAINLP_DEFAULT_DATA_DIR: str = "pythainlp-data"


def get_full_data_path(path: str) -> str:
    """This function joins path of :mod:`pythainlp` data directory and the
    given path, and returns the full path.

    :return: full path given the name of dataset
    :rtype: str

    :Example:
    ::

        from pythainlp.tools import get_full_data_path

        get_full_data_path("ttc_freq.txt")
        # output: '/root/pythainlp-data/ttc_freq.txt'
    """
    return os.path.join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path() -> str:
    """Returns the full path where PyThaiNLP keeps its (downloaded) data.
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
    """This function returns full path of PyThaiNLP codes.

    Note: When the package is installed as a zip file, the returned path
    may not be a standard filesystem path and should not be used for direct
    file I/O operations. Use importlib.resources for accessing package files
    in a zip-safe manner.

    :return: full path of :mod:`pythainlp` codes
    :rtype: str

    :Example:
    ::

        from pythainlp.tools import get_pythainlp_path

        get_pythainlp_path()
        # output: '/usr/local/lib/python3.6/dist-packages/pythainlp'
    """
    package_path = files("pythainlp")
    # For compatibility, convert to string path if possible
    # This works for both regular installations and zip files
    if hasattr(package_path, "__fspath__"):
        return os.fspath(cast(PathLike[str], package_path))
    # Fallback for traversable objects that don't support __fspath__
    return str(package_path)
