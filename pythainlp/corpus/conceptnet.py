# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Get data from ConceptNet API at http://conceptnet.io
"""
import requests


def edges(word: str, lang: str = "th"):
    """
    Get edges from `ConceptNet <http://api.conceptnet.io/>`_ API.
    ConceptNet is a public semantic network, designed to help computers
    understand the meanings of words that people use.

    For example, the term "ConceptNet" is a "knowledge graph", and
    "knowledge graph" has "common sense knowledge" which is a part of
    "artificial intelligence". Also, "ConcepNet" is used for
    "natural language understanding" which is a part of
    "artificial intelligence".

      | "ConceptNet" --is a--> "knowledge graph" --has--> "common sense"\
          --a part of--> "artificial intelligence"
      | "ConceptNet" --used for--> "natural language understanding"\
          --a part of--> "artificial intelligence"

    With this illustration, it shows relationships (represented as *Edge*)
    between the terms (represented as *Node*)

    :param str word: word to be sent to ConceptNet API
    :param str lang: abbreviation of language (i.e. *th* for Thai, *en* for
                     English, or *ja* for Japan). By default, it is *th*
                     (Thai).

    :return: return edges of the given word according to the
             ConceptNet network.
    :rtype: list[dict]

    :Example:
    ::

        from pythainlp.corpus.conceptnet import edges

        edges('hello', lang='en')
        # output:
        # [{
        #   '@id': '/a/[/r/IsA/,/c/en/hello/,/c/en/greeting/]',
        #   '@type': 'Edge',
        #   'dataset': '/d/conceptnet/4/en',
        #   'end': {'@id': '/c/en/greeting',
        #   '@type': 'Node',
        #   'label': 'greeting',
        #   'language': 'en',
        #   'term': '/c/en/greeting'},
        #   'license': 'cc:by/4.0',
        #   'rel': {'@id': '/r/IsA', '@type': 'Relation', 'label': 'IsA'},
        #   'sources': [
        #   {
        #   '@id': '/and/[/s/activity/omcs/vote/,/s/contributor/omcs/bmsacr/]',
        #   '@type': 'Source',
        #   'activity': '/s/activity/omcs/vote',
        #   'contributor': '/s/contributor/omcs/bmsacr'
        #   },
        #   {
        #     '@id': '/and/[/s/activity/omcs/vote/,/s/contributor/omcs/test/]',
        #     '@type': 'Source',
        #     'activity': '/s/activity/omcs/vote',
        #     'contributor': '/s/contributor/omcs/test'}
        #   ],
        #   'start': {'@id': '/c/en/hello',
        #   '@type': 'Node',
        #   'label': 'Hello',
        #   'language': 'en',
        #   'term': '/c/en/hello'},
        #   'surfaceText': '[[Hello]] is a kind of [[greeting]]',
        #   'weight': 3.4641016151377544
        # }, ...]

        edges('สวัสดี', lang='th')
        # output:
        # [{
        #  '@id': '/a/[/r/RelatedTo/,/c/th/สวัสดี/n/,/c/en/prosperity/]',
        #  '@type': 'Edge',
        #  'dataset': '/d/wiktionary/en',
        #  'end': {'@id': '/c/en/prosperity',
        #  '@type': 'Node',
        #  'label': 'prosperity',
        #  'language': 'en',
        #  'term': '/c/en/prosperity'},
        #  'license': 'cc:by-sa/4.0',
        #  'rel': {
        #      '@id': '/r/RelatedTo', '@type': 'Relation',
        #      'label': 'RelatedTo'},
        #  'sources': [{
        #  '@id': '/and/[/s/process/wikiparsec/2/,/s/resource/wiktionary/en/]',
        #  '@type': 'Source',
        #  'contributor': '/s/resource/wiktionary/en',
        #  'process': '/s/process/wikiparsec/2'}],
        #  'start': {'@id': '/c/th/สวัสดี/n',
        #  '@type': 'Node',
        #  'label': 'สวัสดี',
        #  'language': 'th',
        #  'sense_label': 'n',
        #  'term': '/c/th/สวัสดี'},
        #  'surfaceText': None,
        #  'weight': 1.0
        # }, ...]
    """

    obj = requests.get(f"https://api.conceptnet.io/c/{lang}/{word}").json()
    return obj["edges"]
