# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Dictionary-based maximal matching word segmentation, constrained by
Thai Character Cluster (TCC) boundaries with improved rules.

The codes are based on the notebooks created by Korakot Chaovavanich,
with heuristic graph size limit added to avoid exponential waiting time.

:See Also:
    * \
        https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
    * \
        https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
"""
import re
from collections import defaultdict
from heapq import heappop, heappush
from typing import Generator, List

from pythainlp.tokenize import DEFAULT_WORD_DICT_TRIE
from pythainlp.util import Trie

from pythainlp.tokenize.tcc_p import tcc_pos

# match non-Thai tokens
# `|` is used as like "early return",
# which divides "abc123" to "abc", "123" for example.
_PAT_NONTHAI = re.compile(
    r"""(?x)
[-a-zA-Z]+|        # Latin characters
\d+([,\.]\d+)*|    # numbers
[ \t]+|            # spaces
\r?\n|             # newlines
[^\u0E00-\u0E7F \t\r\n]+  # other non-Thai characters, and stops matching until space/newline
"""
)

# match 2-consonant Thai tokens
_PAT_THAI_TWOCHARS = re.compile("[ก-ฮ]{,2}$")


# maximum graph size before cutoff
_MAX_GRAPH_SIZE = 50

# window size for safe mode
_TEXT_SCAN_POINT = 120
_TEXT_SCAN_LEFT = 20
_TEXT_SCAN_RIGHT = 20
_TEXT_SCAN_BEGIN = _TEXT_SCAN_POINT - _TEXT_SCAN_LEFT
_TEXT_SCAN_END = _TEXT_SCAN_POINT + _TEXT_SCAN_RIGHT
del _TEXT_SCAN_POINT
del _TEXT_SCAN_LEFT
del _TEXT_SCAN_RIGHT


def _bfs_paths_graph(
    graph: defaultdict, start: int, goal: int
) -> Generator[List[int], None, None]:
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for pos in graph[vertex]:
            if pos == goal:
                yield path + [pos]
            else:
                queue.append((pos, path + [pos]))


def _onecut(text: str, custom_dict: Trie) -> Generator[str, None, None]:
    # main data structure:
    # - key is beginning position (int)
    # - value is possible ending positions (List[int])
    # if key is not found, value is empty list
    graph = defaultdict(list)

    graph_size = 0  # keep track of graph size, if too big, force cutoff

    valid_poss = tcc_pos(text)  # breaking positions that are TCC-valid

    len_text = len(text)
    pos_list = [0]  # priority queue of possible breaking positions
    end_pos = 0
    while pos_list[0] < len_text:
        begin_pos = heappop(pos_list)
        for word in custom_dict.prefixes(text[begin_pos:]):
            end_pos_candidate = begin_pos + len(word)
            if end_pos_candidate in valid_poss:
                graph[begin_pos].append(end_pos_candidate)
                graph_size = graph_size + 1

                if end_pos_candidate not in pos_list:
                    heappush(pos_list, end_pos_candidate)

                if graph_size > _MAX_GRAPH_SIZE:
                    break

        len_pos_list = len(pos_list)
        if len_pos_list == 1:  # one candidate, no longer ambiguous
            end_pos_candidates = next(
                _bfs_paths_graph(graph, end_pos, pos_list[0])
            )
            graph_size = 0
            for pos in end_pos_candidates[1:]:
                yield text[end_pos:pos]
                end_pos = pos
        elif len_pos_list == 0:  # no candidate, deal with non-dictionary word
            m = _PAT_NONTHAI.match(text[begin_pos:])
            if m:  # non-Thai token, skip to the end
                end_pos = begin_pos + m.end()
            else:  # Thai token, find minimum skip
                for pos in range(begin_pos + 1, len_text):
                    if pos in valid_poss:
                        prefix = text[pos:]
                        words = [
                            word
                            for word in custom_dict.prefixes(prefix)
                            if (
                                (pos + len(word) in valid_poss)
                                and not _PAT_THAI_TWOCHARS.match(word)
                            )
                        ]
                        if words:  # is a Thai token that longer than 2 chars
                            end_pos = pos
                            break

                        # is a non-Thai token
                        if _PAT_NONTHAI.match(prefix):
                            end_pos = pos
                            break
                else:
                    end_pos = len_text

            graph[begin_pos].append(end_pos)
            graph_size = graph_size + 1
            yield text[begin_pos:end_pos]
            heappush(pos_list, end_pos)


def segment(
    text: str,
    custom_dict: Trie = DEFAULT_WORD_DICT_TRIE,
    safe_mode: bool = False,
) -> List[str]:
    """Maximal-matching word segmentation constrained by Thai Character Cluster.

    A dictionary-based word segmentation using maximal matching algorithm,
    constrained by Thai Character Cluster boundaries.

    A custom dictionary can be supplied.

    :param text: text to be tokenized
    :type text: str
    :param custom_dict: tokenization dictionary,\
        defaults to DEFAULT_WORD_DICT_TRIE
    :type custom_dict: Trie, optional
    :param safe_mode: reduce chance for long processing time for long text\
        with many ambiguous breaking points, defaults to False
    :type safe_mode: bool, optional
    :return: list of tokens
    :rtype: List[str]
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = DEFAULT_WORD_DICT_TRIE

    if not safe_mode or len(text) < _TEXT_SCAN_END:
        return list(_onecut(text, custom_dict))

    # if the text is longer than the limit,
    # break them into smaller chunks, then tokenize each chunk
    text_parts = []
    while len(text) >= _TEXT_SCAN_END:
        sample = text[_TEXT_SCAN_BEGIN:_TEXT_SCAN_END]

        # find possible breaking positions
        cut_pos = _TEXT_SCAN_END

        # try to break by space first
        space_idx = sample.rfind(" ")
        if space_idx >= 0:
            cut_pos = space_idx + 1
        else:
            tokens = list(_onecut(sample, custom_dict))
            token_max_idx = 0
            token_max_len = 0
            for i, token in enumerate(tokens):
                if len(token) >= token_max_len:
                    token_max_len = len(token)
                    token_max_idx = i

            # choose the position that covers longest token
            cut_pos = _TEXT_SCAN_BEGIN
            for i in range(0, token_max_idx):
                cut_pos = cut_pos + len(tokens[i])

        text_parts.append(text[:cut_pos])
        text = text[cut_pos:]

    # append remaining text
    if len(text):
        text_parts.append(text)

    # tokenizes each text part
    tokens = []
    for text_part in text_parts:
        tokens.extend(list(_onecut(text_part, custom_dict)))

    return tokens
