# -*- coding: utf-8 -*-

import os

import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")


def get_data(dict_fname="thaiword.txt"):
    template_file = os.path.join(TEMPLATES_DIR, dict_fname)
    with open(template_file, "r", encoding="utf8") as f:
        lines = f.read().splitlines()
    return lines
