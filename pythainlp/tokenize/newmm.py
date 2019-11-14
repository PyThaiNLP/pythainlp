# -*- coding: utf-8 -*-
"""
Dictionary-based Thai Word Segmentation
using maximal matching algorithm and Thai Character Cluster (TCC).

The code is based on the notebooks created by Korakot Chaovavanich.

:See Also:
    * \
        https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
    * \
        https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
"""
import re
from collections import defaultdict
from heapq import heappop, heappush  # for priority queue
from typing import Generator, List

from pythainlp.tokenize import DEFAULT_DICT_TRIE

from .tcc import tcc_pos
from .trie import Trie

# To tokenize English words, for example
_PAT_ENG = re.compile(
    r"""(?x)
[-a-zA-Z]+|   # Latin
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
"""
)

_PAT_TWOCHARS = re.compile("[ก-ฮ]{,2}$")

_TEXT_LIMIT = 120
_TEXT_SCAN_LEFT = 20
_TEXT_SCAN_RIGHT = 20


def _bfs_paths_graph(
    graph: defaultdict, start: int, goal: List[int]
) -> Generator[List[int], None, None]:
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex]:
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def _onecut(text: str, custom_dict: Trie) -> Generator[str, None, None]:
    graph = defaultdict(list)  # main data structure
    allow_pos = tcc_pos(text)  # separating position should aligned with TCC

    q = [0]  # min-heap queue
    last_p = 0  # last position for yield
    while q[0] < len(text):
        p = heappop(q)

        for w in custom_dict.prefixes(text[p:]):
            p_ = p + len(w)
            if p_ in allow_pos:  # only pick one that is TCC-valid
                graph[p].append(p_)
                if p_ not in q:
                    heappush(q, p_)

        # if length == 1 means no longer ambiguous, return previous result
        if len(q) == 1:
            pp = next(_bfs_paths_graph(graph, last_p, q[0]))
            # will eventually start at last_p = pp[0]
            for p in pp[1:]:
                yield text[last_p:p]
                last_p = p
            # will eventually stop at last_p == q[0]

        # if length == 0 means not found in dictionary
        if len(q) == 0:
            m = _PAT_ENG.match(text[p:])
            if m:  # Latin characters, numeric, space
                i = p + m.end()
            else:  # as mininum skip as possible
                for i in range(p + 1, len(text)):
                    if i in allow_pos:  # only if TCC-valid
                        ww = [
                            w
                            for w in custom_dict.prefixes(text[i:])
                            if (i + len(w) in allow_pos)
                        ]
                        ww = [w for w in ww if not _PAT_TWOCHARS.match(w)]
                        m = _PAT_ENG.match(text[i:])
                        if ww or m:
                            break
                else:
                    i = len(text)
            w = text[p:i]
            graph[p].append(i)
            yield w
            last_p = i
            heappush(q, i)


def segment(
    text: str, custom_dict: Trie = DEFAULT_DICT_TRIE, safe_mode: bool = False
) -> List[str]:
    """
    Dictionary-based maximal matching word segmentation, constrained with
    Thai Character Cluster boundaries.

    :param str text: text to be tokenized to words
    :param pythainlp.trie.Trie custom_dict: dictionary for tokenization
    :param bool safe_mode: True to avoid long wait for long continuous text\
        (edge case); Default is False
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = DEFAULT_DICT_TRIE

    if not safe_mode:
        return list(_onecut(text, custom_dict))

    text_len = len(text)

    if text_len < (_TEXT_LIMIT + _TEXT_SCAN_RIGHT):
        # if the text is shorter than the limit,
        # tokenizes the whole text at once
        return list(_onecut(text, custom_dict))
    else:
        # if the text is longer than the limit,
        # breaks them into smaller chunks then tokenizes each chunk
        text_parts = []

        while text_len >= (_TEXT_LIMIT + _TEXT_SCAN_RIGHT):
            sample_start = _TEXT_LIMIT - _TEXT_SCAN_LEFT
            sample_end = _TEXT_LIMIT + _TEXT_SCAN_RIGHT
            sample = text[sample_start:sample_end]

            # find possible break positions
            cut_pos = sample_end

            # try to break by space first
            space_idx = sample.rfind(" ")
            if space_idx >= 0:
                cut_pos = space_idx + 1
            else:
                tokens = list(_onecut(sample, custom_dict))
                token_max_idx = 0
                for i, token in enumerate(tokens):
                    token_max_len = 0
                    if len(token) > token_max_len:
                        token_max_len = len(token)
                        token_max_idx = i

                # choose the position that covers longest token
                cut_pos = sample_start
                for i in range(0, token_max_idx):
                    cut_pos = cut_pos + len(tokens[i])

            text_parts.append(text[:cut_pos])
            text = text[cut_pos:]
            text_len = len(text)

        # append remaining text
        if text_len:
            text_parts.append(text)

        # tokenizes each text parts
        tokens = []
        for text_part in text_parts:
            tokens.extend(list(_onecut(text_part, custom_dict)))

        return tokens
