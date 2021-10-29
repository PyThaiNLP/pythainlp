# -*- coding: utf-8 -*-
from typing import List
from nlpo3 import segment as nlpo3_segment
from pythainlp.corpus import path_pythainlp_corpus, _THAI_WORDS_FILENAME

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
    return nlpo3_segment(
        text=text,
        dict_name=custom_dict,
        safe=safe_mode,
        parallel=parallel
    )