# -*- coding: utf-8 -*-

import json
import os

import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")
TEMPLATE_FILE = os.path.join(TEMPLATES_DIR, "thaipos.json")


def get_data():
    with open(TEMPLATE_FILE, encoding="utf8") as f:
        model = json.load(f)
    return model
