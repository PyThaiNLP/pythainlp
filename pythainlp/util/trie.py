# -*- coding: utf-8 -*-
"""
Trie data structure.

Designed to use for tokenizer's dictionary, but can be for other purposes.
"""
from typing import Iterable, List, Union


class Trie:
    class Node(object):
        __slots__ = "end", "children"

        def __init__(self):
            self.end = False
            self.children = {}
        
        def add(self, ch: str):
            child = self.children.get(ch)
            if not child:
                child = Trie.Node()
                self.children[ch] = child
            return child

    def __init__(self, words: Iterable[str]):
        self.words = words
        self.root = Trie.Node()

        for word in words:
            cur = self.root
            for ch in word:
                cur = cur.add(ch)
            cur.end = True

    def prefixes(self, text: str) -> List[str]:
        res = []
        cur = self.root
        for i, ch in enumerate(text):
            node = cur.children.get(ch)
            if not node:
                break
            if node.end:
                res.append(text[: i + 1])
            cur = node
        return res

    def __contains__(self, key: str) -> bool:
        return key in self.words

    def __iter__(self) -> Iterable[str]:
        yield from self.words


def dict_trie(dict_source: Union[str, Iterable[str], Trie]) -> Trie:
    """
    Create a dictionary trie from a string or an iterable.

    :param str|Iterable[str]|pythainlp.util.Trie dict_source: a path to
        dictionary file or a list of words or a pythainlp.util.Trie object
    :return: a trie object created from a dictionary input
    :rtype: pythainlp.util.Trie
    """
    trie = None

    if isinstance(dict_source, str) and len(dict_source) > 0:
        # dict_source is a path to dictionary text file
        with open(dict_source, "r", encoding="utf8") as f:
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
