# -*- coding: utf-8 -*-

"""
นี่คือ API สำหรับดึงข้อมูลมาจาก http://conceptnet.io
"""
import requests


def edges(word, lang="th"):
    obj = requests.get("http://api.conceptnet.io/c/{}/{}".format(lang, str(word))).json()
    return obj["edges"]
