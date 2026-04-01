# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""PyThaiNLP data tools

For text processing and text conversion, see pythainlp.util
"""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from os import PathLike

if sys.version_info >= (3, 11):
    from importlib.resources import files  # Available in Python 3.11+
else:
    from importlib_resources import files  # noqa: I001

PYTHAINLP_DEFAULT_DATA_DIR: str = "pythainlp-data"


def is_read_only_mode() -> bool:
    """Return whether PyThaiNLP is operating in read-only mode.

    Read-only mode prevents **implicit background writes** to PyThaiNLP's
    internal data directory — writes that happen as side effects the user
    may not be aware of. It is activated by setting the
    ``PYTHAINLP_READ_ONLY`` environment variable to a truthy value
    (e.g. ``"1"``).

    .. deprecated::
        ``PYTHAINLP_READ_MODE`` is deprecated.
        Use ``PYTHAINLP_READ_ONLY`` instead.
        Setting both variables at the same time raises :exc:`ValueError`.

    When read-only mode is active, the following implicit writes are blocked:

    - Creating the PyThaiNLP data directory
      (``~/pythainlp-data`` or as set by ``PYTHAINLP_DATA``).
    - :func:`pythainlp.corpus.download` — corpus downloads and catalog
      updates.
    - :func:`pythainlp.corpus.remove` — corpus file and catalog deletions.

    The following **explicit** user-initiated writes are **not** blocked,
    because the user deliberately provided the destination path:

    - Saving a trained model to a user-specified path
      (e.g. ``model.save("my_model.json")``).
    - Training a tagger with an explicit ``save_loc`` argument.
    - Saving a tokenizer vocabulary to a user-specified directory.
    - CLI output files written to a path the user specified or invoked.

    .. note::
        Use :func:`~pythainlp.tools.path.is_offline_mode` (``PYTHAINLP_OFFLINE``)
        to disable only *automatic* background downloads while still allowing
        explicit :func:`~pythainlp.corpus.download` calls.

    :return: ``True`` if PyThaiNLP is in read-only mode, ``False`` otherwise.
    :rtype: bool

    :raises ValueError: if both ``PYTHAINLP_READ_ONLY`` and
        ``PYTHAINLP_READ_MODE`` are set at the same time.

    :Example:

        >>> import os  # doctest: +SKIP
        >>> from pythainlp import is_read_only_mode  # doctest: +SKIP
        >>> os.environ["PYTHAINLP_READ_ONLY"] = "1"  # doctest: +SKIP
        >>> is_read_only_mode()  # doctest: +SKIP
        True
        >>> os.environ["PYTHAINLP_READ_ONLY"] = "0"  # doctest: +SKIP
        >>> is_read_only_mode()  # doctest: +SKIP
        False
    """
    import warnings

    read_only = os.getenv("PYTHAINLP_READ_ONLY")
    read_mode_legacy = os.getenv("PYTHAINLP_READ_MODE")

    if read_only is not None and read_mode_legacy is not None:
        raise ValueError(
            "Both PYTHAINLP_READ_ONLY and PYTHAINLP_READ_MODE are set. "
            "Please use PYTHAINLP_READ_ONLY only and unset PYTHAINLP_READ_MODE."
        )

    if read_mode_legacy is not None and read_only is None:
        warnings.warn(
            "PYTHAINLP_READ_MODE is deprecated; use PYTHAINLP_READ_ONLY instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return read_mode_legacy == "1"

    if read_only is not None:
        return read_only.strip().lower() not in ("", "0", "false", "no", "off")

    return False


def is_unsafe_pickle_allowed() -> bool:
    """Return whether loading legacy pickle-based corpus files is allowed.

    Pickle deserialisation can execute arbitrary code if the file has been
    tampered with, so it is **disabled by default**.
    Set the ``PYTHAINLP_ALLOW_UNSAFE_PICKLE`` environment variable to
    a truthy value (e.g. ``"1"``) only when you trust the corpus file and
    understand the risk.

    :return: ``True`` if legacy pickle loading is allowed, ``False`` otherwise.
    :rtype: bool
    """
    val = os.getenv("PYTHAINLP_ALLOW_UNSAFE_PICKLE", "")
    return val.strip().lower() in ("1", "true", "yes", "on")


def is_offline_mode() -> bool:
    """Return whether PyThaiNLP is operating in offline mode.

    Offline mode is activated by setting the ``PYTHAINLP_OFFLINE``
    environment variable to a truthy value (e.g. ``"1"``).
    Falsy values (``""``, ``"0"``, ``"false"``, ``"no"``, ``"off"``)
    keep online mode active.

    This follows the same convention as ``HF_HUB_OFFLINE`` in
    `huggingface_hub`.

    When offline mode is active, :func:`pythainlp.corpus.get_corpus_path`
    raises :exc:`FileNotFoundError` for any corpus that is not already
    cached locally, instead of triggering an automatic download.

    .. note::
        :func:`pythainlp.corpus.download` always executes regardless of
        this setting, because an explicit call to ``download()`` or
        ``thainlp data get`` is a deliberate user action.
        ``PYTHAINLP_OFFLINE`` only prevents *automatic* downloads
        initiated by :func:`~pythainlp.corpus.get_corpus_path`.

    :return: ``True`` if PyThaiNLP is in offline mode, ``False`` otherwise.
    :rtype: bool

    :Example:

        >>> import os  # doctest: +SKIP
        >>> from pythainlp import is_offline_mode  # doctest: +SKIP
        >>> os.environ["PYTHAINLP_OFFLINE"] = "1"  # doctest: +SKIP
        >>> is_offline_mode()  # doctest: +SKIP
        True
        >>> os.environ["PYTHAINLP_OFFLINE"] = "0"  # doctest: +SKIP
        >>> is_offline_mode()  # doctest: +SKIP
        False
    """
    val = os.getenv("PYTHAINLP_OFFLINE", "")
    return val.strip().lower() not in ("", "0", "false", "no", "off")


def safe_path_join(base: str, *parts: str) -> str:
    """Join *base* with *parts*, verify containment, and return the normalized path.

    This is the authoritative path-traversal guard used throughout the library
    wherever a base directory and external path components are combined
    (e.g., :func:`get_full_data_path` and the internal corpus path helpers
    in :mod:`pythainlp.corpus.core`).

    :param str base: base directory that the result must reside within.
    :param parts: additional path components to append.
    :type parts: str

    :return: normalized absolute path of the joined result.
    :rtype: str

    :raises ValueError: if the resolved path escapes *base*.
    """
    abs_base = os.path.abspath(base)
    abs_full = os.path.abspath(os.path.join(abs_base, *parts))
    if abs_full != abs_base and not abs_full.startswith(abs_base + os.sep):
        raise ValueError(
            f"Path traversal attempt detected: resolved path {abs_full!r} "
            f"is outside the base directory {abs_base!r}."
        )
    return abs_full


def get_full_data_path(path: str) -> str:
    """Join the PyThaiNLP data directory path with *path* and return the result.

    :param str path: relative path or filename to append to the data directory.

    :return: normalized absolute path within the PyThaiNLP data directory.
    :rtype: str

    :raises ValueError: if *path* resolves to a location outside the
        PyThaiNLP data directory (path traversal attempt).

    :Example:

        >>> from pythainlp.tools import get_full_data_path  # doctest: +SKIP
        >>> get_full_data_path("ttc_freq.txt")  # doctest: +SKIP
        '/root/pythainlp-data/ttc_freq.txt'
    """
    return safe_path_join(get_pythainlp_data_path(), path)


def get_pythainlp_data_path() -> str:
    """Return the full path where PyThaiNLP keeps its (downloaded) data.

    The directory is created if it does not yet exist.

    The path is resolved in the following order:

    1. ``PYTHAINLP_DATA`` environment variable (preferred).
    2. ``PYTHAINLP_DATA_DIR`` environment variable
       (deprecated; shows a warning).
    3. If **both** variables are set, the function raises
       :exc:`ValueError` because the conflict must be resolved
       explicitly.
    4. If neither is set, ``~/pythainlp-data`` is used.

    .. deprecated::
        ``PYTHAINLP_DATA_DIR`` is deprecated.
        Use ``PYTHAINLP_DATA`` instead (follows the same pattern as
        ``NLTK_DATA``).

    :return: full path of directory for :mod:`pythainlp` downloaded data
    :rtype: str

    :Example:

        >>> from pythainlp.tools import get_pythainlp_data_path  # doctest: +SKIP
        >>> get_pythainlp_data_path()  # doctest: +SKIP
        '/root/pythainlp-data'
    """
    import warnings

    data_dir = os.getenv("PYTHAINLP_DATA")
    data_dir_legacy = os.getenv("PYTHAINLP_DATA_DIR")

    if data_dir and data_dir_legacy:
        raise ValueError(
            "Both PYTHAINLP_DATA and PYTHAINLP_DATA_DIR are set. "
            "Please use PYTHAINLP_DATA only and unset PYTHAINLP_DATA_DIR."
        )

    if data_dir_legacy and not data_dir:
        warnings.warn(
            "PYTHAINLP_DATA_DIR is deprecated; use PYTHAINLP_DATA instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        data_dir = data_dir_legacy

    resolved = data_dir or os.path.join("~", PYTHAINLP_DEFAULT_DATA_DIR)
    path = os.path.expanduser(resolved)
    if not is_read_only_mode():
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

        >>> from pythainlp.tools import get_pythainlp_path  # doctest: +SKIP
        >>> get_pythainlp_path()  # doctest: +SKIP
        '/usr/local/lib/python3/dist-packages/pythainlp'
    """
    package_path = files("pythainlp")
    # For compatibility, convert to string path if possible
    # This works for both regular installations and zip files
    if hasattr(package_path, "__fspath__"):
        return os.fspath(cast("PathLike[str]", package_path))
    # Fallback for traversable objects that don't support __fspath__
    return str(package_path)
