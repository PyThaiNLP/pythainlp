# -*- coding: utf-8 -*-
"""
Get data from ConceptNet API at http://conceptnet.io
"""
import requests


def edges(word: str, lang: str = "th"):
    """
    Get edges from ConceptNet API

    :param str word: word
    :param str lang: language
    """

    obj = requests.get(f"http://api.conceptnet.io/c/{lang}/{word}").json()
    return obj["edges"]
