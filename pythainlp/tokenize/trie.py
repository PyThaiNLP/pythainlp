# -*- coding: utf-8 -*-
class Trie:

    class Node(object):
        __slots__ = 'end', 'children'

        def __init__(self):
            self.end = False
            self.children = {}

    def __init__(self, words):
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

    def prefixes(self, text):
        res = []
        cur = self.root
        for i, ch in enumerate(text):
            node = cur.children.get(ch)
            if not node:
                break
            if node.end:
                res.append(text[:i+1])
            cur = node
        return res

    def __contains__(self, key):
        return key in self.words

    def __iter__(self):
        yield from self.words
