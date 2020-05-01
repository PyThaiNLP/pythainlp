# -*- coding: utf-8 -*-
from typing import Iterable, List, Union


class Trie:
    class Node(object):
        __slots__ = "end", "children"

        def __init__(self):
            self.end = False
            self.children = {}

    def __init__(self, words: Iterable[str]):
        self.words = words
        self.root = Trie.Node()

        for word in words:
            cur = self.root
            for ch in word:
                node = cur.children.get(ch)
                if not node:
                    node = Trie.Node()
                    cur.children[ch] = node
                cur = node
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
    Create a dictionary trie which will be used for word_tokenize() function.

    :param str|Iterable[str]|pythainlp.tokenize.Trie dict_source: a path to
        dictionary file or a list of words or a pythainlp.tokenize.Trie object
    :return: a trie object created from a dictionary input
    :rtype: pythainlp.tokenize.Trie
    """
    trie = None

    if isinstance(dict_source, Trie):
        trie = dict_source
    elif isinstance(dict_source, str):
        # Receive a file path of the dict to read
        with open(dict_source, "r", encoding="utf8") as f:
            _vocabs = f.read().splitlines()
            trie = Trie(_vocabs)
    elif isinstance(dict_source, Iterable):
        # Note: Since Trie and str are both Iterable,
        # so the Iterable check should be here, at the very end,
        # because it has less specificality
        # Received a sequence type object of vocabs
        trie = Trie(dict_source)
    else:
        raise TypeError(
            "Type of dict_source must be pythainlp.tokenize.Trie, "
            "or Iterable[str], or str (path to source file)"
        )

    return trie
