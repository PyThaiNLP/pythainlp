# -*- coding: utf-8 -*-

import os

import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")
TEMPLATE_FILE = os.path.join(TEMPLATES_DIR, "thaiword.txt")


def get_data():
    with open(TEMPLATE_FILE, "r", encoding="utf8") as f:
        lines = f.read().splitlines()
    return lines
