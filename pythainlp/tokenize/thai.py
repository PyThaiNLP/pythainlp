# -*- coding: utf-8 -*-
import os
import pythainlp

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "corpus")


def fileload(name1):
    return os.path.join(TEMPLATES_DIR, name1)


def data():
    """
    โหลดรายการคำศัพท์ภาษาไทย (ตัวเก่า)
    """
    with open(fileload("thaiword.txt"), "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    return lines


def newdata():
    """
    โหลดรายการคำศัพท์ภาษาไทย (ตัวใหม่)
    """
    with open(fileload("new-thaidict.txt"), "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    return lines
