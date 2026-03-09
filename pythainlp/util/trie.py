# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Trie data structure.

Designed to be used for tokenizer's dictionary, but can be for other purposes.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Union


class Trie(Iterable[str]):
    """Trie data structure for efficient prefix-based word search.

    A Trie (prefix tree) is a tree-like data structure used to store
    a collection of strings. It enables fast retrieval of words with
    common prefixes, making it ideal for dictionary-based tokenization
    and autocomplete features.

    :param Iterable[str] words: An iterable collection of words to initialize the Trie

    :Example:
    ::

        from pythainlp.util import Trie

        # Create a trie with Thai words
        trie = Trie(["สวัสดี", "สวัส", "ดี", "ครับ"])

        # Check if word exists
        "สวัสดี" in trie
        # output: True

        # Find all prefixes of a word
        trie.prefixes("สวัสดีครับ")
        # output: ['สวัส', 'สวัสดี']

        # Add a new word
        trie.add("สวัสดีตอนเช้า")

        # Get number of words in trie
        len(trie)
        # output: 5
    """

    words: set[str]
    root: Node

    class Node:
        __slots__: tuple[str, str] = ("end", "children")

        def __init__(self) -> None:
            self.end: bool = False
            self.children: dict[str, Trie.Node] = {}

    def __init__(self, words: Iterable[str]) -> None:
        self.words: set[str] = set(words)
        self.root: Trie.Node = Trie.Node()

        for word in words:
            self.add(word)

    def add(self, word: str) -> None:
        """Add a word to the trie.
        Spaces in front of and following the word will be removed.

        :param str text: a word
        """
        word = word.strip()
        self.words.add(word)
        cur = self.root
        for ch in word:
            child = cur.children.get(ch)
            if not child:
                child = Trie.Node()
                cur.children[ch] = child
            cur = child
        cur.end = True

    def remove(self, word: str) -> None:
        """Remove a word from the trie.
        If the word is not found, do nothing.

        :param str text: a word
        """
        # remove from set first
        if word not in self.words:
            return
        self.words.remove(word)
        # then remove from nodes
        parent = self.root
        data = []  # track path to leaf
        for ch in word:
            child = parent.children[ch]
            data.append((parent, child, ch))
            parent = child
        # remove the last one
        child.end = False
        # prune up the tree
        for parent, child, ch in reversed(data):
            if child.end or child.children:
                break
            del parent.children[ch]  # remove from parent dict

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
            node = cur.children.get(text[i])
            if not node:
                break
            if node.end:
                res.append(text[start : i + 1])
            cur = node
            i += 1
        return res

    def __contains__(self, key: str) -> bool:
        return key in self.words

    def __iter__(self) -> Iterator[str]:
        yield from self.words

    def __len__(self) -> int:
        return len(self.words)


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
