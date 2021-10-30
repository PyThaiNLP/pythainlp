# -*- coding: utf-8 -*-
from typing import List
from pathlib import Path
from nlpo3 import segment as nlpo3_segment
from nlpo3 import load_dict
from pythainlp.corpus.common import _THAI_WORDS_FILENAME
from pythainlp.corpus import path_pythainlp_corpus


def segment(
    text: str,
    custom_dict: str = path_pythainlp_corpus(_THAI_WORDS_FILENAME),
    safe_mode: bool = False,
    parallel=False
) -> List[str]:
    """
    nlpO3 Python binding

    Python binding for nlpO. It is newmm engine in Rust.

    :param str text: text to be tokenized
    :param str custom_dict: a path of word dictionary
    :param bool safe_mode:reduce chance for long processing time in long text\
        with many ambiguous breaking points, defaults to False
    :param bool parallel: Use multithread mode, defaults to False

    :return: list of tokens
    :rtype: List[str]

    :See Also:
        * \
            https://github.com/PyThaiNLP/nlpo3
    """
    _file_name = Path(custom_dict).stem
    load_dict(custom_dict, _file_name+"_dict")
    return nlpo3_segment(
        text=text,
        dict_name=_file_name+"_dict",
        safe=safe_mode,
        parallel=parallel
    )
