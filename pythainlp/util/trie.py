# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Trie data structure.

Designed to be used for tokenizer's dictionary, but can be for other purposes.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Optional, Union


class Trie(Iterable[str]):
    """Trie data structure for efficient prefix-based word search.

    A Trie (prefix tree) is a tree-like data structure used to store
    a collection of strings. It enables fast retrieval of words with
    common prefixes, making it ideal for dictionary-based tokenization
    and autocomplete features.

    :param Iterable[str] words: An iterable collection of words to initialize the Trie

    :Example:

        >>> from pythainlp.util import Trie
        >>> trie = Trie(["สวัสดี", "สวัส", "ดี", "ครับ"])
        >>> "สวัสดี" in trie
        True
        >>> trie.prefixes("สวัสดีครับ")
        ['สวัส', 'สวัสดี']
        >>> trie.add("สวัสดีตอนเช้า")
        >>> len(trie)
        5
    """

    root: Node
    _word_count: int

    class Node:
        __slots__: tuple[str, str] = ("end", "children")

        def __init__(self) -> None:
            self.end: bool = False
            # Children dict is created on demand to reduce memory for leaf nodes.
            self.children: Optional[dict[str, Trie.Node]] = None

    def __init__(self, words: Iterable[str]) -> None:
        self._word_count: int = 0
        self.root: Trie.Node = Trie.Node()
        for word in words:
            self.add(word)

    def add(self, word: str) -> None:
        """Add a word to the trie.
        Spaces in front of and following the word will be removed.

        :param str word: a word
        """
        word = word.strip()
        cur = self.root
        for ch in word:
            if cur.children is None:
                cur.children = {}
            child = cur.children.get(ch)
            if child is None:
                child = Trie.Node()
                cur.children[ch] = child
            cur = child
        if not cur.end:
            cur.end = True
            self._word_count += 1

    def remove(self, word: str) -> None:
        """Remove a word from the trie.
        If the word is not found, do nothing.

        :param str word: a word
        """
        # Navigate to the word's end node, recording the path.
        node = self.root
        path: list[tuple[Trie.Node, Trie.Node, str]] = []
        for ch in word:
            if node.children is None:
                return  # word not in trie
            child = node.children.get(ch)
            if child is None:
                return  # word not in trie
            path.append((node, child, ch))
            node = child
        if not node.end:
            return  # path exists but not a complete word
        node.end = False
        self._word_count -= 1
        # Prune nodes that are now unused (not an end and no children).
        # parent.children is always non-None here because the path was
        # built by traversing through existing children dicts.
        for parent, child, ch in reversed(path):
            if child.end or child.children:
                break
            if parent.children is not None:  # always true; narrows type
                del parent.children[ch]
                if not parent.children:
                    parent.children = None  # free empty dict

    def prefixes(self, text: str, start: int = 0) -> list[str]:
        """List all possible words from first sequence of characters in a word.

        :param str text: text to search for prefixes
        :param int start: starting position in text, defaults to 0
        :return: a list of possible words starting at ``start``
        :rtype: list[str]
        """
        res = []
        cur = self.root
        i = start
        n = len(text)
        while i < n:
            if cur.children is None:
                break
            node = cur.children.get(text[i])
            if node is None:
                break
            if node.end:
                res.append(text[start : i + 1])
            cur = node
            i += 1
        return res

    def __contains__(self, key: str) -> bool:
        cur = self.root
        for ch in key:
            if cur.children is None:
                return False
            node = cur.children.get(ch)
            if node is None:
                return False
            cur = node
        return cur.end

    def __iter__(self) -> Iterator[str]:
        # DFS through the trie to yield all stored words.
        # A shared mutable prefix list is appended/popped to avoid
        # O(k²) list copies that a stack-based approach would incur.
        def _dfs(node: Trie.Node, prefix: list[str]) -> Iterator[str]:
            if node.end:
                yield "".join(prefix)
            if node.children:
                for ch, child in node.children.items():
                    prefix.append(ch)
                    yield from _dfs(child, prefix)
                    prefix.pop()

        yield from _dfs(self.root, [])

    def __len__(self) -> int:
        return self._word_count


def dict_trie(dict_source: Union[str, Iterable[str], Trie]) -> Trie:
    """Create a dictionary trie from a file or an iterable.

    :param str|Iterable[str]|pythainlp.util.Trie dict_source: a path to
        dictionary file or a list of words or a pythainlp.util.Trie object
    :return: a trie object
    :rtype: pythainlp.util.Trie
    """
    trie = Trie([])

    if isinstance(dict_source, str) and len(dict_source) > 0:
        # dict_source is a path to dictionary text file
        with open(dict_source, encoding="utf8") as f:
            _vocabs = f.read().splitlines()
            trie = Trie(_vocabs)
    elif isinstance(dict_source, Iterable) and not isinstance(
        dict_source, str
    ):
        # Note: Since Trie and str are both Iterable,
        # so the Iterable check should be here, at the very end,
        # because it has less specificality
        trie = Trie(dict_source)
    else:
        raise TypeError(
            "Type of dict_source must be pythainlp.util.Trie, "
            "or Iterable[str], or non-empty str (path to source file)"
        )

    return trie
