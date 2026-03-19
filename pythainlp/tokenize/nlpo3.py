# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import threading
from importlib.resources import as_file, files
from sys import stderr
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from nlpo3 import (  # noqa: F401
        load_dict as nlpo3_load_dict,
    )
    from nlpo3 import segment as nlpo3_segment  # noqa: F401

_NLPO3_DEFAULT_DICT_NAME: str = (
    "_73bcj049dzbu9t49b4va170k"  # supposed to be unique
)
_NLPO3_WORDS_FILENAME: str = "words_th.txt"
_NLPO3_DEFAULT_DICT: Optional[str] = None  # Will be lazily loaded
_dict_file_ctx: Optional[Any] = (
    None  # File context manager kept alive for program lifetime
)
_load_lock: threading.Lock = threading.Lock()  # Thread safety for lazy loading


def _ensure_default_dict_loaded() -> None:
    """Ensure the default dictionary is loaded.

    This function uses a lock to ensure thread-safe initialization.
    The context manager is kept alive for the lifetime of the program
    to prevent cleanup of temporary files while the dictionary is in use.

    :raises ImportError: If nlpo3 is not installed.
    :raises RuntimeError: If dictionary loading fails.
    """
    try:
        from nlpo3 import load_dict as nlpo3_load_dict
    except ImportError as ex:
        raise ImportError(
            "nlpo3 is not installed. Install it with: pip install nlpo3"
        ) from ex

    global _NLPO3_DEFAULT_DICT, _dict_file_ctx
    if _NLPO3_DEFAULT_DICT is None:
        with _load_lock:
            # Double-check pattern to avoid race conditions
            if _NLPO3_DEFAULT_DICT is None:
                corpus_files = files("pythainlp.corpus")
                dict_file = corpus_files.joinpath(_NLPO3_WORDS_FILENAME)
                _dict_file_ctx = as_file(dict_file)
                dict_path = _dict_file_ctx.__enter__()
                msg, success = nlpo3_load_dict(
                    str(dict_path), _NLPO3_DEFAULT_DICT_NAME
                )
                if not success:
                    raise RuntimeError(
                        f"Failed to load nlpo3 dictionary: {msg}"
                    )
                _NLPO3_DEFAULT_DICT = _NLPO3_DEFAULT_DICT_NAME


def load_dict(file_path: str, dict_name: str) -> bool:
    """Load a dictionary file into an in-memory dictionary collection.

    The loaded dictionary will be accessible through the assigned dict_name.
    **Note: This function will not override an existing dict name.**

    :param file_path: Path to a dictionary file
    :type file_path: str
    :param dict_name: A unique dictionary name, used for reference.
    :type dict_name: str
    :return success: True if loaded successfully, False otherwise.
    :rtype: bool

    :See Also:
        * \
            https://github.com/PyThaiNLP/nlpo3
    """
    try:
        from nlpo3 import load_dict as nlpo3_load_dict
    except ImportError as ex:
        raise ImportError(
            "nlpo3 is not installed. Install it with: pip install nlpo3"
        ) from ex

    msg: str
    success: bool
    msg, success = nlpo3_load_dict(file_path=file_path, dict_name=dict_name)
    if not success:
        print(msg, file=stderr)
    return success


def segment(
    text: str,
    custom_dict: str = _NLPO3_DEFAULT_DICT_NAME,
    safe_mode: bool = False,
    parallel_mode: bool = False,
) -> list[str]:
    """Break text into tokens.

    Python binding for nlpO3. It is newmm engine in Rust.

    :param str text: text to be tokenized
    :param str custom_dict: dictionary name, as assigned with load_dict(),\
        defaults to pythainlp/corpus/common/words_th.txt
    :param bool safe_mode: reduce chance for long processing time for long text\
        with many ambiguous breaking points, defaults to False
    :param bool parallel_mode: Use multithread mode, defaults to False

    :return: list of tokens
    :rtype: list[str]

    :See Also:
        * \
            https://github.com/PyThaiNLP/nlpo3
    """
    try:
        from nlpo3 import segment as nlpo3_segment
    except ImportError as ex:
        raise ImportError(
            "nlpo3 is not installed. Install it with: pip install nlpo3"
        ) from ex

    # Ensure default dict is loaded if it's being used
    if custom_dict == _NLPO3_DEFAULT_DICT_NAME:
        _ensure_default_dict_loaded()

    result: list[str] = nlpo3_segment(
        text=text,
        dict_name=custom_dict,
        safe=safe_mode,
        parallel=parallel_mode,
    )
    return result
