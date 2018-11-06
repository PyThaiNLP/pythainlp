# -*- coding: utf-8 -*-
"""
Transliterating text to International Phonetic Alphabet (IPA)
"""
import epitran

epi = epitran.Epitran("tha-Thai")


class IPA:
    def __init__(self, text=""):
        self.text = text

    def str(self):
        return epi.transliterate(self.text)

    def list(self):
        return epi.trans_list(self.text)

    def xsampa_list(self):
        return epi.xsampa_list(self.text)
