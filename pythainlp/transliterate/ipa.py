# -*- coding: utf-8 -*-
"""
Transliterating text to International Phonetic Alphabet (IPA)
"""

try:
    import epitran
except ImportError:
    from pythainlp.tools import install_package

    install_package("epitran")
    try:
        import epitran
    except ImportError:
        raise ImportError("ImportError: Try 'pip install epitran'")

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
