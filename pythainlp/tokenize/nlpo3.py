# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from sys import stderr

from nlpo3 import load_dict as nlpo3_load_dict
from nlpo3 import segment as nlpo3_segment

from pythainlp.corpus import path_pythainlp_corpus
from pythainlp.corpus.common import _THAI_WORDS_FILENAME

_NLPO3_DEFAULT_DICT_NAME = "_73bcj049dzbu9t49b4va170k"  # supposed to be unique
_NLPO3_DEFAULT_DICT = nlpo3_load_dict(
    path_pythainlp_corpus(_THAI_WORDS_FILENAME), _NLPO3_DEFAULT_DICT_NAME
)  # preload default dict, so it can be accessible by _NLPO3_DEFAULT_DICT_NAME


def load_dict(file_path: str, dict_name: str) -> bool:
    """Load a dictionary file into an in-memory dictionary collection.

    The loaded dictionary will be accessible through the assigned dict_name.
    *** This function will not override an existing dict name. ***

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
    :rtype: List[str]

    :See Also:
        * \
            https://github.com/PyThaiNLP/nlpo3
    """
    return nlpo3_segment(
        text=text,
        dict_name=custom_dict,
        safe=safe_mode,
        parallel=parallel_mode,
    )
