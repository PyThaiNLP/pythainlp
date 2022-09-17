# -*- coding: utf-8 -*-
"""
esupar: Tokenizer POS-tagger and Dependency-parser with BERT/RoBERTa/DeBERTa models for Japanese and other languages

GitHub: https://github.com/KoichiYasuoka/esupar
"""
import esupar


class Parse:
    def __init__(self, model: str="th") -> None:
        if model == None:
            model = "th"
        self.nlp=esupar.load(model)

    def __call__(self, text):
        return self.nlp(text)
