# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Tokenize Thai text into words with dictionary-based maximal matching.

The tokenizer constrains the matching by Thai Character Cluster (TCC)
boundaries with improved rules.

The code is based on notebooks created by Korakot Chaovavanich,
with a heuristic graph size limit added to avoid exponential waiting time.

:See Also:
    * Colab notebook, version 1:
      https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
    * Colab notebook, version 2:
      https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw
"""

from __future__ import annotations

import re
from collections import defaultdict
from heapq import heappop, heappush
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from collections.abc import Generator

    from pythainlp.util import Trie

from pythainlp.tokenize import word_dict_trie
from pythainlp.tokenize.tcc_p import tcc_pos_array

# match non-Thai tokens
# `|` is used as like "early return",
# which divides "abc123" to "abc", "123" for example.
_PAT_NONTHAI: re.Pattern[str] = re.compile(
    r"""(?x)
[-a-zA-Z]+|        # Latin characters
\d+([,\.]\d+)*|    # numbers
[ \t]+|            # spaces
\r?\n|             # newlines
[^\u0E00-\u0E7F \t\r\n]+  # other non-Thai characters, and stops matching until space/newline
"""
)

# match 2-consonant Thai tokens
_PAT_THAI_TWOCHARS: re.Pattern[str] = re.compile("[ก-ฮ]{,2}$")


# maximum graph size before cutoff
_MAX_GRAPH_SIZE: int = 50

# window size for safe mode
_TEXT_SCAN_POINT: int = 120
_TEXT_SCAN_LEFT: int = 20
_TEXT_SCAN_RIGHT: int = 20
_TEXT_SCAN_BEGIN: int = _TEXT_SCAN_POINT - _TEXT_SCAN_LEFT
_TEXT_SCAN_END: int = _TEXT_SCAN_POINT + _TEXT_SCAN_RIGHT
del _TEXT_SCAN_POINT
del _TEXT_SCAN_LEFT
del _TEXT_SCAN_RIGHT


def _bfs_paths_graph(
    graph: defaultdict[int, list[int]], start: int, goal: int
) -> Generator[list[int], None, None]:
    # visited set prevents re-exploring nodes already reached via a shorter
    # path, converting worst-case BFS from exponential to O(V + E).
    visited: set[int] = {start}
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for pos in graph[vertex]:
            if pos == goal:
                yield [*path, pos]
            elif pos not in visited:
                visited.add(pos)
                queue.append((pos, [*path, pos]))


def _extend_graph(
    graph: defaultdict[int, list[int]],
    pos_list: list[int],
    text: str,
    begin_pos: int,
    valid_poss: bytearray,
    custom_dict: Trie,
    graph_size: int,
) -> int:
    """
    Add dictionary words starting at ``begin_pos`` to the graph.

    :param graph: graph of beginning positions to ending positions
    :param list[int] pos_list: priority queue of possible breaking positions
    :param str text: text being tokenized
    :param int begin_pos: position to start from
    :param bytearray valid_poss: valid TCC break positions
    :param pythainlp.util.Trie custom_dict: dictionary trie
    :param int graph_size: current graph size
    :return: new graph size
    :rtype: int
    """
    for word in custom_dict.prefixes(text, begin_pos):
        end_pos_candidate = begin_pos + len(word)
        if valid_poss[end_pos_candidate]:
            graph[begin_pos].append(end_pos_candidate)
            graph_size = graph_size + 1

            if end_pos_candidate not in pos_list:
                heappush(pos_list, end_pos_candidate)

            if graph_size > _MAX_GRAPH_SIZE:
                break
    return graph_size


def _find_skip_end(
    text: str,
    begin_pos: int,
    valid_poss: bytearray,
    custom_dict: Trie,
) -> int:
    """Find the end of an out-of-dictionary word starting at ``begin_pos``."""
    len_text = len(text)
    m = _PAT_NONTHAI.match(text, begin_pos)
    if m:  # non-Thai token, skip to the end
        return m.end()

    # Thai token, find minimum skip
    for pos in range(begin_pos + 1, len_text):
        if valid_poss[pos]:
            words = [
                word
                for word in custom_dict.prefixes(text, pos)
                if (
                    valid_poss[pos + len(word)]
                    and not _PAT_THAI_TWOCHARS.match(word)
                )
            ]
            if words:  # is a Thai token that longer than 2 chars
                return pos

            # is a non-Thai token
            if _PAT_NONTHAI.match(text, pos):
                return pos
    return len_text


def _onecut(text: str, custom_dict: Trie) -> Generator[str, None, None]:
    # main data structure:
    # - key is beginning position (int)
    # - value is possible ending positions (List[int])
    # if key is not found, value is empty list
    graph: defaultdict[int, list[int]] = defaultdict(list)

    graph_size = 0  # keep track of graph size, if too big, force cutoff

    valid_poss = tcc_pos_array(text)  # bytearray of valid TCC break positions

    len_text = len(text)
    pos_list = [0]  # priority queue of possible breaking positions
    end_pos = 0
    while pos_list[0] < len_text:
        begin_pos = heappop(pos_list)
        graph_size = _extend_graph(
            graph,
            pos_list,
            text,
            begin_pos,
            valid_poss,
            custom_dict,
            graph_size,
        )

        len_pos_list = len(pos_list)
        if len_pos_list == 1:  # one candidate, no longer ambiguous
            end_pos_candidates = next(
                _bfs_paths_graph(graph, end_pos, pos_list[0])
            )
            graph_size = 0
            graph.clear()
            for pos in end_pos_candidates[1:]:
                yield text[end_pos:pos]
                end_pos = pos
        elif len_pos_list == 0:  # no candidate, deal with non-dictionary word
            end_pos = _find_skip_end(text, begin_pos, valid_poss, custom_dict)
            graph_size = 0
            graph.clear()
            yield text[begin_pos:end_pos]
            heappush(pos_list, end_pos)


def _split_chunks(text: str, custom_dict: Trie) -> list[str]:
    """Split a long text into chunks at likely breaking points."""
    text_parts = []
    while len(text) >= _TEXT_SCAN_END:
        cut_pos = _find_cut_pos(text, custom_dict)
        text_parts.append(text[:cut_pos])
        text = text[cut_pos:]

    if len(text):
        text_parts.append(text)
    return text_parts


def _find_cut_pos(text: str, custom_dict: Trie) -> int:
    """Find a position to cut a chunk, in the scan window of ``text``."""
    sample = text[_TEXT_SCAN_BEGIN:_TEXT_SCAN_END]

    # try to break by space first
    space_idx = sample.rfind(" ")
    if space_idx >= 0:
        return space_idx + 1 + _TEXT_SCAN_BEGIN

    tokens = list(_onecut(sample, custom_dict))
    token_max_idx = 0
    token_max_len = 0
    for i, token in enumerate(tokens):
        if len(token) >= token_max_len:
            token_max_len = len(token)
            token_max_idx = i

    # choose the position that covers longest token
    cut_pos = _TEXT_SCAN_BEGIN
    for i in range(token_max_idx):
        cut_pos = cut_pos + len(tokens[i])
    return cut_pos


def segment(
    text: str,
    custom_dict: Optional[Trie] = None,
    safe_mode: bool = False,
) -> list[str]:
    """
    Tokenize text into words with maximal matching and TCC boundaries.

    This is a dictionary-based tokenizer that uses a maximal matching
    algorithm, constrained by Thai Character Cluster (TCC) boundaries.
    A custom dictionary can be supplied.

    For very long text (hundreds of kilobytes or more), consider using
    ``safe_mode=True`` to enable chunk-based processing and reduce memory
    use.

    :param str text: text to be tokenized
    :param pythainlp.util.Trie custom_dict: dictionary trie
        (default: the default word trie)
    :param bool safe_mode: True to use chunk-based processing, which reduces
        memory use and processing time for long text with many ambiguous
        breaking points (default: False)
    :return: list of words
    :rtype: list[str]
    """
    if not text or not isinstance(text, str):
        return []

    if not custom_dict:
        custom_dict = word_dict_trie()

    if not safe_mode or len(text) < _TEXT_SCAN_END:
        return list(_onecut(text, custom_dict))

    # if the text is longer than the limit,
    # break them into smaller chunks, then tokenize each chunk
    tokens: list[str] = []
    for text_part in _split_chunks(text, custom_dict):
        tokens.extend(_onecut(text_part, custom_dict))

    return tokens
